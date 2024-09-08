
from the_types import *
from typing import Optional

def check_constraints(constraints: list[Constraint], assignments: dict[str, float]) -> Optional[tuple[Constraint, float]]:

    for constraint in constraints:

        relation, variables, coefficients, constant = constraint

        result = sum(map(lambda x,y: assignments[x] * y, variables, coefficients))

        ok = relation_matches(relation, result, constant)

        if not ok:
            return (constraint, result)

    return None


def evaluate_formula(formula: Formula, assignments: dict[str, float]) -> float:
    match formula:
        case Atomic(name):
            return assignments[name]

        case Min(left, right):
            return min(evaluate_formula(left, assignments), evaluate_formula(right, assignments))

        case Max(left, right):
            return max(evaluate_formula(left, assignments), evaluate_formula(right, assignments))

        case Conjunction(left, right):
            left_value = evaluate_formula(left, assignments)
            right_value = evaluate_formula(right, assignments)
            return max(0, 1 - right_value + left_value)

        case Disjunction(left, right):
            left_value = evaluate_formula(left, assignments)
            right_value = evaluate_formula(right, assignments)
            return min(1, right_value + left_value)

        case Implication(left, right):
            left_value = evaluate_formula(left, assignments)
            right_value = evaluate_formula(right, assignments)
            return min(1, 1 + right_value - left_value)

        case Negation(formula):
            return 1 - evaluate_formula(formula, assignments)


def relation_matches(relation: RelationLiteral, left: float, right: float) -> bool:
    match relation:
        case 'eq':
            return left == right

        case 'le':
            return left <= right

        case 'ge':
            return left >= right


def check_formula_constraints(constraints: list[FormulaConstraint], assignments: dict[str, float]) -> Optional[tuple[FormulaConstraint, float]]:

    for constraint in constraints:

        relation, formula, constant = constraint

        result = evaluate_formula(formula, assignments)

        ok = relation_matches(relation, result, constant)

        if not ok:
            return (constraint, result)

    return None

