#include "../core/tensor.h"
#include <pybind11/numpy.h> // for numpy array conversion
#include <pybind11/pybind11.h>
#include <pybind11/stl.h> // for automatic conversion of std::vector
#include <sstream>        // for string stream in __repr__

namespace py = pybind11;

PYBIND11_MODULE(fusion, m) {
  m.doc() = "Fusion Tensor module exposing Tensor<double>";

  // Bind Tensor<double>
  py::class_<Tensor<double>>(m, "Tensor")
      .def(py::init<const std::vector<double>, const std::vector<size_t> &>(),
           "Create a Tensor from a list of doubles.")
      .def(py::init<const double &>(),
           "Create a Tensor from a list of doubles.")
      .def("__repr__",
           [](const Tensor<double> &t) {
             std::ostringstream oss;
             oss << t;
             return oss.str();
           })
      // Add a method to convert the tensor data to a numpy array.
      .def(
          "to_numpy",
          [](const Tensor<double> &t) {
            // Allocate a numpy array of the same size as the tensor data.
            py::array_t<double> np_arr(t.arr.size());
            // Request a buffer info from the numpy array.
            auto buf = np_arr.request();
            double *ptr = static_cast<double *>(buf.ptr);
            // Copy the tensor's data into the numpy array.
            std::copy(t.arr.begin(), t.arr.end(), ptr);
            return np_arr;
          },
          "Return the tensor as a numpy array.")
      // Overload for Tensor + Tensor
      .def("__add__",
           (Tensor<double>(Tensor<double>::*)(const Tensor<double> &) const) &
               Tensor<double>::operator+,
           "Element-wise addition of two Tensors.")
      // Overload for Tensor + scalar
      .def("__add__",
           (Tensor<double>(Tensor<double>::*)(const double &) const) &
               Tensor<double>::operator+,
           "Element-wise addition of a Tensor and a scalar.")
      // Overload for Tensor - Tensor
      .def("__sub__",
           (Tensor<double>(Tensor<double>::*)(const Tensor<double> &) const) &
               Tensor<double>::operator-,
           "Element-wise subtraction of two Tensors.")
      // Overload for Tensor - scalar
      .def("__sub__",
           (Tensor<double>(Tensor<double>::*)(const double &) const) &
               Tensor<double>::operator-,
           "Element-wise subtraction of a scalar from a Tensor.")
      // Overload for Tensor * Tensor
      .def("__mul__",
           (Tensor<double>(Tensor<double>::*)(const Tensor<double> &) const) &
               Tensor<double>::operator*,
           "Element-wise multiplication of two Tensors.")
      // Overload for Tensor * scalar
      .def("__mul__",
           (Tensor<double>(Tensor<double>::*)(const double &) const) &
               Tensor<double>::operator*,
           "Element-wise multiplication of a Tensor with a scalar.")
      // Overload for Tensor / Tensor
      .def("__truediv__",
           (Tensor<double>(Tensor<double>::*)(const Tensor<double> &) const) &
               Tensor<double>::operator/,
           "Element-wise division of two Tensors.")
      // Overload for Tensor / scalar
      .def("__truediv__",
           (Tensor<double>(Tensor<double>::*)(const double &) const) &
               Tensor<double>::operator/,
           "Element-wise division of a Tensor by a scalar.");
}
