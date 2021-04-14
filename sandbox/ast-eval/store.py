
# --------------------------------------------------------------
# return.py
#
# Example illustrating how an eval function in east AST node
# stores its result, to be used by the eval() functions
# higher up. This could perhaps be necessary if this value
# is reused or it is expensive to return values. However,
# if data are represented by references (pointers) it could be
# ok to just return values as in return.py.
# --------------------------------------------------------------

# The AST:

class Exp:
    def eval(self):
        pass
    value: int

class Plus(Exp):
    def __init__(self, exp1, exp2):
        self.exp1 = exp1
        self.exp2 = exp2
        self.value = 0

    def eval(self):
        self.exp1.eval()
        self.exp2.eval()
        self.value = self.exp1.value + self.exp2.value

class Minus(Exp):
    def __init__(self, exp1, exp2):
        self.exp1 = exp1
        self.exp2 = exp2
        self.value = 0

    def eval(self):
        self.exp1.eval()
        self.exp2.eval()
        self.value = self.exp1.value - self.exp2.value

class Num(Exp):
    def __init__(self, number):
        self.value = number

    def eval(self):
      pass

# An example expression AST corresponding to the expression (5 + 2) + (65 - 30):


exp = Plus(Plus(Num(5), Num(2)), Minus(Num(65), Num(30)))

exp.eval()
val = exp.value

print(val)


