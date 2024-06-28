
from rich import print

from the_types import *

from constraint_builder import build_constraints, MixedProblem
















def main():
    p0 = Atomic("p0")
    p1 = Atomic("p1")
    p2 = Atomic("p2")

    things: list[FormulaConstraint] = [
        ("le", Negation(p0), 0.2),
        ("ge", Conjunction(p0, p1), 0.3),
        ("le", Max(p1, p2), 0.3),
        ("ge", Min(p1, Conjunction(p1, p2)), 0.8),
        ("eq", Implication(p0, p2), 1.0),
        ("ge", p0, 0.3),
    ]

    constraints, fvars, bvars = build_constraints(things)

    print('Constraints:')
    print(constraints)

    print('Float Vars:')
    print(fvars)

    print('Binary Vars:')
    print(bvars)
    print(fvars)
if __name__ == '__main__':
    main()
