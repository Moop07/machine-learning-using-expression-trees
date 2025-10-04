import random
import math as maths

# === Expression node Classes ===

class node:
    def copy(self):
        raise NotImplementedError


class constant(node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)

    def copy(self):
        return constant(self.value)


class variable(node):
    def __init__(self, name="x"):
        self.name = name

    def __repr__(self):
        return self.name

    def copy(self):
        return variable(self.name)


class unary_op(node):
    def __init__(self, op, operand):
        self.op = op  # e.g. 'maths.sin', 'maths.cos', '-'
        self.operand = operand

    def __repr__(self):
        return f"{self.op}({self.operand})"

    def copy(self):
        return unary_op(self.op, self.operand.copy())


class binary_op(node):
    def __init__(self, op, left, right):
        self.op = op  # '+', '-', '*', '/'
        self.left = left 
        self.right = right

    def __repr__(self):
        return f"({self.left} {self.op} {self.right})"

    def copy(self):
        return binary_op(self.op, self.left.copy(), self.right.copy())


# === Expression Generation ===

def simplify(expr):
    """Simplify an expression tree on the fly."""
    if isinstance(expr, constant) or isinstance(expr, variable):
        return expr

    elif isinstance(expr, unary_op):
        operand = simplify(expr.operand)
        # Simplify if operand is a constant
        if isinstance(operand, constant):
            try:
                if expr.op == "maths.sin":
                    return constant(maths.sin(operand.value))
                elif expr.op == "maths.cos":
                    return constant(maths.cos(operand.value))
                elif expr.op == "-":
                    return constant(-operand.value)
            except Exception:
                pass
        return unary_op(expr.op, operand)

    elif isinstance(expr, binary_op):
        left = simplify(expr.left)
        right = simplify(expr.right)

        # If both sides are constants, evaluate immediately
        if isinstance(left, constant) and isinstance(right, constant):
            try:
                if expr.op == "+":
                    return constant(left.value + right.value)
                elif expr.op == "-":
                    return constant(left.value - right.value)
                elif expr.op == "*":
                    return constant(left.value * right.value)
                elif expr.op == "/":
                    if right.value != 0:
                        return constant(left.value / right.value)
                    else:
                        return constant(0)
            except Exception:
                pass

        # Algebraic simplifications
        if expr.op == "+":
            if isinstance(left, constant) and left.value == 0:
                return right
            if isinstance(right, constant) and right.value == 0:
                return left
        elif expr.op == "-":
            if isinstance(right, constant) and right.value == 0:
                return left
        elif expr.op == "*":
            if isinstance(left, constant):
                if left.value == 0: return constant(0)
                if left.value == 1: return right
            if isinstance(right, constant):
                if right.value == 0: return constant(0)
                if right.value == 1: return left
        elif expr.op == "/":
            if isinstance(right, constant):
                if right.value == 1: return left
                if right.value == 0: return constant(0)

        return binary_op(expr.op, left, right)

    return expr


def random_expression(depth=2):
    #generates a random, valid expression
    if depth == 0:
        if random.random() < 0.5:
            return variable("x")
        else:
            return constant(random.randint(1, 9))

    op = random.choice(["+", "-", "*", "/", "maths.sin", "maths.cos"])
    if op in ["maths.sin", "maths.cos"]:
        expr = unary_op(op, random_expression(depth - 1))
    else:
        expr = binary_op(op, random_expression(depth - 1), random_expression(depth - 1))
    return simplify(expr)


def mutate(expr):
    """Return a mutated copy of expr, possibly adding or scaling by a random constant."""
    expr = expr.copy()

    # --- Global mutation: add or multiply by a constant term ---
    r = random.random()
    if r < 0.15:
        # 15% chance to add a random constant
        const_val = random.randint(-3, 3)
        if const_val != 0:
            return simplify(binary_op("+", expr, constant(const_val)))
    elif r < 0.3:
        # 15% chance to multiply by a random constant
        const_val = random.randint(-3, 3)
        if const_val not in [0, 1, -1]:
            return simplify(binary_op("*", constant(const_val), expr))

    # --- Local mutations depending on node type ---
    if isinstance(expr, constant):
        # tweak value slightly
        expr.value += random.choice([-1, 1])

    elif isinstance(expr, variable):
        # sometimes wrap variable in unary op
        if random.random() < 0.3:
            expr = unary_op(random.choice(["maths.sin", "maths.cos"]), expr)

    elif isinstance(expr, unary_op):
        # mutate operand or change operator
        if random.random() < 0.5:
            expr.operand = mutate(expr.operand)
        else:
            expr.op = random.choice(["maths.sin", "maths.cos", "-"])

    elif isinstance(expr, binary_op):
        # mutate one branch, operator, or replace subtree
        choice = random.choice(["left", "right", "op", "replace"])
        if choice == "left":
            expr.left = mutate(expr.left)
        elif choice == "right":
            expr.right = mutate(expr.right)
        elif choice == "op":
            expr.op = random.choice(["+", "-", "*", "/"])
        else:
            expr = random_expression(depth=3)

    return simplify(expr)




def generate_functions(num):
    functions = []
    e = random_expression(depth = 2)
    print("Original:", e)
    for i in range(num):
        m = mutate(e)
        functions.append(m)
    return functions

def mutate_functions(functions):
    mutated_functions = []
    for f in functions:
        for i in range(10):
            mutated_functions.append(mutate(f))
        #mutated_functions.append(random_expression(4))
    return mutated_functions
