
# O que é isso

Este projeto é um pequeno estudo no desenvolvimento do problema de satisfabilidade para a
[lógica de Łukasiewicz](https://en.wikipedia.org/wiki/%C5%81ukasiewicz_logic).

Ele utiiza um resolvedor de problemas de otimização inteira do google para
estas lógicas.

## Intuição

Para traduzir valorações da lógica L para um conjunto de inequações lineares mistas,
precisamos realizar transformações nas valorações das operações desta lógica:

Em todos os casos, uma variável adicional `β ∈ {0,1}` é introduzida.

### Disjunção

O valor de `v(φ ⊕ ψ)` é `min(1, v(φ) + v(ψ))`.

Sendo `s = v(φ) + v(ψ)`, as seguintes inequações garantem que
`y` seja igual a `v(φ ⊕ ψ)`:

1. `s - β ≤ y ≤ s`
2. `β ≤ y ≤ 1`

Quando β é 0, a equação 1 garante que `y = s`,
e a equação 2 garante que `y ≤ 1`, logo `y = min(1, s)`.

Quando β é 1, a equação 2 garante que `y = 1`,
e a equação 1 garante que `y ≤ s`, assim `y = min(1, s)`.

## Conjunção

O valor de `v(φ ⊗ ψ)` é `max(0, v(φ) + v(ψ) - 1)`.

Sendo `d = v(φ) + v(ψ) - 1`, as seguintes inequações garantem que
`y` seja igual a `v(φ ⊗ ψ)`:

1. `d ≤ y ≤ d + β`
2. `0 ≤ y ≤ 1 - β`

Quando β é 0, a equação 1 garante que `y = d`,
e a equação 2 garante que `0 ≤ y`, logo `y = max(0, d)`.

Quando β é 1, a equação 2 garante que `y = 0`,
e a equação 1 garane que `d ≤ y`, assim `y = max(0, d)`.

## Mínimo

O valor de `v(φ ∧ ψ)` é `min(v(φ), v(ψ))`.

Sendo `a = v(φ)` e `b = v(ψ)`, as seguintes inequações garantem que
`y` seja igual a `v(φ ∧ ψ)`:

1. `a - β ≤ y ≤ a`
2. `b - (1 - β) ≤ y ≤ b`

Quando β é 0, a equação 1 garante que `y = a`,
e a equação 2 garante que `y ≤ b`, logo `y = min(a, b)`.

Quando β é 1, a equação 2 garante que `y = b`,
e a equação 1 garane que `y ≤ a`, assim `y = min(a, b)`.

## Máximo

O valor de `v(φ ∨ ψ)` é `max(v(φ), v(ψ))`.

Sendo `a = v(φ)` e `b = v(ψ)`, as seguintes inequações garantem que
`y` seja igual a `v(φ ∨ ψ)`:

1. `a ≤ y ≤ a + β`
2. `b ≤ y ≤ b + (1 - β)`

Quando β é 0, a equação 1 garante que `y = a`,
e a equação 2 garante que `b ≤ y`, logo `y = max(a, b)`.

Quando β é 1, a equação 2 garante que `y = b`,
e a equação 1 garane que `a ≤ y`, assim `y = max(a, b)`.

