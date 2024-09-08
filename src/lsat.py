
from rich import print

from the_types import *

from constraint_builder import build_constraints


import test_util

import solver

def example1():

    p0 = Atomic("p0")
    p1 = Atomic("p1")

    things: list[FormulaConstraint] = [
        ("le", Min(p0, p1), 0.3),
        ("ge", Max(p0, p1), 0.6),
        ("eq", p0, 0.7),
        ("eq", p1, 0.1),
    ]

    print(solver.solve_formula_constraints(things))
    

def example2():
    p0 = Atomic("p0")
    p1 = Atomic("p1")

    things: list[FormulaConstraint] = [
        ("le", Min(p0, p1), 0.3),
        ("ge", Max(p0, p1), 0.6),
        ("eq", p0, 0.7),
        ("eq", p1, 0.1),
    ]

    problem =  build_constraints(things)
    constraints, fvars, bvars = problem


    print('Constraints:')
    print(constraints)

    print('Float Vars:')
    print(fvars)

    print('Binary Vars:')
    print(bvars)

    print('Solution:')
    print(solver.solve_mixed_problem(problem))




def main():
    example1()

if __name__ == '__main__':
    main()
