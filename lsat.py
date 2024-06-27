from rich import print

import equations

def minus(a, b):
    return ("minus", a, b)


def plus(a, b):
    return ("plus", a, b)

class FormulaBuilder:
    _equations = []
    _var_counter = 0

    def add_formula(self, input_formula):
        def add_binary_formula(left, right, fn):
            a = self.add_formula(left)
            b = self.add_formula(right)

            y = self._add_variable()
            beta = self._add_binary_variable()

            equations = fn(a,b,beta,y)

            for equation in equations:
                self._add_equation(equation)

            return y

        match input_formula:
            case ("Negation", formula):
                t = self.add_formula(formula)

                y = self._add_variable()

                """
                y = 1 - t
                y + t = 1
                """

                self._add_equation(('eq', [y, t], [1, 1], 1))

                return y

            case ('Atomic', name):
                return self._add_variable("y_" + name)

            case ("Disjunction", left, right):
                return add_binary_formula(left, right, equations.disjunction_equations)

            case ("Conjunction", left, right):
                return add_binary_formula(left, right, equations.conjunction_equations)

            case ("Max", left, right):
                return add_binary_formula(left, right, equations.max_equations)

            case ("Min", left, right):
                return add_binary_formula(left, right, equations.min_equations)

            case ('Implication', left, right):
                return add_binary_formula(left, right, equations.implication_equations)

        raise ValueError('Unknown formula: {}'.format(input_formula))

    def add_formula_assignment(self, formula_assignment):
        operator, formula, value = formula_assignment

        result = self.add_formula(formula)

        self._add_equation((operator, [result], [1], value))

    def _add_equation(self, equation):
        self._equations.append(equation)

    def _inc_counter(self):
        current = self._var_counter
        self._var_counter += 1
        return current


    def _add_binary_variable(self, name = None):
        return self._add_variable("b_{}".format(self._inc_counter()))

    def _add_variable(self, name = None):
        return name if name is not None else "x_{}".format(self._inc_counter())




def build_equations(assignments):

    builder = FormulaBuilder()

    for assignment in assignments:
        builder.add_formula_assignment(assignment)

    return builder._equations


def main():
    p0 = ("Atomic", "p0")
    p1 = ("Atomic", "p1")
    p2 = ("Atomic", "p2")

    things = [
        ("le", ("Negation", p0), 0.2),
        ("ge", ("Conjunction", p0, p1), 0.3),
        ("le", ("Max", p1, p2), 0.3),
        ("ge", ("Min", p1, ('Conjunction', p1, p2)), 0.8),
        ("eq", ("Implication", p0, p2), 1.0),
        ("ge", p0, 0.3),
    ]

    equations = build_equations(things)


    print(equations)

if __name__ == '__main__':
    main()
