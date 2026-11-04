# Numerical stability

This dimension covers defects in which a computation that is mathematically correct produces a wrong result because of finite-precision arithmetic: floating-point equality comparisons, overflow and underflow, catastrophic cancellation, division by quantities that can approach zero, unstable evaluation of exponentials and logarithms, silent narrowing of numeric precision, implicit broadcasting that yields an unintended shape, and propagation of not-a-number (NaN) or missing values through reductions. It excludes style, naming, lint and performance; it also excludes errors in the underlying formula, which belong to the mathematical dimension. A finding in this dimension is reportable only when a concrete input can be stated together with the wrong output it produces.

## Checks

1. **Floating-point equality.** Look for `==` or `!=` (and `===`, `!==` in TypeScript) between floating-point values that are results of arithmetic, and for loop conditions that wait for a float to reach an exact value. Evidence: an input for which the computed value differs from the expected value in the last bits, for example `0.1 + 0.2 == 0.3` evaluating to false, and the branch taken as a result.
2. **Overflow and underflow.** Look for `exp`, `pow`, factorials, products of many terms, and squared magnitudes of large values. Evidence: an input within the realistic domain that yields `inf`, `Infinity`, `0.0` or a subnormal value where a finite, non-zero result is expected, and the downstream value that results.
3. **Catastrophic cancellation.** Look for subtraction of two nearly equal quantities whose difference is the quantity of interest: `E[x^2] - E[x]^2`, `1 - cos(x)` for small `x`, the textbook quadratic formula when `b^2 >> 4ac`, finite differences with a very small step. Evidence: an input for which the computed result has few or no correct significant digits, stated beside the exact value.
4. **Division near zero.** Look for denominators that are differences, norms, standard deviations, counts after filtering, or user-supplied parameters, with no guard. Evidence: an input that makes the denominator zero or vanishingly small, and the resulting `inf`, `NaN`, `ZeroDivisionError` or exploding value.
5. **Unstable exponential and logarithm evaluation.** Look for `log(sum(exp(x)))`, softmax computed as `exp(x) / sum(exp(x))`, `log(1 + x)` for small `x`, and `exp(x) - 1` for small `x`. Evidence: an input such as large logits for which the naive form returns `inf` or `NaN`, compared with the stable form (log-sum-exp with the maximum subtracted, `log1p`, `expm1`).
6. **Silent narrowing of precision.** Look for casts to `float32`, `float16` or integer types, `astype`, typed arrays such as `Float32Array` or `Int32Array`, integer division where real division is intended, and accumulation in a narrower type than the data. Evidence: an input whose result differs, beyond the stated tolerance, from the same computation carried out in the wider type.
7. **Unintended broadcasting.** Look for element-wise operations between arrays of shapes `(n,)` and `(n, 1)`, reductions without an explicit axis, and operations that silently expand a dimension. Evidence: the input shapes, the shape actually produced, and the shape the surrounding code requires.
8. **NaN propagation through reductions.** Look for `sum`, `mean`, `max`, `min` and sorting over data that can contain `NaN`, `None`, `null` or `undefined`, and for NaN-aware variants used where propagation is intended (or the reverse). Evidence: an input containing one missing value and the resulting reduction (`NaN`, a silently dropped element, or an order-dependent `max`).

## Severity guidance

The severity definitions are those of the skill:

- High: produces a wrong result under realistic inputs.
- Medium: produces a wrong result only under plausible edge-case inputs, or prevents reproduction of a result.
- Low: a latent risk that does not currently produce a wrong result.

Typical mapping for this dimension:

| Defect | Typical severity | Condition |
| --- | --- | --- |
| Naive log-sum-exp or softmax on logits or log-likelihoods | High | Inputs of magnitude above about 700 (float64) or 88 (float32) occur in normal use |
| Variance as `E[x^2] - E[x]^2` on data with a large mean | High | Measured data with a mean far larger than its spread |
| Equality test on an arithmetic float result controlling a branch | High | The compared values are computed, not assigned |
| Division by a difference, count or norm without a guard | Medium | Zero is reachable only for degenerate inputs (empty filter, identical points) |
| Narrowing to `float32` before accumulation | Medium | Error exceeds tolerance only for long series or large magnitudes |
| Reduction that propagates or drops `NaN` unexpectedly | Medium | Missing values are possible but not typical |
| Broadcasting that yields a wrong shape | High | The wrong shape is consumed without error |
| Unguarded denominator that cannot currently reach zero | Low | All present callers guarantee a non-zero value |

## Not defects

The following constructs resemble defects but are correct in context and must not be reported. Each should appear among the items checked and found correct.

1. **Equality against a sentinel value.** `x == -9999.0`, `x === -1` or `value == MISSING` where the sentinel is assigned, never computed, is exact: an assigned literal is stored without rounding, and the comparison tests identity of a marker, not closeness of a measurement.
2. **Equality against an exact integer-valued float.** `n == 0.0`, `count == 3.0` or `x == 1.0` where the value is an integer-valued float obtained by assignment, counting or conversion of an integer within the exact range (magnitude at most 2^53 for float64) is exact. Every integer in that range is representable, and integer addition within it does not round.
3. **Equality used to detect an exact zero before a guarded operation.** `if denom == 0: return default` is correct when the intent is to avoid an exception; near-zero values are a separate check (4) that must be argued on its own evidence.
4. **Division whose denominator is provably non-zero.** A denominator that is a constant, a length checked earlier, or a quantity bounded away from zero by validation is not a defect.
5. **Deliberate reduced precision.** Use of `float32` or `float16` that is documented, matches an external format (GPU kernels, file formats) and stays within a stated tolerance is a design choice, not a defect.
6. **Intentional broadcasting.** Subtracting a `(1, m)` row of column means from an `(n, m)` matrix is the standard idiom; it is a defect only when the resulting shape differs from the shape required.
7. **NaN propagation that is intended.** A reduction that returns `NaN` to signal missing input, and whose callers check for it, is correct.

## Worked examples

### Defect: naive log-sum-exp (check 5, High)

Trigger: `x = [1000, 1000]`. Wrong output: `inf` (Python) and `Infinity` (TypeScript), because `exp(1000)` overflows. Correct value: `1000 + log(2) = 1000.6931...`.

```python
import math

def logsumexp(x: list[float]) -> float:
    return math.log(sum(math.exp(v) for v in x))  # inf for x = [1000, 1000]
```

```typescript
const logSumExp = (x: number[]): number =>
  Math.log(x.reduce((s, v) => s + Math.exp(v), 0)); // Infinity for [1000, 1000]
```

Fix: subtract the maximum before exponentiating.

```python
def logsumexp(x: list[float]) -> float:
    m = max(x)
    return m + math.log(sum(math.exp(v - m) for v in x))
```

```typescript
const logSumExp = (x: number[]): number => {
  const m = Math.max(...x);
  return m + Math.log(x.reduce((s, v) => s + Math.exp(v - m), 0));
};
```

### Defect: variance by catastrophic cancellation (check 3, High)

Trigger: `xs = [1e9 + 1, 1e9 + 2, 1e9 + 3]`. Wrong output: `0.0` in both languages. Correct population variance: `0.6666...`. The two terms are near `1e18`, where adjacent doubles are 128 apart, so their difference retains no correct digits.

```python
def variance(xs: list[float]) -> float:
    m = sum(xs) / len(xs)
    return sum(x * x for x in xs) / len(xs) - m * m  # 0.0
```

```typescript
const variance = (xs: number[]): number => {
  const m = xs.reduce((a, b) => a + b, 0) / xs.length;
  return xs.reduce((a, x) => a + x * x, 0) / xs.length - m * m; // 0
};
```

Fix: use the two-pass form `sum((x - m) ** 2) / n` (or Welford's algorithm for streaming data), which returns `0.6666666666666666` for the same input.

### Look-alike: equality against a sentinel (not a defect)

The value `-9999.0` is a missing-data marker assigned by the reader, never the result of arithmetic. The comparison is exact and must not be reported.

```python
MISSING = -9999.0

def valid(readings: list[float]) -> list[float]:
    return [r for r in readings if r != MISSING]
```

```typescript
const MISSING = -9999.0;
const valid = (readings: number[]): number[] =>
  readings.filter((r) => r !== MISSING);
```

Reason: no input exists for which an assigned `-9999.0` compares unequal to the literal `-9999.0`, so no failure scenario can be stated. A finding would be reportable only if the sentinel were produced by computation (for example after unit conversion), in which case the comparison falls under check 1.
