
from rich import print

from the_types import *

from constraint_builder import MixedProblem, build_constraints

from pyscipopt import Model

import test_util

def solve(problem: MixedProblem):
    solver = Model('Example')

    solver.hideOutput()

    solver_vars = dict()

    for name in problem.float_variables:
        variable = solver.addVar(name)
        solver_vars[name] = variable
        solver.addCons(0.0 <= variable)
        solver.addCons(variable <= 1.0)

    for name in problem.binary_variables:
        solver_vars[name] = solver.addVar(name, vtype='B')


    for relation, variables, values, constant in problem.constraints:

        left_side = 0

        for variable, value in zip(variables, values):
            left_side = (solver_vars[variable] * value) + left_side

        match relation:
            case 'eq': constraint = left_side == constant
            case 'le': constraint = left_side <= constant
            case 'ge': constraint = left_side >= constant

        solver.addCons(constraint)

    solver.optimize()

    print('status:', solver.getStatus())

    if solver.getStatus() == 'optimal':
        for v in solver.getVars():
            print(v, solver.getVal(v))



def main():
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
    solve(problem)


if __name__ == '__main__':
    main()
