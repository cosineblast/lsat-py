# TODO: consider optimizing out s and d unecessary variables
# in FormulaBuilder

from rich import print

def minus(a, b):
    return ("minus", a, b)


def plus(a, b):
    return ("plus", a, b)

class FormulaBuilder:
    _equations = []
    _var_counter = 0

    def add_formula(self, input_formula):
        match input_formula:
            case ("Negation", formula):
                target_variable = self.add_formula(formula)

                y = self._add_variable()

                self._add_equation(("eq", y, minus(1, target_variable)))

                return y

            case ('Atomic', name):
                return self._add_variable("y_" + name)

            case ("Disjunction", left_formula, right_formula):
                a = self.add_formula(left_formula)
                b = self.add_formula(right_formula)

                y = self._add_variable()
                beta = self._add_variable()
                s = self._add_variable()

                equations = [
                    ("eq", s, plus(a, b)),
                    ("le", minus(s, beta), y),
                    ("le", y, s),
                    ("le", beta, y),
                    ("le", y, 1),
                ]

                for equation in equations:
                    self._add_equation(equation)

                return y

            case ("Conjunction", left_formula, right_formula):
                a = self.add_formula(left_formula)
                b = self.add_formula(right_formula)

                y = self._add_variable()
                beta = self._add_variable()
                d = self._add_variable()

                equations = [
                    ("eq", d, minus(plus(a, b), 1)),
                    ("le", d, y),
                    ("le", y, plus(d, beta)),
                    ("le", 0, y),
                    ("le", y, minus(1, beta)),
                ]

                for equation in equations:
                    self._add_equation(equation)

                return y

            case ("Max", left_formula, right_formula):
                a = self.add_formula(left_formula)
                b = self.add_formula(right_formula)

                y = self._add_variable()
                beta = self._add_variable()

                equations = [
                    ("le", a, y),
                    ("le", y, plus(a, beta)),
                    ("le", b, y),
                    ("le", y, plus(b, minus(1, beta))),
                ]

                for equation in equations:
                    self._add_equation(equation)

                return y

            case ("Min", left_formula, right_formula):
                a = self.add_formula(left_formula)
                b = self.add_formula(right_formula)

                y = self._add_variable()
                beta = self._add_variable()

                equations = [
                    ("le", minus(a, beta), y),
                    ("le", y, a),
                    ("le", minus(b, minus(1, beta)), y),
                    ("le", y, b),
                ]

                for equation in equations:
                    self._add_equation(equation)

                return y
        raise ValueError('Unknown formula: {}'.format(input_formula))

    def add_formula_assignment(self, formula_assignment):
        operator, formula, value = formula_assignment

        result = self.add_formula(formula)

        self._add_equation((operator, result, value))

    def _add_equation(self, equation):
        self._equations.append(equation)

    def _add_variable(self, name = None):
        if name is None:
            current = self._var_counter
            self._var_counter += 1
            return "x_{}".format(current)
        else:
            return name


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
        ("ge", p0, 0.3),
    ]

    equations = build_equations(things)


    print(equations)

if __name__ == '__main__':
    main()
