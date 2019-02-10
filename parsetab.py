
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'DEFN IF LBRAC LET LPAREN NUMBER OBSERVE RBRAC RPAREN SAMPLE VARIABLEstatement : LPAREN DEFN VARIABLE LBRAC arguments RBRAC expression RPAREN statementstatement : expressionarguments : arguments VARIABLE\n                    | VARIABLEexpression : LPAREN IF expression expression expression RPARENvarexpre : varexpre VARIABLE expression\n                    | VARIABLE expressionexpression : LPAREN LET LBRAC varexpre RBRAC expression RPARENexpression : LPAREN VARIABLE expression_list RPARENexpression_list : expression_list expression \n                            | expressionexpression : LPAREN SAMPLE expression RPARENexpression : LPAREN OBSERVE expression expression RPARENexpression : NUMBERexpression : VARIABLE'
    
_lr_action_items = {'LPAREN':([0,3,5,7,8,10,11,14,15,16,19,21,22,23,25,26,31,32,34,36,37,41,42,],[2,-15,-14,13,13,13,13,13,-11,13,13,-9,-10,13,13,-12,13,13,-13,13,-5,-8,2,]),'NUMBER':([0,3,5,7,8,10,11,14,15,16,19,21,22,23,25,26,31,32,34,36,37,41,42,],[5,-15,-14,5,5,5,5,5,-11,5,5,-9,-10,5,5,-12,5,5,-13,5,-5,-8,5,]),'VARIABLE':([0,2,3,5,6,7,8,10,11,13,14,15,16,17,19,20,21,22,23,24,25,26,28,29,31,32,33,34,35,36,37,39,41,42,],[3,7,-15,-14,12,3,3,3,3,7,3,-11,3,25,3,28,-9,-10,3,32,3,-12,-4,35,3,3,-7,-13,-3,3,-5,-6,-8,3,]),'$end':([1,3,4,5,21,26,34,37,41,43,],[0,-15,-2,-14,-9,-12,-13,-5,-8,-1,]),'DEFN':([2,],[6,]),'IF':([2,13,],[8,8,]),'LET':([2,13,],[9,9,]),'SAMPLE':([2,13,],[10,10,]),'OBSERVE':([2,13,],[11,11,]),'RPAREN':([3,5,14,15,18,21,22,26,27,30,34,37,38,40,41,],[-15,-14,21,-11,26,-9,-10,-12,34,37,-13,-5,41,42,-8,]),'RBRAC':([3,5,21,24,26,28,29,33,34,35,37,39,41,],[-15,-14,-9,31,-12,-4,36,-7,-13,-3,-5,-6,-8,]),'LBRAC':([9,12,],[17,20,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'statement':([0,42,],[1,43,]),'expression':([0,7,8,10,11,14,16,19,23,25,31,32,36,42,],[4,15,16,18,19,22,23,27,30,33,38,39,40,4,]),'expression_list':([7,],[14,]),'varexpre':([17,],[24,]),'arguments':([20,],[29,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> statement","S'",1,None,None,None),
  ('statement -> LPAREN DEFN VARIABLE LBRAC arguments RBRAC expression RPAREN statement','statement',9,'p_statement_define','parser.py',8),
  ('statement -> expression','statement',1,'p_statement_expr','parser.py',17),
  ('arguments -> arguments VARIABLE','arguments',2,'p_arguments_expr','parser.py',22),
  ('arguments -> VARIABLE','arguments',1,'p_arguments_expr','parser.py',23),
  ('expression -> LPAREN IF expression expression expression RPAREN','expression',6,'p_expression_if','parser.py',33),
  ('varexpre -> varexpre VARIABLE expression','varexpre',3,'p_expression_varexp','parser.py',37),
  ('varexpre -> VARIABLE expression','varexpre',2,'p_expression_varexp','parser.py',38),
  ('expression -> LPAREN LET LBRAC varexpre RBRAC expression RPAREN','expression',7,'p_expression_letsugar','parser.py',47),
  ('expression -> LPAREN VARIABLE expression_list RPAREN','expression',4,'p_expression_fcall','parser.py',56),
  ('expression_list -> expression_list expression','expression_list',2,'p_expression_list','parser.py',63),
  ('expression_list -> expression','expression_list',1,'p_expression_list','parser.py',64),
  ('expression -> LPAREN SAMPLE expression RPAREN','expression',4,'p_sample','parser.py',74),
  ('expression -> LPAREN OBSERVE expression expression RPAREN','expression',5,'p_observe','parser.py',78),
  ('expression -> NUMBER','expression',1,'p_expression_number','parser.py',82),
  ('expression -> VARIABLE','expression',1,'p_expression_variable','parser.py',86),
]
