import ast
import math
import operator
from collections.abc import Callable

_BIN_OPS: dict[type, Callable[[float, float], float]] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_UNARY_OPS: dict[type, Callable[[float], float]] = {ast.USub: operator.neg, ast.UAdd: operator.pos}

_FUNCTIONS: dict[str, Callable[..., float]] = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
    "sqrt": math.sqrt,
    "log": math.log,
    "log10": math.log10,
    "exp": math.exp,
    "factorial": math.factorial,
    "floor": math.floor,
}


class CalculatorError(Exception):
    """Raised whenever an expression cannot be safely evaluated"""

    pass


def safe_eval(expression: str) -> float:
    """Evaluates the expression using a safe evaluation mechanism.
    :param expression: The expression to evaluate.
    :type expression: str
    :return: The evaluated expression.
    :rtype: float
    """
    try:
        tree = ast.parse(expression, mode="eval")
        return _eval(tree.body)
    except SyntaxError as e:
        raise CalculatorError(f"Invalid syntax in {expression}: {e}") from e


def _eval(node: ast.AST) -> float:
    """The helper function that basically breaks down the tree and evaluates the single nodes.
    :param node: The node to evaluate.
    :type node: ast.AST
    :return: The evaluated expression.
    :rtype: float
    """
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return float(node.value)
        raise CalculatorError(f"Invalid input for {node.value!r}")

    elif isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op = type(node.op)
        if op not in _BIN_OPS:
            raise CalculatorError(f"Invalid input for {type(node.op).__name__}")
        op_func = _BIN_OPS[op]
        try:
            return op_func(left, right)
        except ZeroDivisionError as e:
            raise CalculatorError("division by zero") from e

    elif isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        operation = type(node.op)
        if operation not in _UNARY_OPS:
            raise CalculatorError(f"Invalid input for {type(node.op).__name__}")
        op_function = _UNARY_OPS[operation]
        return op_function(operand)

    elif isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name):
            name = node.func.id
            if name not in _FUNCTIONS:
                raise CalculatorError(
                    f"Invalid input for {type(node.func).__name__}. "
                    f"There is no matching function named {name}"
                )
            if (len(node.keywords)) >= 1:
                raise CalculatorError("There is some extra information present.")
            evaluated_args = [_eval(arg) for arg in node.args]
            function_to_call = _FUNCTIONS[name]
            return function_to_call(*evaluated_args)
        raise CalculatorError(f"Invalid input for {type(node.func).__name__}")

    else:
        raise CalculatorError(f"Unsupported expression: {type(node).__name__}")
