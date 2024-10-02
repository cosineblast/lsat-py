
from the_types import *

import parsy as p


_ws = p.regex("\\s*")
token_string = lambda s: p.string(s) << _ws
token_regex = lambda r: p.regex(r) << _ws

_constant = token_regex("[+\\-]?\\d+(\\.\\d+)?").map(float)

_formula = p.forward_declaration()
_formula_no_op = p.forward_declaration()

_atom = token_regex("[a-z]+").map(Atomic)

def binary_function(name, constructor):
    def result():
        yield token_string(name) 
        yield token_string("(") 
        x = yield _formula 
        yield token_string(",")
        y = yield _formula 
        yield token_string(")")
        return constructor(x,y)

    return p.generate(result)

_min = binary_function("min", Min)

_max = binary_function("max", Max)

_conj = binary_function("conj", Conjunction)

_disj = binary_function("disj", Disjunction)

@p.generate
def _negation():
    yield token_string("not") 
    yield token_string("(") 
    x = yield _formula 
    yield token_string(")")
    return Negation(x)

_paren = token_string("(") >> (_formula << token_string(")"))

_formula.become(_min | _max | _conj | _disj | _paren | _negation | _atom)

_relation = token_string("==").result('eq') | token_string("<=").result('le') | token_string(">=").result('ge')

_equation = p.seq(_formula, _relation, _constant).combine(lambda f,r,c: (r,f,c))

equations = _ws >> _equation.sep_by(token_string(";"))

if __name__ == '__main__':
    import sys
    arg = sys.argv[1]
    print(equations.parse(arg))



