
# --------------------------------------------------------------
# return.py
#
# Example illustrating how an eval function in east AST node
# returns its result, to be used by the eval() functions
# higher up. This is the standard way to evaluate an expression
# based on an AST.
# --------------------------------------------------------------

# The AST:

class Exp:
    def eval(self):
        pass

class Plus(Exp):
    def __init__(self, exp1, exp2):
        self.exp1 = exp1
        self.exp2 = exp2

    def eval(self):
        return self.exp1.eval() + self.exp2.eval()

class Minus(Exp):
    def __init__(self, exp1, exp2):
        self.exp1 = exp1
        self.exp2 = exp2

    def eval(self):
        return self.exp1.eval() - self.exp2.eval()


class Num(Exp):
    def __init__(self, number):
        self.number = number

    def eval(self):
        return self.number

# An example expression AST corresponding to the expression (5 + 2) + (65 - 30):


exp = Plus(Plus(Num(5), Num(2)), Minus(Num(65), Num(30)))

val = exp.eval()

print(val)

'''
The variable exp above after the assignment to it denotes the AST:

          exp
       /      \
     Plus    Minus
    /   \    /   \
  Num  Num  Num Num
   5    2    65  30  

When eval() is called on exp, the top node,
it calls eval() on the sub-nodes, which again
call eval() on their sub-nodes. These calls
reach the bottom, the Num nodes, where they result in actual 
numbers, and then, as the eval() functions return
we move back up the tree. So calling eval() on
the top node actually causes the tree to be evaluated
bottom up.
'''
