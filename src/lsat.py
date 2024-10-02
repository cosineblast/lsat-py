

from the_types import *

from constraint_builder import build_constraints


import test_util

import solver

import fire

import parser

from rich import print

def run(target, verbose=False):

    stuff = None
    with open(target) as file:
        stuff = file.read()

    parsed = parser.equations.parse(stuff)

    problem =  build_constraints(parsed)

    constraints, fvars, bvars = problem

    if verbose:
        print('Constraints:')
        print(constraints)

        print('Float Vars:')
        print(fvars)

        print('Binary Vars:')
        print(bvars)

        print('Solution:')

    solution = solver.solve_mixed_problem(problem)

    if solution is not None:
        atomics = {k[2:]:solution[k] for k in solution if k.startswith('a_')}

        print(atomics)
    else:
        print('null')

def main():
    fire.Fire(run)

if __name__ == '__main__':
    main()
