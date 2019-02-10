from AST import *
from lexer import FOPPLLexer
import ply.yacc as yacc

class FOPPLParser() :
    
    def p_statement_define(self, p):
        'statement : LPAREN DEFN VARIABLE LBRAC arguments RBRAC expression RPAREN statement'
        if p[3] in p.parser.top_environment.procedures_order :
            raise FileExistsError
        else :
            p.parser.top_environment.procedures[p[3]] = Function(name=p[3], arguments=p[5], expression=p[7])
            p.parser.top_environment.procedures_order.append(p[3])
            p[0] = p[9]

    def p_statement_expr(self, p):
        'statement : expression'
        print(p[1])
        p[0] = p[1]

    def p_arguments_expr(self, p) :
        '''arguments : arguments VARIABLE
                    | VARIABLE'''

        if len(p) == 3 :
            print(p[1])
            p[1].append(p[2])
            p[0] = p[1]
        else :
            p[0] = [p[1]]

    def p_expression_if(self, p):
        'expression : LPAREN IF expression expression expression RPAREN'
        p[0] = IfExpression(p[3], p[4], p[5])

    def p_expression_varexp(self, p):
        '''varexpre : varexpre VARIABLE expression
                    | VARIABLE expression'''
        
        if len(p) == 4 :
            p[1].append((p[2], p[3]))
            p[0] = p[1]
        else :
            p[0] = [(p[1], p[2])]

    def p_expression_letsugar(self, p) :
        'expression : LPAREN LET LBRAC varexpre RBRAC expression_list RPAREN'
        varlist = p[4]
        exprlist = p[6]
        le = exprlist[-1]
        for e in exprlist[-2::-1] :
            le = LetExpression('_', e, le)
            
        for (v, e) in varlist[-1::-1] :
            le = LetExpression(v, e, le) 

        p[0] = le

    def p_expression_fcall(self, p) :
        'expression : LPAREN VARIABLE expression_list RPAREN'
        if p[2] in p.parser.top_environment.constants :
            p[0] = ConstantCall(name=p[2], params=p[3])
        else :
            p[0] = FunctionCall(name=p[2], params=p[3])

    def p_expression_list(self, p) :
        '''expression_list : expression_list expression 
                            | expression'''

        if len(p) == 3 :
            p[1].append(p[2])
            p[0] = p[1]
        elif len(p) == 2 :
            p[0] = [p[1]]


    def p_sample(self, p) :
        'expression : LPAREN SAMPLE expression RPAREN'
        p[0] = Sample(p[3])

    def p_observe(self, p) :
        'expression : LPAREN OBSERVE expression expression RPAREN'
        p[0] = Observe(p[3], p[4])

    def p_expression_number(self, p):
        'expression : NUMBER'
        p[0] = Number(p[1])

    def p_expression_variable(self, p):
        'expression : VARIABLE'
        if p[1] in p.parser.top_environment.constants :
            raise LookupError("Symbol is constant")
        
        p[0] =  Variable(p[1])

    def p_error(self, p):
        print("Syntax error at '%s'" % p.value)

    def __init__(self):
        self.lexer = FOPPLLexer()
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self)

def parse(program) :
    top_environment = Environment()
    parser = FOPPLParser()
    parser.parser.top_environment = top_environment
    p1 = parser.parser.parse(program)
    top_environment.assign_program(p1)
    return top_environment