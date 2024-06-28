
from rich import print

from the_types import *

from constraint_builder import build_constraints, MixedProblem

from ortools.linear_solver import pywraplp

def solve(problem: MixedProblem):
    solver = pywraplp.Solver.CreateSolver("GLOP")

    if not solver:
        raise ValueError('Linear solver not found')

    inf = solver.infinity()

    solver_vars = dict()

    for variable in problem.float_variables:
        solver_vars[variable] = solver.NumVar(0.0, 1.0, variable)

    for variable in problem.binary_variables:
        solver_vars[variable] = solver.NumVar(0.0, 1.0, variable)

    for relation, variables, values, constant in problem.constraints:
        constraint = None

        match relation:
            case 'eq': constraint = solver.RowConstraint(constant, constant, '')
            case 'le': constraint = solver.RowConstraint(-inf, constant, '')
            case 'ge': constraint = solver.RowConstraint(constant, inf, '')

        for variable, value in zip(variables, values):
            constraint.SetCoefficient(solver_vars[variable], value)

    objective = solver.Objective()
    objective.SetMaximization()

    status = solver.Solve()

    print('(solution status code: {})'.format(status))

    if status == pywraplp.Solver.OPTIMAL:
        for variable in problem.float_variables | problem.binary_variables:
            print(variable, solver_vars[variable].solution_value())
    elif status == pywraplp.Solver.INFEASIBLE:
        print('NOSAT :(')
    else:
        raise Error('Some unexpected result happend, status={}'.format(status))

def main():
    p0 = Atomic("p0")
    p1 = Atomic("p1")

    things: list[FormulaConstraint] = [
        ("le", Min(p0, p1), 0.3),
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
