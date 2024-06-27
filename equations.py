
def disjunction_equations(a, b, beta, y):
    """
    Disjunction

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

    return [
        ('le', [a,b,beta,y], [1,1,-1,-1], 0),
        ('le', [y,a,b], [1,-1,-1], 0),
        ('le', [beta, y], [1, -1], 0),
        ('le', [y], [1], 1)
    ]


def conjunction_equations(a, b, beta, y):
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

    return [
        ('le',[a,b,y], [1,1,-1],  1),
        ('le',[y,a,b,beta], [1,-1,-1,-1],  -1),
        ('le',[y], [-1],  0),
        ('le',[y, beta], [1,1],  1)
    ]


def max_equations(a, b, beta, y):
    """
    Max

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

    return [
        ('le',[a,y], [1,-1],  0),
        ('le',[y,a,beta], [1,-1,-1],  0),
        ('le',[b,y], [1,-1],  0),
        ('le',[y,b,beta], [1,-1,1],  1)
    ]

def min_equations(a, b, beta, y):
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


    return [
        ('le',[a, beta, y], [1, -1, -1],  0),
        ('le',[y, a], [1, -1],  0),
        ('le',[b, beta, y], [1, 1, -1],  1),
        ('le',[y, b], [1, -1],  0)
    ]

def implication_equations(a, b, beta, y):
    """
    Implication

    1. s - β ≤ y ≤ s
    s = 1 + b - a

    s - β ≤ y
    1 + b - a - β ≤ y
    1 + b - a - β - y ≤ 0
    b - a - β - y ≤ -1

    [b,a,β,y] ∙ [1,-1,-1,-1] ≤ -1

    y ≤ s
    y ≤ 1 + b - a
    y - b + a ≤ 1
    [y,b,a] ∙ [1,-1,1] ≤ 1

    2. β ≤ y ≤ 1

    β ≤ y
    β - y ≤ 0
    [β, y] ∙ [1, -1] ≤ 0

    y ≤ 1
    [y] ∙ [1] ≤ 1
    """

    return [
        ('le',[b,a,beta,y], [1,-1,-1,-1],  -1),
        ('le',[y,b,a], [1,-1,1],  1),
        ('le',[beta,y], [1,-1],  0),
        ('le',[y], [1],  1)
    ]

