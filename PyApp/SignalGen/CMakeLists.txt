####
# F prime CMakeLists.txt:
#
# SOURCE_FILES: combined list of source and autocoding diles
# MOD_DEPS: (optional) module dependencies
#
####
set(SOURCE_FILES
  "${CMAKE_CURRENT_LIST_DIR}/SignalTypeEnumAi.xml"
  "${CMAKE_CURRENT_LIST_DIR}/SignalSetArrayAi.xml"
  "${CMAKE_CURRENT_LIST_DIR}/SignalPairSerializableAi.xml"
  "${CMAKE_CURRENT_LIST_DIR}/SignalPairSetArrayAi.xml"
  "${CMAKE_CURRENT_LIST_DIR}/SignalInfoSerializableAi.xml"
  "${CMAKE_CURRENT_LIST_DIR}/SignalGenComponentAi.xml"
  #"${CMAKE_CURRENT_LIST_DIR}/PyAppPyBind.cpp"
  #"${CMAKE_CURRENT_LIST_DIR}/SignalGen.cpp"
)
set(MOD_DEPS
    fprime-python/FprimePy
)
register_fprime_module()
register_python_component("${CMAKE_CURRENT_LIST_DIR}/SignalGenComponentAi.xml" "${CMAKE_CURRENT_LIST_DIR}/SignalGen.py")
#get_module_name("${CMAKE_CURRENT_LIST_DIR}")
#target_link_libraries("${MODULE_NAME}" pybind11::embed pybind11::module)

#target_compile_options(${MODULE_NAME} PUBLIC -I/usr/include/python3.8 -I/usr/include/python3.8  -Wno-unused-result -Wsign-compare -g -fdebug-prefix-map=/build/python3.8-CoVRmP/python3.8-3.8.10=. -specs=/usr/share/dpkg/no-pie-compile.specs -fstack-protector -Wformat -Werror=format-security  -DNDEBUG -g -fwrapv -O3 -Wall -fPIE)
#
#        -I/Library/Frameworks/Python.framework/Versions/3.8/include/python3.8
#        -I/Library/Frameworks/Python.framework/Versions/3.8/include/python3.8
#        -Wno-unused-result -Wsign-compare -Wunreachable-code -fno-common -dynamic -DNDEBUG -g
#        -fwrapv -O3 -Wall -arch x86_64 -g)
#target_link_libraries(${MODULE_NAME} -L/usr/lib/python3.8/config-3.8-x86_64-linux-gnu -L/usr/lib -lpython3.8 -lcrypt -lpthread -ldl  -lutil -lm -lm )
#        -L/Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/config-3.8-darwin
#        -ldl -framework CoreFoundation)

### UTs ###
#set(UT_SOURCE_FILES
#  "${CMAKE_CURRENT_LIST_DIR}/SignalGenComponentAi.xml"
#  "${CMAKE_CURRENT_LIST_DIR}/test/ut/Tester.cpp"
#  "${CMAKE_CURRENT_LIST_DIR}/test/ut/TestMain.cpp"
#)
#register_fprime_ut()
