# registry.py
import numpy as np

from .operation import Operation


########################
# ADD
########################
def add_backward(result, a, b, grad_output):
    """C = a + b derivative wrt a = grad_output derivative wrt b = grad_output."""
    return (grad_output, grad_output)


add_op = Operation("add", lambda a, b: a.data + b.data, add_backward)


########################
# SUBTRACT
########################
def subtract_backward(result, a, b, grad_output):
    """
    c = a - b
    dc/da = +1 * grad_output
    dc/db = -1 * grad_output
    """
    return grad_output, -grad_output


subtract_op = Operation("subtract", lambda a, b: a.data - b.data, subtract_backward)


########################
# RIGHT-SUBTRACT
########################
def right_subtract_backward(result, a, b, grad_output):
    """
    c = b - a
    => derivative wrt 'a' = -grad_output
       derivative wrt 'b' = +grad_output
    (assuming parents are (a, b) in that order)
    """
    return (-grad_output, grad_output)


right_subtract_op = Operation(
    "right_subtract", lambda a, b: b.data - a.data, right_subtract_backward
)


########################
# DIVIDE
########################
def divide_backward(result, a, b, grad_output):
    grad_a = grad_output / b.value
    grad_b = -grad_output * a.value / (b.value**2)
    return (grad_a, grad_b)


divide_op = Operation("divide", lambda a, b: a.data / b.data, divide_backward)


def matmul_backward(
    result, a, b, grad_output
):  # TODO: Should there be switching between dot/matmul for 1d/2d arrays?
    """
    Matrix multiply forward: result = a.data @ b.data

    grad_output has the same shape as result.

    - grad wrt a = grad_output @ b^T
    - grad wrt b = a^T @ grad_output
    """
    A = a.value
    B = b.value
    dZ = grad_output

    grad_a = dZ @ B.T
    grad_b = A.T @ dZ
    return grad_a, grad_b


matmul_op = Operation(
    "matmul",
    lambda a, b: a.data @ b.data,  # forward pass
    matmul_backward,  # backward pass
)


def sum_backward(result, a, grad_output):
    """
    Backward pass:
      result = sum(a)

    If 'result' is a scalar, 'grad_output' is also scalar (or shape () in NumPy).
    The gradient wrt 'a' is just grad_output * ones_like(a.value).
    """
    grad_a = grad_output * np.ones_like(a.value)
    return (grad_a,)


sum_op = Operation(
    op_name="sum", forward_func=lambda a: np.sum(a.data), backward_func=sum_backward
)


def maximum_backward(result, a, b, grad_output):
    """
    result = np.maximum(a.value, b.value)
    We take a subgradient approach:
      grad wrt a = grad_output if a.value >= b.value, else 0
      grad wrt b = grad_output if b.value >  a.value, else 0
    (Ties are broken to favor 'a' in this version.)
    """
    grad_a = grad_output * (a.value >= b.value)
    grad_b = grad_output * (b.value > a.value)
    return (grad_a, grad_b)


maximum_op = Operation(
    op_name="maximum",
    forward_func=lambda a, b: np.maximum(a.data, b.data),
    backward_func=maximum_backward,
)


def transpose_backward(result, a, grad_output):
    """
    For a transpose operation, the backward pass simply transposes the gradient.
    Since the forward pass is: result = transpose(a.data),
    the derivative wrt 'a' is simply: transpose(grad_output).
    """
    return (np.transpose(grad_output),)


transpose_op = Operation(
    op_name="transpose",
    forward_func=lambda a: np.transpose(a.data),
    backward_func=transpose_backward,
)
