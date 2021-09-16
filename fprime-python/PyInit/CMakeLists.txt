get_module_name("${CMAKE_CURRENT_LIST_DIR}")

add_subdirectory("${CMAKE_CURRENT_LIST_DIR}/../pybind11" pybind11)
add_library("${MODULE_NAME}" INTERFACE)
target_link_libraries(fprime-python_PyInit INTERFACE pybind11::embed)

