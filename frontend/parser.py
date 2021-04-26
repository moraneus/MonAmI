
# ----------------------------------------------
# frontend.py
#
# PLY frontend for the MonAmi specification logic
# ---------------------------------------------

import ply.lex as lex
import ply.yacc as yacc

from frontend.ast import *

__errors__ = False

#############
### Lexer ###
#############

tokens = (
    'AND',
    'OR',
    'IMPLIES',
    'NOT',
    'BEFORE',
    'OVERLAPS',
    'INCLUDES',
    'EXIST',
    'FORALL',
    'COMMA',
    'DOT',
    'SAME',
    'LPAREN',
    'RPAREN',
    'NAME',
    'NUMBER',
    'STRING'
)

RESERVED = {
    "o": 'OVERLAPS',
    "i": 'INCLUDES',
    "exist": 'EXIST',
    "forall": 'FORALL',
    "same": 'SAME'
}

t_AND = r'\&'
t_OR = r'\|'
t_IMPLIES = r'->'
t_NOT = r'!'
t_BEFORE = r'\<'
t_COMMA = r','
t_DOT = r'\.'
t_LPAREN = r'\('
t_RPAREN = r'\)'


def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_\.]*'
    t.type = RESERVED.get(t.value, "NAME")
    return t


def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t


t_STRING = r'\"([^\\\n]|(\\.))*?\"'

t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def find_column(input,token):
    i = token.lexpos
    while i > 0:
        if input[i] == '\n': break
        i -= 1
    column = (token.lexpos - i)+1
    return column


def t_error(t):
    global __errors__
    __errors__ = True
    lexpos = find_column(t.lexer.lexdata,t)
    print(f"lexer error, illegal character '{t.value[0]}', line '{t.lineno}', pos '{lexpos}'")
    t.lexer.skip(1)


lex.lex()

##############
### Parser ###
##############


def p_formula_1(p):
    "formula : formula AND formula"
    p[0] = And(p[1], p[3])


def p_formula_2(p):
    "formula : formula OR formula"
    p[0] = Or(p[1], p[3])


def p_formula_3(p):
    "formula : formula IMPLIES formula"
    p[0] = Implies(p[1], p[3])


def p_formula_4(p):
    "formula : NOT formula"
    p[0] = Not(p[2])


def p_formula_5(p):
    "formula : NAME BEFORE NAME"
    p[0] = Before(p[1], p[3])


def p_formula_6(p):
    "formula : NAME OVERLAPS NAME"
    p[0] = Overlaps(p[1], p[3])


def p_formula_7(p):
    "formula : NAME INCLUDES NAME"
    p[0] = Includes(p[1], p[3])


def p_formula_8(p):
    "formula : NAME LPAREN data RPAREN"
    p[0] = Data(p[1], p[3])


def p_formula_9(p):
    "formula : SAME LPAREN NAME COMMA NAME RPAREN"
    p[0] = Same(p[3], p[5])


def p_formula_10(p):
    "formula : EXIST names DOT formula"
    p[0] = Exist(p[2], p[4])


def p_formula_11(p):
    "formula : FORALL names DOT formula"
    p[0] = Not(Exist(p[2], Not(p[4])))


def p_formula_12(p):
    "formula : LPAREN formula RPAREN"
    p[0] = Paren(p[2])


def p_data_1(p):
    "data : NUMBER"
    p[0] = p[1]


def p_data_2(p):
    "data : STRING"
    p[0] = p[1]


def p_names_1(p):
    "names : NAME"
    p[0] = [p[1]]


def p_names_2(p):
    "names : names COMMA NAME"
    p[0] = p[1] + [p[3]]


precedence = (
    ('left', 'OR', 'IMPLIES'),
    ('left', 'AND'),
    ('right', 'NOT')
)

def p_error(p):
    global __errors__
    __errors__ = True
    if p:
        print(f"Syntax error at '{p.value}' in line '{p.lineno}'")
    else:
        print("Syntax error at EOF")


parser = yacc.yacc()


def parse(formula: str) -> Formula:
    global __errors__
    __errors__ = False
    tree = parser.parse(formula)
    if __errors__:
        error(f'syntax error!')
        return None
    else:
        if tree.is_well_formed():
            return tree
        else:
            error(f'formula parses but is not well formed!')
            return None

