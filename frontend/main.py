
# -------------------------------------------
# main.py
#
# Main program creating and parsing a formula
# -------------------------------------------

print("hello")

from parser import parser

# The input formula, formula on page 3 bottom in paper:

formula = """
exist A, B, C .
  A("load") &
  B("boot") &
  C("boot") &
  A i B &
  A i C &
  B < C
"""

# print the formula as typed:

print(formula)

# parse the formula and store AST in tree:

tree = parser.parse(formula)

# print back the tree:

print(tree)

# print the tree as an AST so one can see the internal structure:

print(repr(tree))
