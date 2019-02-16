add = lambda x, y : x + y
sub = lambda x, y : x - y
mul = lambda x, y : x * y
div = lambda x, y : x / y
power = lambda x, y : x**y

from copy import deepcopy

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

bool_constants = {
    'and' : lambda x, y : x and y,
    'or' : lambda x, y : x or y,
    'not' : lambda x : not x
}

constants.update(bool_constants)

def vector(*params) :
    return list(params)

def last(vec) :
    return vec[-1]

def first(vec) :
    return vec[0]

def append(vec_1, vec_2) :
    return deepcopy(vec_1) + deepcopy(vec_2)

def get(e1, e2) :
    if type(e1) == list :
        return e1[int(e2)]
    return e1[e2]

def put(e1, e2, e3) :
    e1_1 = deepcopy(e1)
    e1_1[e2] = e3
    return e1_1

def remove(e1, e2) :
    e1_1 = deepcopy(e1)
    del e1_1[e2]
    return e1_1
    
constants.update({
    'vector' : vector,
    'last' : last,
    'first' : first,
    'append' : append,
    'get' : get,
    'put' : put,
    'remove' : remove
})

from Distributions import distribution_constants

constants.update(distribution_constants)

