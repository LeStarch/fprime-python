####
# F prime CMakeLists.txt:
#
# SOURCE_FILES: combined list of source and autocoding diles
# MOD_DEPS: (optional) module dependencies
#
# Note: using PROJECT_NAME as EXECUTABLE_NAME
####
set(SOURCE_FILES
  "${CMAKE_CURRENT_LIST_DIR}/PyAppTopologyAppAi.xml"
  "${CMAKE_CURRENT_LIST_DIR}/Topology.cpp"  
  "${CMAKE_CURRENT_LIST_DIR}/Main.cpp"  
)
# Note: supply non-explicit dependencies here
set(MOD_DEPS
    Fw/Logger
    Svc/LinuxTime
    # Communication Implementations
    Drv/Udp
    Drv/TcpClient
    pybind
)
register_fprime_executable()
#get_module_name("${CMAKE_CURRENT_LIST_DIR}")
#target_link_libraries("PyApp_exe" pybind11::embed)
