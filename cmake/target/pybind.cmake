####
# pybind.cmake:
#
# A target used to make bindings for the python language. This will handle fprime data types
# enabling them for use the python layer. This will also be used to generate the interace
# mappings for the component targets.
#
# Author: mstarch
####
cmake_policy(SET CMP0079 NEW)
set(BINDING_AUTOCODER_PATH ${CMAKE_CURRENT_LIST_DIR}/../../autocode/pybind_gen.py)

# Unused function needed for target API
function(add_global_target TARGET_NAME)
    find_program(PYTHON NAMES python3 python REQUIRED)
    if (NOT PYTHON)
        message(FATAL_ERROR "Failed to find python3, cannot run python bindings")
    endif()
    string(REPLACE ";" ":" FPRIME_BUILD_LOCATIONS_SEP "${FPRIME_BUILD_LOCATIONS}")
    add_custom_command(
        COMMAND ${CMAKE_COMMAND} -E chdir ${CMAKE_BINARY_DIR}
        ${CMAKE_COMMAND} -E env
            PYTHONPATH="${FPRIME_FRAMEWORK_PATH}/Autocoders/Python/src"
            BUILD_ROOT="${FPRIME_BUILD_LOCATIONS_SEP}"
	    ${PYTHON} ${BINDING_AUTOCODER_PATH} $<TARGET_PROPERTY:${TARGET_NAME},PYTHON_BINDINGS>
        OUTPUT ${CMAKE_BINARY_DIR}/PyBindAc.hpp ${CMAKE_BINARY_DIR}/PyBindAc.cpp COMMAND_EXPAND_LISTS
    )
    add_library(${TARGET_NAME} ${CMAKE_BINARY_DIR}/PyBindAc.cpp)
    set_property(TARGET ${TARGET_NAME} PROPERTY PYTHON_BINDINGS)
    set_property(TARGET ${TARGET_NAME} PROPERTY PYTHON_INSTALLS ${CMAKE_BINARY_DIR}/fprime_pybind.py)
    add_dependencies(${TARGET_NAME} fprime-python_FprimePy)
    target_link_libraries(${TARGET_NAME} PUBLIC fprime-python_FprimePy)
    set_source_files_properties(${CMAKE_BINARY_DIR}/PyBindAc.cpp PROPERTIES GENERATED TRUE)
    set_source_files_properties(${CMAKE_BINARY_DIR}/PyBindAc.hpp PROPERTIES GENERATED TRUE)

    add_custom_target(pybind_package_gen COMMAND ${CMAKE_COMMAND} -E make_directory ${FPRIME_INSTALL_DEST}/python
                      COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_PROPERTY:${TARGET_NAME},PYTHON_INSTALLS> ${FPRIME_INSTALL_DEST}/python
                      DEPENDS $<TARGET_PROPERTY:${TARGET_NAME},PYTHON_INSTALLS> COMMAND_EXPAND_LISTS)
endfunction(add_global_target)

function(register_python_component AI_XML PY_IMPL)
    get_module_name("${CMAKE_CURRENT_LIST_DIR}") # Get the current target
    add_dependencies(${MODULE_NAME} fprime-python_FprimePy)

    set_property(TARGET pybind APPEND PROPERTY PYTHON_BINDINGS ${AI_XML})
    set_property(TARGET pybind APPEND PROPERTY PYTHON_INSTALLS ${PY_IMPL})

    add_dependencies(pybind ${MODULE_NAME})
    target_link_libraries(pybind PUBLIC ${MODULE_NAME})
endfunction(register_python_component)

function(add_module_target MODULE_NAME TARGET_NAME GLOBAL_TARGET_NAME AC_INPUTS SOURCE_FILES AC_OUTPUTS MOD_DEPS)
    # Try to generate dictionaries for every AC input file
    foreach (AC_IN IN LISTS AC_INPUTS)
        # Only generate dictionaries on serializables or topologies
        if (AC_IN MATCHES ".*(Array)|(Serializable)|(Enum)Ai.xml$")
            set_property(TARGET ${GLOBAL_TARGET_NAME} APPEND PROPERTY PYTHON_BINDINGS ${AC_IN})
	    add_dependencies(${GLOBAL_TARGET_NAME} ${MODULE_NAME})
        endif()
    endforeach()
endfunction(add_module_target)



