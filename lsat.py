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

            case ("Disjunction", left_formula, right_formula):
                a = self.add_formula(left_formula)
                b = self.add_formula(right_formula)

                y = self._add_variable()
                beta = self._add_variable()

                """
                `s - β ≤ y ≤ s`

                s - β ≤ y →
                s - β - y ≤ 0 →
                a + b - β - y ≤ 0 →
                [a, b, β, y] ∙ [1, 1, -1, -1] ≤ 0

                y ≤ s →
                y ≤ a + b →
                y - a - b ≤ 0
                [y, a, b] ∙ [1, -1, -1] ≤ 0
                -}

                {-
                `β ≤ y ≤ 1`

                β ≤ y →
                β - y ≤  0 →
                [β, y] ∙ [1,-1] ≤ 0

                y ≤ 1 →
                [y] ∙ [1] ≤ 1
                """

                equations = [
                    ('le', [a,b,beta,y], [1,1,-1,-1], 0),
                    ('le', [y,a,b], [1,-1,-1], 0),
                    ('le', [beta, y], [1, -1], 0),
                    ('le', [y], [1], 1)
                ]

                for equation in equations:
                    self._add_equation(equation)

                return y

            case ("Conjunction", left_formula, right_formula):
                a = self.add_formula(left_formula)
                b = self.add_formula(right_formula)

                y = self._add_variable()
                beta = self._add_variable()

                """
                Conjunction

                1. `d ≤ y ≤ d + β`
                d ≤ y →
                d - y ≤ 0 →
                a+b-1-y ≤ 0
                a + b - y ≤ 1
                [a, b, y] ∙ [1, 1, -1] ≤ 1

                y ≤ d + β →
                y - d - β ≤ 0
                y - (a + b - 1) - β ≤ 0
                y - a - b + 1 - β ≤ 0
                y - a - b - β ≤ -1
                [y, a, b, β] ∙ [1, -1, -1, -1] ≤ -1

                2. `0 ≤ y ≤ 1 - β`

                0 ≤ y →
                - y ≤ 0 →
                [y] ∙ [-1] ≤  0

                y ≤ 1 - β →
                y + β ≤ 1
                [y,β] ∙ [1,1] ≤ 1
                """

                equations = [
                    ('le',[a,b,y], [1,1,-1],  1),
                    ('le',[y,a,b,beta], [1,-1,-1,-1],  -1),
                    ('le',[y], [-1],  0),
                    ('le',[y, beta], [1,1],  1)
                ]

                for equation in equations:
                    self._add_equation(equation)

                return y

            case ("Max", left_formula, right_formula):
                a = self.add_formula(left_formula)
                b = self.add_formula(right_formula)

                y = self._add_variable()
                beta = self._add_variable()

                """
                1. `a ≤ y ≤ a + β`
                a ≤ y →
                a - y ≤ 0 →
                [a, y] ∙ [1, -1] ≤ 0

                y ≤ a + β
                y - a - β ≤ 0
                [y,a,β] ∙ [1,-1,-1] ≤ 0


                2. `b ≤ y ≤ b + (1 - β)`

                b ≤ y
                b - y ≤ 0
                [b, y] ∙ [1,-1] ≤ 0

                y ≤ b + (1 - β)
                y - b + β ≤ 1
                [y,b,β] ∙ [1,-1,1] ≤ 1
                """

                equations = [
                    ('le',[a,y], [1,-1],  0),
                    ('le',[y,a,beta], [1,-1,-1],  0),
                    ('le',[b,y], [1,-1],  0),
                    ('le',[y,b,beta], [1,-1,1],  1)
                ]

                for equation in equations:
                    self._add_equation(equation)

                return y

            case ("Min", left_formula, right_formula):
                a = self.add_formula(left_formula)
                b = self.add_formula(right_formula)

                y = self._add_variable()
                beta = self._add_variable()

                """
                Min

                1. `a - β ≤ y ≤ a`
                a - β ≤ y
                a - β - y ≤ 0
                [a, β, y] ∙ [1, -1, -1] ≤ 0

                y ≤ a
                y - a ≤ 0
                [y,a] ∙ [1,-1] ≤ 0


                2. `b - (1 - β) ≤ y ≤ b`
                b - (1 - β) ≤ y
                b - (1 - β) - y ≤ 0
                b - 1 + β - y ≤ 0
                b + β - y ≤ 1

                [b, β, y] ∙ [1,1,-1] ≤ 1

                y ≤ b
                y - b ≤ 0
                [y,b] ∙ [1, -1] ≤ 0
                """


                equations = [
                    ('le',[a, beta, y], [1, -1, -1],  0),
                    ('le',[y, a], [1, -1],  0),
                    ('le',[b, beta, y], [1, 1, -1],  1),
                    ('le',[y, b], [1, -1],  0)
                ]

                for equation in equations:
                    self._add_equation(equation)

                return y
        raise ValueError('Unknown formula: {}'.format(input_formula))

    def add_formula_assignment(self, formula_assignment):
        operator, formula, value = formula_assignment

        result = self.add_formula(formula)

        self._add_equation((operator, [result], [1], value))

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
