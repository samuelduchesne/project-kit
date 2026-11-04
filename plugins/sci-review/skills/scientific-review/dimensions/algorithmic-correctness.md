# Algorithmic correctness

This dimension covers whether an algorithm computes the result it claims to compute for every input it accepts: the invariants and pre- and postconditions it relies on, the termination and convergence of loops and iterative methods, integer overflow and index arithmetic, the handling of empty, single-element and duplicate-key inputs, dependence on evaluation order or concurrent execution, nondeterminism across runs or platforms, and caches that return stale results. It excludes style, naming, structure and performance, except where a performance construct (parallelism, caching, early exit) changes the result. Floating-point error analysis belongs to the numerical dimension; this dimension is concerned with the control flow and data handling that surround the arithmetic.

## Checks

Each check states what to look for and what evidence establishes a defect. Evidence is always a concrete input or program state together with the wrong output it produces. A suspicion without such a pair is recorded as a checked item, not as a finding with a trigger.

1. **Invariants and pre- and postconditions.** Identify what each function assumes of its inputs (sorted, non-negative, unique, normalised, same length) and what it guarantees of its output. Look for callers that violate an assumption and for code paths that break a guarantee. Evidence: an input that satisfies the documented contract, or a call site that passes an input violating an undocumented assumption, and the incorrect output that follows.
2. **Termination.** Examine every loop and recursion whose exit depends on data. Look for loop variables that may fail to progress, recursion without a decreasing measure, and `while` conditions that can remain true indefinitely. Evidence: an input for which the procedure does not terminate, or terminates only through an external timeout.
3. **Convergence criteria.** For iterative methods, check that the stopping test is meaningful at the scale of the quantity (absolute against relative tolerance), that a maximum iteration count exists, and that reaching it is reported rather than silently returning the last iterate. Evidence: an input for which the method stops early with an inaccurate value, or exhausts its iterations and returns an unconverged value presented as a result.
4. **Integer overflow and precision limits.** Look for fixed-width integers (NumPy `int32` or `int64`, C extensions, TypeScript bitwise operators that coerce to 32 bits), products of counts or indices, and TypeScript `number` values above 2^53. Evidence: realistic input sizes for which an intermediate value exceeds the representable range, and the wrapped or rounded output.
5. **Index arithmetic.** Check half-open against closed intervals, off-by-one boundaries, lengths computed as `end - start` versus `end - start + 1`, Python negative indices that wrap silently, and TypeScript out-of-range reads that yield `undefined` and then `NaN`. Evidence: an index range and the element that is dropped, duplicated or read from the wrong position.
6. **Empty, single-element and duplicate-key inputs.** Check behaviour on an empty collection (division by a zero count, `max` of nothing, reduction without an initial value), on one element (sample variance with denominator `n - 1`, interpolation with one point), and on duplicate keys (dictionary or `Map` construction that keeps only the last value, sort or merge steps that assume uniqueness). Evidence: the specific degenerate input and the silent wrong value, as opposed to a clear error.
7. **Order dependence.** Look for results that depend on iteration order: floating-point reductions over unordered collections, iteration over Python `set` values or over string-keyed hashes, JavaScript object keys that reorder integer-like keys, unsorted directory listings, and "first match wins" logic over unordered data. Evidence: two orderings of the same input that produce different outputs.
8. **Concurrency dependence.** Look for shared mutable state updated from threads, processes, async tasks or workers, and for accumulation in completion order rather than submission order (for example a parallel floating-point sum). Evidence: an input and two schedules that yield different results, or a race that loses an update.
9. **Nondeterminism across runs or platforms.** Look for unseeded random generators whose output feeds a reported result, hash randomisation, wall-clock time, thread-count-dependent reductions in BLAS or GPU libraries, and platform-dependent defaults (integer width on Windows NumPy before 2.0, locale-dependent parsing). Evidence: two runs or two platforms with identical inputs and different outputs.
10. **Stale caching.** For every cache or memoisation, list the inputs the cached value depends on and compare them with the cache key. Look for keys that omit a parameter, a mutable global, a file's contents or a configuration value, and for caches keyed on object identity of mutable objects. Evidence: a sequence of calls in which a dependency changes and the cache returns the value computed under the old dependency.

## Severity guidance

The severities are defined as follows:

- High: produces a wrong result under realistic inputs.
- Medium: produces a wrong result only under plausible edge-case inputs, or prevents reproduction of a result.
- Low: a latent risk that does not currently produce a wrong result.

Typical mappings for this dimension:

| Defect | Typical severity |
|---|---|
| Cache key omits a parameter that callers vary in normal use | High |
| Iterative method returns an unconverged value as a result for inputs in the documented range | High |
| Off-by-one boundary that drops or double-counts an element on every call | High |
| Overflow of an `int32` counter at input sizes the project processes | High |
| Wrong value (not an error) on empty, single-element or duplicate-key input that a caller can plausibly supply | Medium |
| Parallel floating-point sum accumulated in completion order, so results differ between runs | Medium |
| Undocumented unseeded randomness or unsorted directory listing that changes reported results between runs | Medium |
| Missing iteration limit where all current inputs converge quickly | Low |
| Overflow reachable only at input sizes far beyond any current use | Low |
| Cache that would become stale only if a currently constant configuration value were made mutable | Low |

When a defect produces a wrong result under realistic inputs only on some platforms that the project supports, it remains High. When it produces a wrong result only on a platform the project does not support, it is Low.

## Not defects

The following constructs resemble defects in this dimension and must not be reported.

- **Floating-point equality against a sentinel or an exact integer-valued float.** Comparing with `0.0` or `-1.0` when the value was assigned that literal, testing for `NaN` with `isnan` or `Number.isNaN`, or comparing floats that hold small integers exactly, is correct. Exact equality is a defect only when the value is the result of inexact arithmetic.
- **Seeding left to the caller and documented as such.** A function that accepts a generator or seed argument, or documents that callers must seed, is not nondeterministic within this dimension.
- **Order-independent reductions.** Integer sums, `min`, `max`, set union and counting do not depend on order. Python `dict` iteration follows insertion order since Python 3.7 and is deterministic for a deterministic insertion sequence.
- **Nondeterminism that does not reach a result.** Log ordering, progress output, timing measurements and temporary file names that do not affect reported values are not defects.
- **Python integer arithmetic.** Built-in `int` has arbitrary precision and does not overflow; only fixed-width types (NumPy, `array`, `ctypes`, extensions) can.
- **Defensive errors on degenerate input.** A function that raises a clear exception on empty input handles the edge case; only a silent wrong value is a defect.
- **Caches keyed on the full set of immutable inputs.** `functools.lru_cache` on a pure function of hashable arguments, or a `Map` keyed on a complete serialised input, cannot return stale values.
- **Performance-only concerns.** Quadratic algorithms, redundant recomputation and missing caches are outside this dimension unless they change the result.

## Worked examples

### Defect 1: parallel sum accumulated in completion order (check 8, Medium)

Trigger: chunk partial sums `[1e16, 1.0, -1e16]` complete in a schedule-dependent order. Wrong output: the total is `1.0` when the chunks finish in the order 1e16, -1e16, 1.0, and `0.0` when they finish in the order 1e16, 1.0, -1e16, because `1e16 + 1.0` rounds to `1e16`. The same input gives different results across runs.

```python
total = 0.0
with ThreadPoolExecutor() as pool:
    futures = [pool.submit(partial_sum, c) for c in chunks]
    for f in as_completed(futures):   # completion order varies per run
        total += f.result()
```

```typescript
let total = 0;
await Promise.all(chunks.map(async (c) => {
  const s = await partialSum(c);
  total += s;                         // accumulated as each promise settles
}));
```

Fix: collect the partial sums in submission order and reduce them in a fixed order, preferably with a compensated sum (`math.fsum(f.result() for f in futures)` in Python; `const parts = await Promise.all(chunks.map(partialSum))` followed by a fixed-order Neumaier sum in TypeScript).

### Defect 2: cache key omits a dependency (check 10, High)

Trigger: `emission_factor("QC")` is called with the reference year 2020, the reference year is then set to 2030, and `emission_factor("QC")` is called again. Wrong output: the second call returns the 2020 factor, because the cache key contains only the region.

```python
REFERENCE_YEAR = 2020

@lru_cache(maxsize=None)
def emission_factor(region: str) -> float:
    return load_table(REFERENCE_YEAR)[region]
```

```typescript
let referenceYear = 2020;
const cache = new Map<string, number>();
function emissionFactor(region: string): number {
  if (!cache.has(region)) cache.set(region, loadTable(referenceYear)[region]);
  return cache.get(region)!;
}
```

Fix: make every dependency part of the key by passing it as an argument: `emission_factor(region: str, year: int)` in Python, and a key such as `` `${region}:${year}` `` in TypeScript.

### Look-alike: equality against an assigned sentinel (not a defect)

The weights below are assigned the literal `0.0` to mark excluded samples, so the exact comparison is correct; no input produces a wrong output. Reporting it would violate FR-015.

```python
weights = [0.0 if s.excluded else s.weight for s in samples]
for w, s in zip(weights, samples):
    if w == 0.0:          # sentinel assigned above, not computed
        continue
    acc += w * s.value
```

```typescript
const weights = samples.map((s) => (s.excluded ? 0 : s.weight));
samples.forEach((s, i) => {
  if (weights[i] === 0) return;   // sentinel assigned above, not computed
  acc += weights[i] * s.value;
});
```

Reason it is not a defect: the compared value is an exact literal assigned on a known path, not the result of inexact arithmetic. It would become a defect only if a computed weight could be a tiny non-zero value intended to mean "excluded", which requires a concrete input to establish.
