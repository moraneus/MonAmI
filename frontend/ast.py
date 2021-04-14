
# --------------------------------------------------------------
# ast.py
#
# Abstract syntax (AST nodes) for the MonAmi specification logic
# --------------------------------------------------------------
from typing import Set


def error(msg : str):
    print(f'*** Error - {msg}')


class Formula:
    def free_vars(self) -> Set[str]:
        pass

    def is_well_formed(self) -> bool:
        free = self.free_vars()
        if free == set():
            return True
        else:
            error(f'the formula has free variables: {free}')
            return False


class And(Formula):
    def __init__(self, formula1, formula2):
        self.formula1 = formula1
        self.formula2 = formula2

    def __str__(self):
        return f'{self.formula1} & {self.formula2}'

    def __repr__(self):
        return f'And({repr(self.formula1)},{repr(self.formula2)})'

    def free_vars(self) -> Set[str]:
        return self.formula1.free_vars() | self.formula2.free_vars()


class Or(Formula):
    def __init__(self, formula1, formula2):
        self.formula1 = formula1
        self.formula2 = formula2

    def __str__(self):
        return f'{self.formula1} | {self.formula2}'

    def __repr__(self):
        return f'Or({repr(self.formula1)},{repr(self.formula2)})'

    def free_vars(self) -> Set[str]:
        return self.formula1.free_vars() | self.formula2.free_vars()


class Implies(Formula):
    def __init__(self, formula1, formula2):
        self.formula1 = formula1
        self.formula2 = formula2

    def __str__(self):
        return f'{self.formula1} -> {self.formula2}'

    def __repr__(self):
        return f'Implies({repr(self.formula1)},{repr(self.formula2)})'

    def free_vars(self) -> Set[str]:
        return self.formula1.free_vars() | self.formula2.free_vars()


class Not(Formula):
    def __init__(self, formula):
        self.formula = formula

    def __str__(self):
        return f'! {self.formula}'

    def __repr__(self):
        return f'Not({repr(self.formula)})'

    def free_vars(self) -> Set[str]:
        return self.formula.free_vars()


class Before(Formula):
    def __init__(self, interval1, interval2):
        self.interval1 = interval1
        self.interval2 = interval2

    def __str__(self):
        return f'{self.interval1} < {self.interval2}'

    def __repr__(self):
        return f'Before({self.interval1},{self.interval2})'

    def free_vars(self) -> Set[str]:
        return {self.interval1, self.interval2}


class Overlaps(Formula):
    def __init__(self, interval1, interval2):
        self.interval1 = interval1
        self.interval2 = interval2

    def __str__(self):
        return f'{self.interval1} o {self.interval2}'

    def __repr__(self):
        return f'Overlaps({self.interval1},{self.interval2})'

    def free_vars(self) -> Set[str]:
        return {self.interval1, self.interval2}


class Includes(Formula):
    def __init__(self, interval1, interval2):
        self.interval1 = interval1
        self.interval2 = interval2

    def __str__(self):
        return f'{self.interval1} i {self.interval2}'

    def __repr__(self):
        return f'Includes({self.interval1},{self.interval2})'

    def free_vars(self) -> Set[str]:
        return {self.interval1, self.interval2}


class Data(Formula):
    def __init__(self, interval, data):
        self.interval = interval
        self.data = data

    def __str__(self):
        return f'{self.interval}({self.data})'

    def __repr__(self):
        return f'Data({self.interval},{self.data})'

    def free_vars(self) -> Set[str]:
        return {self.interval}


class Same(Formula):
    def __init__(self, interval1, interval2):
        self.interval1 = interval1
        self.interval2 = interval2

    def __str__(self):
        return f'same({self.interval1},{self.interval2})'

    def __repr__(self):
        return f'Same({self.interval1},{self.interval2})'

    def free_vars(self) -> Set[str]:
        return {self.interval1, self.interval2}


class Exist(Formula):
    def __init__(self, intervals, formula):
        self.intervals = intervals
        self.formula = formula

    def __str__(self):
        return f'exist {self.intervals} . {self.formula}'

    def __repr__(self):
        return f'Exist({self.intervals},{repr(self.formula)})'

    def free_vars(self) -> Set[str]:
        return self.formula.free_vars() - set(self.intervals)


class Paren(Formula):
    def __init__(self, formula):
        self.formula = formula

    def __str__(self):
        return f'({self.formula})'

    def __repr__(self):
        return f'Paren({repr(self.formula)})'

    def free_vars(self) -> Set[str]:
        return self.formula.free_vars()
