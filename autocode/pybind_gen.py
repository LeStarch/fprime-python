"""
pybind_gen.py:

This is a very crude implementation of the python templater for python bindings.
"""
import argparse
import os
import re
import sys
from pathlib import Path
from collections import OrderedDict

from xml.dom.minidom import parse, parseString

from jinja2 import Environment, PackageLoader, select_autoescape

from fprime_ac.utils.buildroot import search_for_file, build_root_relative_path, set_build_roots

env = Environment(
    loader=PackageLoader(__name__),
    autoescape=select_autoescape()
)


def parse_enum(xml):
    """ Maps Enum XML to an enum item """
    root = xml.getElementsByTagName("enum")[0]
    values = [tag.getAttribute("name") for tag in xml.getElementsByTagName("item")]
    return {"ns": root.getAttribute("namespace"), "name": root.getAttribute("name"), "vals": values}


def parse_array(xml):
    """ Maps Enum XML to an array item """
    root = xml.getElementsByTagName("array")[0]
    size = int(root.getElementsByTagName("size")[0].firstChild.nodeValue)
    etype = root.getElementsByTagName("type")[0].firstChild.nodeValue
    return {"ns": root.getAttribute("namespace"), "name": root.getAttribute("name"), "elem_type": etype, "size": size}


def parse_serializable(xml):
    """ Maps Enum XML to an enum item """
    members_to_types = OrderedDict()
    root = xml.getElementsByTagName("serializable")[0]
    for tag in xml.getElementsByTagName("member"):
        members_to_types[tag.getAttribute("name")] = tag.getAttribute("type")
    return {"ns": root.getAttribute("namespace"), "name": root.getAttribute("name"), "member_list": members_to_types}


def parse_args(xml, source=None):
    """"""
    results = []
    for arg in xml.getElementsByTagName("arg"):
        arg_type = arg.getAttribute("type")
        if source is not None and arg_type == "string":
            arg_type = f"Fw::{ source }StringArg"
        results.append((arg.getAttribute("name"), arg_type))
    return results


def parse_comp_commands(xml):
    """"""
    results = []
    for command in xml.getElementsByTagName("command"):
        name = command.getAttribute("mnemonic")
        args = [("opCode", "FwOpcodeType"), ("cmdSeq", "U32")] + parse_args(command, "Cmd")
        results.append({"name": name, "arg_full_texts": ["{} {}".format(atype, name) for name, atype in args],
                        "arg_names": ["{}".format(name) for name, _ in args], "args": args})
    return results


def parse_comp_extras(xml, extra_type):
    """"""
    results = []
    for item in xml.getElementsByTagName(extra_type):
        obj = {"name": item.getAttribute("name")}
        if extra_type == "event":
            args = parse_args(item)
            obj["severity"] = item.getAttribute("severity")
            obj["arg_full_texts"] = ["{} {}".format(atype, name) for name, atype in args],
            obj["arg_names"] = ["{}".format(name) for name, _ in args]
        results.append(obj)
    return results


def port_defs(xml):
    """"""
    results = {}
    for port_import in xml.getElementsByTagName("import_port_type"):
        with open(search_for_file("Port", port_import.firstChild.nodeValue), "r") as file_handle:
            port_xml = parse(file_handle)
            args = [("portNum", "NATIVE_INT_TYPE")] + list(parse_args(port_xml))
            ns = port_xml.documentElement.getAttribute("namespace")
            name = port_xml.documentElement.getAttribute("name")
            results[ns + "::" + name] = {"name": name, "ns": ns, "arg_full_texts": ["{} {}".format(atype, name) for name, atype in args],
                                         "arg_names": ["{}".format(name) for name, _ in args], "args": args}
    return results


def parse_comp_ports(xml):
    """"""
    verboten = ["Fw::Cmd", "Fw::CmdResponse", "Fw::CmdReg", "Fw::LogText", "Fw::Log", "Fw::Tlm", "Fw::Time"] #TODO: fix this for role ports
    in_ports = []
    out_ports = []
    port_definitions = port_defs(xml)
    for port in xml.getElementsByTagName("port"):
        dtype = port.getAttribute("data_type")
        name = port.getAttribute("name")
        kind = port.getAttribute("kind")
        port_def = port_definitions[dtype]
        try:
            obj = {"name": name, "ns": port_def["ns"], "args": port_def["args"], "arg_full_texts": port_def["arg_full_texts"], "arg_names": port_def["arg_names"]}
        except:
            raise Exception(f"Malformed port definition with name: { name }")
        if "input" in kind and dtype not in verboten:
            in_ports.append(obj)
        elif "output" in kind and dtype not in verboten:
            out_ports.append(obj)
    return in_ports, out_ports

def parse_component(xml):
    """ Maps Enum XML to an enum item """
    elements = []
    for tag in xml.getElementsByTagName("import_dictionary"):
        with open(search_for_file("Any", tag.firstChild.nodeValue), "r") as file_handle:
            elements += [parse(file_handle).documentElement]
    for element in elements:
        xml.documentElement.appendChild(element)
    root = xml.documentElement
    component = {"ns": root.getAttribute("namespace"), "name": root.getAttribute("name"), "kind": root.getAttribute("kind")}
    component["commands"] = parse_comp_commands(xml)
    component["events"] = parse_comp_extras(xml, "event")
    component["channels"] = parse_comp_extras(xml, "channel")
    in_ports, out_ports = parse_comp_ports(xml)
    component["in_ports"] = in_ports
    component["out_ports"] = out_ports
    return component


PARSE_ROUTE_TABLE = {
    "Enum": parse_enum,
    "Array": parse_array,
    "Serializable": parse_serializable,
    "Component": parse_component
}


def main():
    """ Reads a list of XMLs from file, generates output """
    parser = argparse.ArgumentParser(description='Parse out the python bindings and generate binding outputs')
    parser.add_argument('--ai', nargs='+', help='AI file list of files that might need bindings')
    parser.add_argument('--deps', nargs='+', help='Dependencies of components explicitly requesting pybind')
    args = parser.parse_args()



    # Setup mechanics for fprime autocoders
    set_build_roots(os.environ["BUILD_ROOT"])
    searcher = re.compile(r"(Component|Enum|Array|Serializable)Ai\.xml")
    # Read out XML list and make them absolute
    paths = set([Path(item).absolute() for item in args.ai])
    namespaces = {}

    # Running through each path
    for path in paths:
        relative_path = build_root_relative_path(str(path))
        searched = searcher.search(str(path.name))

        # Skip files that are not something we can handle (ai.xml)
        if not searched:
            continue
        # Filter out items that are not part of a dependency package
        elif os.path.dirname(relative_path).replace(os.sep, "_").strip("_") not in args.deps:
            continue
        try:
            parser_function = PARSE_ROUTE_TABLE[searched.group(1)]
        except Exception as exc:
            print(f"[ERROR] PyBind found unknown model type { searched.group(1) }", file=sys.stderr)
            sys.exit(1)
        # Parse file
        try:
            with open(path, "r") as file_handle:
                 dom = parse(file_handle)
            item = parser_function(dom)
            if item is None:
                continue
        except OSError as ose:
            print(f"[ERROR] PyBind errored reading: { path } with error { exc }", file=sys.stderr)
            sys.exit(1)
        except IndexError:
            print(f"[ERROR] PyBind errored parsing: { path }. Required tag missing, check for misspellings.", file=sys.stderr)
            sys.exit(1)
        except KeyError as ker:
            ker = str(ker)
            message = f"find symbol {ker}" if ":" in ker else f"read field {ker}"
            print(f"[ERROR] PyBind unable { message }", file=sys.stderr)
            sys.exit(1)
        except Exception as exc:
            print(f"[ERROR] PyBind errored parsing: { path } with error { exc }", file=sys.stderr)
            sys.exit(1)
        item["type"] = searched.group(1)
        item["header_path"] = relative_path.replace("Ai.xml", "Ac.hpp")
        item["output_directory"] = path.parent
        if item["ns"] not in namespaces:
            namespaces[item["ns"]] = []
        namespaces[item["ns"]].append(item)

    for template_name in ["PyBindAc.hpp.j2", "PyBindAc.cpp.j2", "fprime_pybind.py.j2"]:
        template = env.get_template(template_name)
        output = template.render(namespaces=namespaces)
        with open(f"{ template_name.replace('.j2', '') }", "w") as file_handle:
            file_handle.write(output)
    # Write out component templates
    template = env.get_template("ComponentTemplate.py.j2")
    for _, items in namespaces.items():
        for item in [item for item in items if item["type"] == "Component"]:
            output = template.render(item=item)
            output_path = item["output_directory"] / f"{ item['name'] }.py.tmpl"
            with open(output_path, "w") as file_handle:
                file_handle.write(output)


if __name__ == "__main__":
    main()
