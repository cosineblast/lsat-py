
from the_types import *
from typing import NamedTuple

import constraints

class _ConstraintBuilder:
    _constraints: list[Constraint] = []
    _float_vars: set[str] = set()
    _binary_vars: set[str] = set()
    _var_counter: int = 0

    def add_formula(self, input_formula: Formula):
        def add_binary_formula(left, right, fn):
            a = self.add_formula(left)
            b = self.add_formula(right)

            y = self._add_variable()
            beta = self._add_binary_variable()

            constraints = fn(a,b,beta,y)

            for constraint in constraints:
                self._add_constraint(constraint)

            return y

        match input_formula:
            case Negation(formula):
                t = self.add_formula(formula)

                y = self._add_variable()

                """
                y = 1 - t
                y + t = 1
                """

                self._add_constraint(('eq', [y, t], [1, 1], 1))

                return y

            case Atomic(name):
                return self._add_variable("a_" + name)

            case Disjunction(left, right):
                return add_binary_formula(left, right, constraints.disjunction_constraints)

            case Conjunction(left, right):
                return add_binary_formula(left, right, constraints.conjunction_constraints)

            case Max(left, right):
                return add_binary_formula(left, right, constraints.max_constraints)

            case Min(left, right):
                return add_binary_formula(left, right, constraints.min_constraints)

            case Implication(left, right):
                return add_binary_formula(left, right, constraints.implication_constraints)

        raise ValueError('Unknown formula: {}'.format(input_formula))

    def add_formula_assignment(self, formula_assignment: FormulaConstraint):
        operator, formula, value = formula_assignment

        result = self.add_formula(formula)

        self._add_constraint((operator, [result], [1], value))

    def _add_constraint(self, constraint: Constraint):
        self._constraints.append(constraint)

    def _inc_counter(self):
        current = self._var_counter
        self._var_counter += 1
        return current


    def _add_binary_variable(self, name = None):
        result = name if name is not None else "b_{}".format(self._inc_counter())
        self._binary_vars.add(result)
        return result

    def _add_variable(self, name = None):
        result = name if name is not None else "y_{}".format(self._inc_counter())
        self._float_vars.add(result)
        return result

class MixedProblem(NamedTuple):
    constraints: list[Constraint]
    float_variables: set[str]
    binary_variables: set[str]

def build_constraints(assignments: list[FormulaConstraint]) -> MixedProblem:
    builder = _ConstraintBuilder()

    for assignment in assignments:
        builder.add_formula_assignment(assignment)

    return MixedProblem(constraints = builder._constraints,
                        float_variables = builder._float_vars,
                        binary_variables = builder._binary_vars)
