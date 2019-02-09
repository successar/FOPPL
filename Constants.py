add = lambda x, y : x + y
sub = lambda x, y : x - y
mul = lambda x, y : x * y
div = lambda x, y : x / y
power = lambda x, y : x**y

def generate_math_constant(lbd) :
    class MathConstant() :
        def __init__(self) :
            pass

        def __call__(self, x, y) :
            return lbd(x, y)

    return MathConstant

constants = {
    '+' : generate_math_constant(add)(), 
    '-' : generate_math_constant(sub)(), 
    '*' : generate_math_constant(mul)(), 
    '/' : generate_math_constant(div)(), 
    '**' : generate_math_constant(power)()
}

from Distributions import distribution_constants

constants.update(distribution_constants)

