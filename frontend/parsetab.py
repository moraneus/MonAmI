
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftORIMPLIESleftANDrightNOTAND OR IMPLIES NOT BEFORE OVERLAPS INCLUDES EXIST COMMA DOT SAME LPAREN RPAREN NAME NUMBER STRINGformula : formula AND formulaformula : formula OR formulaformula : formula IMPLIES formulaformula : NOT formulaformula : NAME BEFORE NAMEformula : NAME OVERLAPS NAMEformula : NAME INCLUDES NAMEformula : NAME LPAREN data RPARENformula : SAME LPAREN NAME COMMA NAME RPARENformula : EXIST names DOT formulaformula : LPAREN formula RPARENdata : NUMBERdata : STRINGnames : NAMEnames : names COMMA NAME'
    
_lr_action_items = {'NOT':([0,2,4,7,8,9,30,],[2,2,2,2,2,2,2,]),'NAME':([0,2,4,6,7,8,9,11,12,13,16,30,31,33,],[3,3,3,18,3,3,3,22,23,24,29,3,35,36,]),'SAME':([0,2,4,7,8,9,30,],[5,5,5,5,5,5,5,]),'EXIST':([0,2,4,7,8,9,30,],[6,6,6,6,6,6,6,]),'LPAREN':([0,2,3,4,5,7,8,9,30,],[4,4,14,4,16,4,4,4,4,]),'$end':([1,10,19,20,21,22,23,24,28,32,34,37,],[0,-4,-1,-2,-3,-5,-6,-7,-11,-8,-10,-9,]),'AND':([1,10,15,19,20,21,22,23,24,28,32,34,37,],[7,-4,7,-1,7,7,-5,-6,-7,-11,-8,7,-9,]),'OR':([1,10,15,19,20,21,22,23,24,28,32,34,37,],[8,-4,8,-1,-2,-3,-5,-6,-7,-11,-8,8,-9,]),'IMPLIES':([1,10,15,19,20,21,22,23,24,28,32,34,37,],[9,-4,9,-1,-2,-3,-5,-6,-7,-11,-8,9,-9,]),'BEFORE':([3,],[11,]),'OVERLAPS':([3,],[12,]),'INCLUDES':([3,],[13,]),'RPAREN':([10,15,19,20,21,22,23,24,25,26,27,28,32,34,36,37,],[-4,28,-1,-2,-3,-5,-6,-7,32,-12,-13,-11,-8,-10,37,-9,]),'NUMBER':([14,],[26,]),'STRING':([14,],[27,]),'DOT':([17,18,35,],[30,-14,-15,]),'COMMA':([17,18,29,35,],[31,-14,33,-15,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'formula':([0,2,4,7,8,9,30,],[1,10,15,19,20,21,34,]),'names':([6,],[17,]),'data':([14,],[25,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> formula","S'",1,None,None,None),
  ('formula -> formula AND formula','formula',3,'p_formula_1','parser.py',106),
  ('formula -> formula OR formula','formula',3,'p_formula_2','parser.py',111),
  ('formula -> formula IMPLIES formula','formula',3,'p_formula_3','parser.py',116),
  ('formula -> NOT formula','formula',2,'p_formula_4','parser.py',120),
  ('formula -> NAME BEFORE NAME','formula',3,'p_formula_5','parser.py',125),
  ('formula -> NAME OVERLAPS NAME','formula',3,'p_formula_6','parser.py',130),
  ('formula -> NAME INCLUDES NAME','formula',3,'p_formula_7','parser.py',135),
  ('formula -> NAME LPAREN data RPAREN','formula',4,'p_formula_8','parser.py',139),
  ('formula -> SAME LPAREN NAME COMMA NAME RPAREN','formula',6,'p_formula_9','parser.py',144),
  ('formula -> EXIST names DOT formula','formula',4,'p_formula_10','parser.py',149),
  ('formula -> LPAREN formula RPAREN','formula',3,'p_formula_11','parser.py',154),
  ('data -> NUMBER','data',1,'p_data_1','parser.py',159),
  ('data -> STRING','data',1,'p_data_2','parser.py',164),
  ('names -> NAME','names',1,'p_names_1','parser.py',169),
  ('names -> names COMMA NAME','names',3,'p_names_2','parser.py',174),
]
