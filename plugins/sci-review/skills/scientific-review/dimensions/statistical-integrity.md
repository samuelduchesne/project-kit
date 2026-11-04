# Statistical integrity

This dimension covers the integrity of data handling in statistical and data-science code (FR-011): leakage of information from validation, test or future data into training or estimation; plotting and reporting code that mutates the data it displays; and stochastic processes whose results cannot be reproduced because no seed or other reproducibility control is applied. It excludes the numerical behaviour of the estimators themselves (numerical stability), the physical meaning of the quantities (physical modelling and units), the correctness of formulas (mathematical invariants), and nondeterminism caused by parallel execution order (algorithmic correctness). A finding in this dimension must show that a reported number, metric or figure differs from the value that leak-free, non-mutating, reproducible code would produce.

## Checks

1. **Preprocessing fitted before the split.** Look for a stateful transform (scaler, imputer, encoder, PCA, feature selector, outlier filter, vocabulary builder) whose `fit` or statistics use rows that later belong to the validation or test set, including fitting inside a cross-validation loop on the full fold set rather than on each training fold. Evidence: a held-out row whose value changes a quantity used in training (a mean, a variance, an imputed value, a selected feature), and the resulting change in the transformed training data or in the evaluation metric.
2. **Temporal leakage.** Look for random or shuffled splits of time-ordered data, features that read future values (centred rolling windows, backward fill, negative shifts, statistics over the whole series), and labels joined on a time key without an "as of" constraint. Evidence: a timestamp `t` in the training or prediction set whose feature depends on an observation after `t`, with the value it takes with and without that observation.
3. **Target and post-outcome leakage.** Look for features computed from the target, from records created after the outcome, or from aggregates (target encodings, group means) that include the row being predicted. Evidence: a row whose feature changes when its own label changes.
4. **Entity and duplicate leakage.** Look for row-level splits of data with repeated subjects, sites, sessions or exact duplicates. Evidence: an entity or duplicated row present in both training and test sets, and the metric inflation this produces.
5. **Selection on the test set.** Look for hyperparameters, thresholds, feature sets or early-stopping points chosen by the score on the data that is then reported as the held-out result. Evidence: the reported score is the maximum over candidates evaluated on the same held-out data.
6. **Mutation by plotting or reporting.** Look for in-place operations on caller-owned data inside plotting, logging or summary functions: in-place sort, `inplace=True`, augmented assignment on a passed array or column, `dropna` or filtering on the original, `Array.prototype.sort`, `reverse` or `splice` on an argument. Evidence: a call sequence in which a value computed after the plot or report differs from the value computed before it.
7. **Unseeded stochastic processes.** Look for random sampling, shuffling, initialisation, bootstrap, Monte Carlo, dropout or stochastic optimisation that draws from an unseeded or global generator (`np.random.*` without a seed, `random.random`, `default_rng()` with no argument, `Math.random`) in code that produces a reported result. Evidence: two runs on identical inputs that produce different reported values.
8. **Incomplete seeding.** Look for a seed that does not reach every generator in use: one library seeded while another is not, worker processes or threads that inherit or re-derive the same or an unset state, or a seed applied after the first draw. Evidence: the generator that remains unseeded and the output that varies between runs.

## Severity guidance

Severity definitions, from the skill: **High:** produces a wrong result under realistic inputs; **Medium:** produces a wrong result only under plausible edge-case inputs, or prevents reproduction of a result; **Low:** a latent risk that does not currently produce a wrong result.

| Typical defect | Severity |
| --- | --- |
| Scaler, imputer or feature selector fitted on data that includes the validation or test rows, where a metric is reported | High |
| Random split or future-reading feature on time-ordered data used for forecasting or evaluation | High |
| Target encoding or feature that includes the predicted row's own label | High |
| Plotting or reporting function that mutates data used by a later computation in the same pipeline | High |
| Entity or duplicate leakage present only when a subject appears more than once, which the data permits but rarely contains | Medium |
| Unseeded stochastic process whose output is reported (prevents reproduction) | Medium |
| Seed that does not reach one generator in use (prevents reproduction) | Medium |
| Mutating plotting or reporting function whose callers do not currently reuse the data afterwards | Low |
| Global-generator use in code that currently runs only with a fixed, seeded caller | Low |

## Not defects

- **Stateless transforms before the split.** A logarithm, a fixed unit conversion, clipping to physical constants or a fixed one-hot vocabulary learns nothing from the data, so applying it before the split cannot leak.
- **Fitting inside a pipeline.** A transform inside a pipeline object passed to cross-validation is refitted on each training fold; this is the correct order.
- **Refitting on all data after evaluation.** Refitting the final model and its preprocessing on the full dataset for deployment is correct when the reported metrics were computed earlier on a proper split.
- **Seeding documented as left to the caller (FR-015).** A function that accepts a generator or seed parameter, or whose documentation states that the caller is responsible for seeding, is correct; the reproducibility obligation lies with the caller, which may be reviewed separately.
- **Randomness that does not affect a reported result.** Random temporary file names, retry jitter, UI colours and sampling for a visual preview that is not reported as a statistic are not stochastic results.
- **Retrospective smoothing.** A centred window or backward fill in descriptive analysis of a completed series, where nothing is predicted or evaluated, is not temporal leakage.
- **Mutation of a local copy.** In-place operations on an explicit copy (`df.copy()`, `[...arr]`, `arr.slice()`, `np.array(x, copy=True)`) inside a plotting function do not affect the caller.

## Worked examples

### Defect 1: scaler fitted before the train/test split (High)

```python
X_scaled = StandardScaler().fit_transform(X)       # fit sees every row
X_tr, X_te = X_scaled[:4], X_scaled[4:]
```

```typescript
const mu = mean(x), sd = std(x);                   // statistics over every row
const scaled = x.map(v => (v - mu) / sd);
const [train, test] = [scaled.slice(0, 4), scaled.slice(4)];
```

Trigger: `x = [1, 2, 3, 4, 100]` with the last row held out. Wrong output: the training mean is 22.0 and the population standard deviation is 39.01, so the first training row scales to -0.538; with the scaler fitted on the training rows only (mean 2.5, standard deviation 1.118) it scales to -1.342. The test row's value has entered every training feature, and any reported test metric is computed against statistics that already include the test data. Fix: split first, fit on the training rows, transform both sets with the fitted parameters (`scaler.fit(X_tr)`, then `scaler.transform(X_te)`; in TypeScript compute `mu` and `sd` from `train` only).

### Defect 2: plotting function sorts the caller's data in place (High)

```python
def plot_profile(t, y):
    y.sort()                                       # mutates the caller's list
    plt.plot(t, y)

plot_profile(t, y); peak_time = t[int(np.argmax(y))]
```

```typescript
function plotProfile(t: number[], y: number[]): void {
  y.sort((a, b) => a - b);                         // mutates the caller's array
  chart.line(t, y);
}
plotProfile(t, y); const peakTime = t[y.indexOf(Math.max(...y))];
```

Trigger: `t = [0, 1, 2]`, `y = [3, 1, 2]`. Wrong output: after the call `y` is `[1, 2, 3]`, so the peak time is reported as 2 instead of 0, and the plotted curve no longer pairs each time with its value. Fix: sort a copy (`ys = sorted(y)`; `const ys = [...y].sort(...)`), or plot without sorting.

### Look-alike: seeding documented as left to the caller (not a defect)

```python
def bootstrap_mean(x: np.ndarray, n: int, rng: np.random.Generator) -> np.ndarray:
    """Resample x n times. Seeding is the caller's responsibility via rng."""
    return np.array([rng.choice(x, x.size).mean() for _ in range(n)])
```

```typescript
/** Resample x n times. The caller supplies a seeded generator `rand`. */
function bootstrapMean(x: number[], n: number, rand: () => number): number[] {
  return Array.from({ length: n }, () =>
    mean(x.map(() => x[Math.floor(rand() * x.length)])));
}
```

Reason: the function draws only from the generator it is given and documents that seeding belongs to the caller, so two calls with identically seeded generators return identical results. No trigger produces an irreproducible output inside this function. Report it among the items checked and found correct. The same function calling `np.random.choice` or `Math.random` directly, with no documented contract, would be a defect under check 7 (Medium).
