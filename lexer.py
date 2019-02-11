import ply.lex as lex

class FOPPLLexer() :
    reserved = {
        'defn' : 'DEFN',
        'sample' : 'SAMPLE',
        'observe' : 'OBSERVE',
        'let' : 'LET',
        'if' : 'IF'
    }

    tokens = ['LPAREN','RPAREN', 'LBRAC', 'RBRAC', 'NUMBER', 'VARIABLE'] + list(reserved.values())

    # Tokens

    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'
    t_LBRAC  = r'\['
    t_RBRAC  = r'\]'

    def t_NUMBER(self, t):
        r'-?\d+(\.\d+)?'
        t.value = float(t.value)
        return t
    
    def t_VARIABLE(self, t) :
        r'([^\s\(\)\]\[\d])([^\s\(\)\]\[])*'
        t.type = self.reserved.get(t.value,'VARIABLE')
        return t

    # Ignored characters
    t_ignore = " \t"

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def __init__(self):
        # Build the lexer
        self.lexer = lex.lex(module=self)