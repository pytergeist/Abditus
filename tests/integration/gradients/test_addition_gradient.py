import numpy as np
import pytest

from tests.integration.gradients.finite_difference import finite_difference_jacobian
from abditus.tensor import Tensor


def fn_numpy(x):
    return x + x


def compute_autodiff_gradient(x):
    x_tensor = Tensor(x, requires_grad=True)

    output = x_tensor + x_tensor

    output.backward()

    return x_tensor.grad


def test_addition_grad():
    x_test = np.random.rand(5)

    numerical_jacobian = finite_difference_jacobian(fn_numpy, x_test, epsilon=1.5e-8)
    numerical_vector_grad = np.dot(np.ones(x_test.shape), numerical_jacobian)
    analytical_grad = compute_autodiff_gradient(x_test)

    np.testing.assert_allclose(
        analytical_grad,
        numerical_vector_grad,
        rtol=1e-5,
        atol=1e-7,
        err_msg="Autodiff gradient does not match numerical gradient for addition.",
    )
