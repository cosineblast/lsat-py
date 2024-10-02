

from the_types import *

from typing import Tuple, Literal, Optional
import constraint_builder

from pyscipopt import Model

def solve_formula_constraints(source: list[FormulaConstraint]) -> Optional[dict[str, float]]:

    mixed_problem = constraint_builder.build_constraints(source)

    solution = solve_mixed_problem(mixed_problem)

    if solution is None: return None

    result = {}

    for name, value in solution.items():

        atom_name = constraint_builder.demangle_atom_name(name)

        if atom_name is not None:
            result[atom_name] = value

    return result


def solve_mixed_problem(problem: MixedProblem) -> Optional[dict[str, float]]:
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

    if solver.getStatus() == 'optimal':
        result = {}

        for name, variable in solver_vars.items():
            result[name] = solver.getVal(variable)

        return result
    else:
        return None

