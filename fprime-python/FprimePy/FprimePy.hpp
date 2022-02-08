//
// Created by mstarch on 9/14/21.
//

#ifndef PYAPP_PYINIT_HPP
#define PYAPP_PYINIT_HPP

#include "pybind11/pybind11.h"
#include "pybind11/embed.h"
namespace py = pybind11;


namespace FprimePy {

class FprimePython {
  public:
    FprimePython();
    void initialize();
    void deinitalize();
    ~FprimePython();

  private:
    py::gil_scoped_release* m_releaser;
};
}
#endif  // PYAPP_PYINIT_HPP
