import random

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

def random_expression(depth=2):
    #generates a random, valid expression
    if depth == 0:
        if random.random() < 0.5:
            return variable("x")
        else:
            return constant(random.randint(1, 9))

    op = random.choice(["+", "-", "*", "/", "maths.sin", "maths.cos"])
    if op in ["maths.sin", "maths.cos"]:
        return unary_op(op, random_expression(depth - 1))
    else:
        return binary_op(op, random_expression(depth - 1), random_expression(depth - 1))


# === Mutation Logic ===

def mutate(expr):
    #returns a mutated copy of the expression
    expr = expr.copy()

    if isinstance(expr, constant):
        # tweak value slightly
        expr.value += random.choice([-1, 1])

    elif isinstance(expr, variable):
        # sometimes wrap with maths.sin/maths.cos
        if random.random() < 0.3:
            expr = unary_op(random.choice(["maths.sin", "maths.cos"]), expr)

    elif isinstance(expr, unary_op):
        # mutate inside or change operator
        if random.random() < 0.5:
            expr.operand = mutate(expr.operand)
        else:
            expr.op = random.choice(["maths.sin", "maths.cos", "-"])

    elif isinstance(expr, binary_op):
        #mutates one of the nodes
        choice = random.choice(["left", "right", "op", "replace"])
        if choice == "left":
            expr.left = mutate(expr.left)
        elif choice == "right":
            expr.right = mutate(expr.right)
        elif choice == "op":
            expr.op = random.choice(["+", "-", "*", "/"])
        else:
            #replace a whole subtree
            expr = random_expression(depth=2)

    return expr



def generate_functions():
    functions = []
    e = random_expression(depth=2)
    print("Original:", e)
    for i in range(8):
        m = mutate(e)
        functions.append(m)
    return functions

print(generate_functions())