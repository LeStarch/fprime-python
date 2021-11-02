# fprime-python: F´ to Python Bindings

Once in a great blue moon, an fprime developer will find themselves in a bind: call into python code, or incur the
cost of translating that code into C++ before such code can be used. Since Python code typically represents prototype
code it is incredibly helpful to call it directly and defer the translation cost until after the project has left the
prototype phase.

This package allows F´ running as a C++ binary to call into F´ components defined in Python. These components implement
the functionality of F´ components while maintaining access to the Python environment itself.

**Acknowledgements:** [`pybind11`](https://github.com/pybind/pybind11) library helps quite a bit!  The Python C API is
verbose and this library reduces that  complexity. 

**WARNING: THIS IS DEEPLY EXPERIMENTAL CODE, NO SUPPORT, NOR GUARANTEE IS PROVIDED.**

**WARNING: SUPPORT IS ONLY AVAILABLE FOR F´ 2.x.x VERSIONS**

## Installation and Setup

In order to use `fprime-python` download the source code, or add it as a Git submodule.  Once finished, make sure to
pull int `pybind11` by running `git submodule update --init` in the `fprime-python` checkout.

Next, add the path to the download in the `library_locations` list set in settings.ini for a deployment. If
`fprime-python` is checked out parallel to the deployment directory then the following will work:

```ini
library_locations: ../fprime-python
```

## Setting a Component Up With Python Bindings

In order to write a component in python, the component Ai.xml file and the Python implementation file must be registered
with the system. Add a call to `register_python_component(ai xml path, python file path)` to your CMakeLists.txt. This
must be done **after** the call to `register_fprime_module` which registers the component with F´´. For example:

```cmake
register_fprime_module()
...
register_python_component("${CMAKE_CURRENT_LIST_DIR}/SignalGenComponentAi.xml" "${CMAKE_CURRENT_LIST_DIR}/SignalGen.py")
```

Once finished, the python bindings will be autocoded and included in the next build (assuming the deployment is setup 
as shown below). This will also produce a `<component>.py.tmpl` file in the component folder as a basic template for
implementing components in python.

## Complex Data Types (Serializables, Arrays, Enums)

Other types are automatically supplied by the bindings autocoder, however; only types referenced in a component's model
(AI XML file) will be included. To use these types, reference:

```python
import <namespace>

var = <namespace>.typename()
```

Since these types are C++ class wrappers, one must be as pedantic when using them as one is in C++. It is best to
convert in/out of python data types close to the component interface and proceed with native python. An instructive
example with F´ types can be seen in the SignalGen reimplementation example found here:
[https://github.com/LeStarch/fprime-python-examples.git](https://github.com/LeStarch/fprime-python-examples.git)

## Deployments and Topologies

Deployments are required to add a few items to their `CMakeLists.txt` to properly pull in the `fprime-python` autocoder
and support code.  Take a note, the call to `register_fprime_target` must occur after the `FPrime.cmake` include call
and before the `FPrime-Code.cmake` include call.

```cmake
include("${FPRIME_FRAMEWORK_PATH}/cmake/FPrime.cmake")
register_fprime_target("<path to fprime-python>/cmake/target/pybind.cmake")

# NOTE: register custom targets between these two lines
include("${FPRIME_FRAMEWORK_PATH}/cmake/FPrime-Code.cmake")
include("<path to fprime-python>/fprime-python.cmake")
...
...
```

In addition, the user should add the following code to their `Main.cpp` file before calling F´ construction functions:

```c++
#include <fprime-python/FprimePy/FprimePy.hpp>

int main(int argc, char* argv[]) {
    FprimePy::initialize();
}
```

## A Working Example

A working example of SignalGen with a number of different types, commands, channels, events,
and schedule ports is available here:
[https://github.com/LeStarch/fprime-python-examples.git](https://github.com/LeStarch/fprime-python-examples.git)


Enjoy!

## Idiosyncrasies

These are known missing features:

1. Parameter definitions are not supported
2. Extensive testing has not been done