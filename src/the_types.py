
from typing import Tuple, Literal, Optional
from dataclasses import dataclass
from typing import NamedTuple

RelationLiteral = Literal['eq', 'le', 'ge']

Constraint = Tuple[RelationLiteral, list[str], list[float], float]

@dataclass
class Atomic:
    name: str

@dataclass
class Negation:
    target: 'Formula'

@dataclass
class Conjunction:
    left: 'Formula'
    right: 'Formula'

@dataclass
class Disjunction:
    left: 'Formula'
    right: 'Formula'

@dataclass
class Min:
    left: 'Formula'
    right: 'Formula'

@dataclass
class Max:
    left: 'Formula'
    right: 'Formula'

@dataclass
class Implication:
    left: 'Formula'
    right: 'Formula'

Formula = Atomic | Negation | Conjunction | Disjunction | Min | Max | Implication

FormulaConstraint = Tuple[RelationLiteral, Formula, float]

class MixedProblem(NamedTuple):
    constraints: list[Constraint]
    float_variables: set[str]
    binary_variables: set[str]

