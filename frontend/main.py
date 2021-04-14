
# ------------------------------------------
# main.py
#
# Main program creating and parsing formulas
# ------------------------------------------

from parser import parse

# parse is a function with the type:
#
#   parse(formula: str) -> Formula
#
# which returns a formula (AST node) if the formula parses
# and is well formed. If not, parse returns None.

# Now we create a list of formulas and run parse on them
# in a for loop.

# The boot spec from page 3 of the paper:

boot_formula = """exist A, B, C .
  A("load") &
  B("boot") &
  C("boot") &
  A i B &
  A i C &
  B < C"""

# A list of formulas for testing, one per line:

specs = [
  boot_formula,
  'A < B & B i C & C o D',
  'exist A, B . A < B & B i C & exist D . C o D',
  'A > B & C && D',
  'exist A, B, C, D, E, F, G, H . A < B & C < D | ! E < F & G < H'
]

# Looping though specs and processing them:

for spec in specs:
    print()
    print('=========================')
    print(spec)
    print('-------------------------')
    tree = parse(spec)
    if tree is not None:
        print(f'{tree}')
        print(f'{repr(tree)}')

