//
// Created by mstarch on 9/14/21.
//

#ifndef PYAPP_PYINIT_HPP
#define PYAPP_PYINIT_HPP

#include "pybind11/pybind11.h"
#include "pybind11/embed.h"
namespace py = pybind11;


namespace FprimePy {
    // Initialize the python environment
    void initialize();
    
    void destroy();
}
#endif  // PYAPP_PYINIT_HPP
