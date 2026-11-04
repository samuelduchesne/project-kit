# Mathematical derivations

This dimension covers the correspondence between the mathematics a piece of code claims to implement and the computation it actually performs. It includes equations and transformations compared with their stated or standard forms (each derivation step, signs, constant factors such as 2 and pi, transposes and conjugates), the shapes of matrices and arrays entering each operation, and the bounds of indices and summations, including off-by-one errors. It excludes floating-point behaviour (see numerical stability), units and physical validity (see physical modelling and units), and all matters of style, naming, formatting and performance. A finding in this dimension asserts that the code computes a different mathematical quantity from the one intended.

## Checks

1. **Stated-form correspondence.** Locate the reference form: a docstring, comment, cited paper, variable name or the standard textbook form of a named quantity. Compare the implemented expression term by term. A defect is established by an input for which the code and the reference form, evaluated by hand, give different values.
2. **Derivation steps.** Where the code implements a rearranged, simplified or discretised form, verify each algebraic step from the reference form to the code. Look for dropped terms, terms moved across an equality without a sign change, and a chain rule applied incompletely. Evidence is an input on which the original and the rearranged form disagree.
3. **Signs.** Check the sign of every term against the reference form, with particular attention to rotation matrices, cross products, gradient descent updates, and differences written as `a - b` where `b - a` is intended. Evidence is an input whose output has the wrong sign or the wrong orientation.
4. **Constant factors.** Check factors of 2, pi, 2 pi, 1/2 and normalisation constants: angular versus ordinary frequency, radius versus diameter, the 1/2 in kinetic energy or quadratic forms, and the normalisation of transforms and densities. Evidence is an input whose output differs from the reference by exactly the missing or extra factor.
5. **Transposes and conjugates.** Check whether `A`, `A^T` or `A^H` is required at each use, and whether a row-major or column-major convention changes the meaning of an index pair. Evidence is a non-symmetric (or complex) input whose output differs from the reference.
6. **Shapes.** Track the shape of each operand through the expression. Check that matrix products have conforming inner dimensions for the intended reason, not by coincidence (a square matrix conforms in both orders), and that reductions run over the intended axis. Evidence is a non-square input that either fails or yields a result of the wrong shape or value.
7. **Index and summation bounds.** Compare each loop or slice bound with the summation limits of the reference form, translating between one-based mathematical notation and zero-based code. Check inclusive versus exclusive upper bounds and the first and last terms. Evidence is a small input (two or three elements suffice) whose output includes a term that should be excluded or omits one that should be included.
8. **Index mapping.** Check that the index used to read an element matches the index in the formula: `x[i]` versus `x[i-1]`, swapped `i` and `j`, and neighbours in stencils. Evidence is an input with distinct element values for which the wrong element is read.

## Severity guidance

The severity definitions are those of the skill:

- High: produces a wrong result under realistic inputs; Medium: produces a wrong result only under plausible edge-case inputs, or prevents reproduction of a result; Low: a latent risk that does not currently produce a wrong result.

Typical mapping for this dimension:

- **High.** A wrong sign, a missing or extra constant factor, a missing transpose on a non-symmetric operand, a summation bound that includes or excludes a term for every input, or a wrong index in a stencil. These defects affect every typical input.
- **Medium.** A bound error that matters only for empty, single-element or boundary inputs; a transpose that is omitted where the operand is symmetric in every realistic case but not guaranteed to be; a formula whose convention (for example, transform normalisation) differs from the one stated, so that published results cannot be reproduced from the documentation.
- **Low.** An expression that is correct only because current callers pass square or symmetric operands, with no such call yet producing a wrong value; a reference form that is undocumented, so that a future change to the convention would go unnoticed.

## Not defects

- **Alternative but equivalent forms.** An expression rearranged into an algebraically equivalent form is not a defect, even when it differs visually from the textbook. Verify equivalence before reporting.
- **Documented conventions.** A different but documented convention (unitary versus non-unitary Fourier transform, `exp(-i omega t)` versus `exp(i omega t)`, row versus column vectors) is not a defect when it is applied consistently.
- **Zero-based translations.** A loop `range(0, n)` implementing a sum from 1 to n is correct when the body indexes element `i` as the i-plus-first term. Check the body, not only the bounds.
- **Symmetric operands by construction.** A missing transpose on a matrix that is symmetric by construction (a covariance matrix, a Gram matrix, a Laplacian) is not a defect.
- **Finite differences with n - 1 terms.** A loop starting at 1, or a sum of n - 1 terms, is correct for differences between consecutive elements. The shorter range is required, not an off-by-one.
- **Numerical concerns.** A correct formula that loses precision belongs to numerical stability, not to this dimension.

## Worked examples

### Defect 1: trapezoidal rule with an off-by-one interior sum (High)

The composite trapezoidal rule on n uniformly spaced samples is h times (y_0/2 + y_1 + ... + y_{n-2} + y_{n-1}/2). The interior sum runs over indices 1 to n - 2.

```python
def trapezoid(y: list[float], h: float) -> float:
    interior = sum(y[i] for i in range(1, len(y)))  # includes y[n-1]
    return h * (0.5 * (y[0] + y[-1]) + interior)
```

```typescript
function trapezoid(y: number[], h: number): number {
  let interior = 0;
  for (let i = 1; i < y.length; i++) interior += y[i]; // includes y[n-1]
  return h * (0.5 * (y[0] + y[y.length - 1]) + interior);
}
```

- **Trigger:** `y = [1, 1, 1]`, `h = 1` (the integral of the constant 1 over [0, 2]).
- **Wrong output:** 3. The correct value is 2; the last sample is counted with weight 3/2 instead of 1/2.
- **Fix:** bound the interior sum by `len(y) - 1` (Python `range(1, len(y) - 1)`; TypeScript `i < y.length - 1`).

### Defect 2: rotation matrix with transposed signs (High)

A counter-clockwise rotation by theta maps (x, y) to (x cos theta - y sin theta, x sin theta + y cos theta). The code below applies the transpose, which rotates clockwise.

```python
import math

def rotate(x: float, y: float, theta: float) -> tuple[float, float]:
    c, s = math.cos(theta), math.sin(theta)
    return (x * c + y * s, -x * s + y * c)
```

```typescript
function rotate(x: number, y: number, theta: number): [number, number] {
  const c = Math.cos(theta), s = Math.sin(theta);
  return [x * c + y * s, -x * s + y * c];
}
```

- **Trigger:** `(x, y) = (1, 0)`, `theta = pi / 2`, documented as a counter-clockwise rotation.
- **Wrong output:** approximately (0, -1). The correct value is (0, 1).
- **Fix:** return `(x * c - y * s, x * s + y * c)`, or document the function as a clockwise rotation if that is the intended convention and every caller agrees.

### Defect 3: matrix-vector product with a missing transpose (High)

The docstring states that the function returns `A^T v` for an m-by-n matrix `A` stored as a list of rows and a vector `v` of length m. The code computes `A v` instead, which conforms only when m equals n.

```python
def at_times_v(a: list[list[float]], v: list[float]) -> list[float]:
    """Return A^T v."""
    return [sum(a[i][j] * v[j] for j in range(len(v))) for i in range(len(a))]
```

```typescript
/** Return A^T v. */
function atTimesV(a: number[][], v: number[]): number[] {
  return a.map((row) => row.reduce((acc, aij, j) => acc + aij * v[j], 0));
}
```

- **Trigger:** `A = [[1, 2], [3, 4]]`, `v = [1, 0]`.
- **Wrong output:** `[1, 3]` (the first column of `A`). The correct value of `A^T v` is `[1, 2]` (the first row of `A`). For a 3-by-2 matrix with `v` of length 3, the Python version raises `IndexError` and the TypeScript version silently ignores `v[2]`.
- **Fix:** sum over the row index: element `j` of the result is the sum over `i` of `a[i][j] * v[i]`, for `j` from 0 to n - 1.

### Look-alike: consecutive differences over n - 1 terms (not a defect)

The loop below starts at index 1 and appears to skip an element. It computes the n - 1 forward differences of n samples, which is the intended quantity.

```python
def differences(x: list[float]) -> list[float]:
    return [x[i] - x[i - 1] for i in range(1, len(x))]
```

```typescript
function differences(x: number[]): number[] {
  const d: number[] = [];
  for (let i = 1; i < x.length; i++) d.push(x[i] - x[i - 1]);
  return d;
}
```

- **Candidate trigger:** `x = [0, 1, 3]`.
- **Output:** `[1, 2]`, which is correct: two differences from three samples, with no term omitted and no index out of range.
- **Reason not reported:** the range of n - 1 terms is required by the definition. No input produces a wrong value, so no concrete failure scenario exists.
