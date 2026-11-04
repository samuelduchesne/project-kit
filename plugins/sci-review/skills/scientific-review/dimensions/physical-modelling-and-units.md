# Physical modelling and units

This dimension covers whether code represents physical quantities and physical models correctly: explicit and consistent units, unit handling where data is read or written, conservation laws in continuous and discrete form, probabilities and fractions that must sum to one, values outside physically possible bounds, discretisation of space and time, boundary and initial conditions, stability limits of time-stepping schemes, sign conventions and coordinate frames, and use of a model outside its regime of validity. It excludes style, naming, performance and lint, as well as floating-point behaviour that belongs to numerical stability. It contains no domain-specific rules (for example building-energy rules); those are contributed by domain extensions.

## Checks

1. **Explicit, consistent units.** Look for physical quantities combined in one expression without a stated or derivable unit, and for operands whose units differ (kPa added to Pa, hours multiplied by a rate per second). Evidence: an input in the documented unit and the output that is wrong by the conversion factor.
2. **Unit handling at I/O.** Look at file readers, API boundaries, configuration and serialisation: values read in one unit and used as another (degrees Celsius used as kelvin, degrees used as radians, kilometres as metres), or written without recording the unit. Evidence: a realistic file value and the resulting output, compared with the value obtained after correct conversion.
3. **Conservation, continuous and discrete.** Check that mass, energy, momentum, charge or count is conserved by the governing equations and also by the discrete update (fluxes leaving one cell enter its neighbour; sources and sinks are accounted once). Evidence: an initial state whose total changes over a step with no source or sink, and the size of the drift.
4. **Probabilities and fractions sum to one.** Check that mixtures, distributions, partition fractions and transition matrix rows are normalised after every update, clipping or truncation. Evidence: an input after which the components sum to a value other than one beyond rounding, and the downstream quantity that is therefore wrong.
5. **Physically impossible values.** Look for paths that produce negative absolute temperature, negative mass, density or concentration, a probability outside [0, 1], an efficiency above one, or a speed above a stated limit, without detection. Evidence: an input that drives the value across the bound and the value produced.
6. **Discretisation.** Check grid spacing, cell-centre versus cell-face placement, off-by-one extents of the domain, and time-step accumulation (for example `t += dt` drifting from `n * dt` when a stopping condition depends on it). Evidence: a grid or step sequence for which the computed solution differs from the analytical or refined solution beyond the scheme's stated order.
7. **Boundary and initial conditions.** Check that every boundary has a condition, that the condition is applied to the correct nodes or faces, that Dirichlet, Neumann and periodic conditions are not confused, and that initial conditions are consistent with the boundary conditions. Evidence: a configuration in which a boundary value or flux in the output differs from the one prescribed.
8. **Stability limits of explicit schemes.** For explicit time stepping, derive the stability limit (CFL for advection, `alpha * dt / dx**2 <= 1/2` for one-dimensional explicit diffusion, the oscillation limit for stiff source terms) and check that the code enforces it or chooses `dt` from it. Evidence: parameter values that violate the limit and the resulting growing or oscillating output.
9. **Sign conventions and frames.** Check that the sign of fluxes, forces and heat transfer is consistent between producer and consumer, and that vectors are not combined across coordinate frames (body versus inertial, local versus global, east-north-up versus north-east-down) without a transformation. Evidence: an input whose output has the wrong sign or orientation.
10. **Validity regime.** Check whether a model or correlation is applied outside the range in which it holds (a small-angle approximation at large angles, a laminar correlation at turbulent Reynolds numbers, an ideal-gas law near condensation, an empirical fit outside its fitted range). Evidence: an input in the code's reachable range that lies outside the stated regime, and the error against the exact or accepted value.

## Severity guidance

The severities are those defined by the skill:

- **High:** produces a wrong result under realistic inputs.
- **Medium:** produces a wrong result only under plausible edge-case inputs, or prevents reproduction of a result.
- **Low:** a latent risk that does not currently produce a wrong result.

Typical mapping:

| Defect | Severity |
|---|---|
| Unit mismatch or unconverted I/O value on the main computational path | High |
| Explicit time step that exceeds its stability limit for the default or documented parameters | High |
| Discrete update that does not conserve a conserved quantity in normal operation | High |
| Stability limit violated only for a plausible but non-default combination of parameters | Medium |
| Fractions that fail to sum to one only after clipping at an extreme input | Medium |
| Output written without its unit, so a result cannot be reproduced or reinterpreted | Medium |
| Model used near, but not beyond, the edge of its validity regime with no guard | Low |
| Unit carried only by an identifier name, with every current caller consistent | Low |

## Not defects

- **Temperature differences in degrees Celsius.** A difference of 1 °C equals a difference of 1 K, so `k * (t_hot_c - t_cold_c)` is correct. Only absolute temperatures in a nonlinear law (radiation, ideal gas, Arrhenius) require kelvin.
- **Deliberately non-dimensional formulations.** Code written in scaled variables (Reynolds number, dimensionless time) is consistent when the scaling is applied once at input and inverted once at output.
- **Unconditionally stable schemes.** Implicit Euler, Crank-Nicolson for diffusion and other implicit schemes have no explicit stability limit; a large `dt` affects accuracy, which is reported only with a concrete accuracy failure.
- **Stability enforced by the caller.** A solver documented to require `dt` within a stated limit, whose every caller in scope computes `dt` from that limit, is not a defect.
- **Normalisation to rounding.** Fractions that sum to one within a few units in the last place are correct; exact floating-point equality to one is not required.
- **Sign conventions that differ but are documented and converted.** A flux reported positive inward in one module and positive outward in another is correct when the interface converts it.

## Worked examples

### Defect 1: explicit diffusion step above its stability limit (High)

Trigger: `alpha = 1e-4` m²/s, `dx = 0.01` m, `dt = 1.0` s gives `r = alpha * dt / dx**2 = 1.0`, above the limit of 0.5. Wrong output: the highest-frequency mode is multiplied by `1 - 4r = -3` per step, so an initial spike of 1.0 on a 101-node grid alternates in sign and reaches about 3.8e8 in magnitude after 20 steps, while the exact solution decays. Fix: choose `dt` from the limit, sub-step, or use an implicit scheme.

```python
def step(u: list[float], alpha: float, dx: float, dt: float) -> list[float]:
    r = alpha * dt / dx**2  # defect: r is never checked against 0.5
    return [u[0]] + [u[i] + r * (u[i-1] - 2*u[i] + u[i+1]) for i in range(1, len(u)-1)] + [u[-1]]

# Fix
def stable_dt(alpha: float, dx: float, dt: float) -> float:
    return min(dt, 0.5 * dx**2 / alpha)
```

```typescript
function step(u: number[], alpha: number, dx: number, dt: number): number[] {
  const r = (alpha * dt) / (dx * dx); // defect: r is never checked against 0.5
  return u.map((v, i) => (i === 0 || i === u.length - 1 ? v : v + r * (u[i - 1] - 2 * v + u[i + 1])));
}

// Fix
const stableDt = (alpha: number, dx: number, dt: number): number => Math.min(dt, (0.5 * dx * dx) / alpha);
```

### Defect 2: Celsius read from input used as an absolute temperature (High)

Trigger: a surface temperature of 20 read from a CSV column documented in °C. Wrong output: the emitted radiative flux `sigma * T**4` is 9.07e-3 W/m² instead of 418.7 W/m² (a factor of about 46,000). Fix: convert to kelvin at the I/O boundary.

```python
SIGMA = 5.670e-8  # W m^-2 K^-4
def emitted_flux(row: dict[str, str]) -> float:
    t = float(row["temp_c"])        # defect: Celsius used as kelvin
    return SIGMA * t**4
# Fix: t = float(row["temp_c"]) + 273.15
```

```typescript
const SIGMA = 5.670e-8; // W m^-2 K^-4
function emittedFlux(row: Record<string, string>): number {
  const t = Number(row["temp_c"]); // defect: Celsius used as kelvin
  return SIGMA * t ** 4;
}
// Fix: const t = Number(row["temp_c"]) + 273.15;
```

### Look-alike: Celsius difference in a linear conduction law (not a defect)

Trigger considered: `t_hot_c = 80`, `t_cold_c = 20`, `k = 50` W/(m K), `area = 1` m², `length = 0.1` m. Output: 30,000 W, identical to the result in kelvin, because only the difference enters a linear law. No fix is required; record the item as checked and found correct.

```python
def conduction(k: float, area: float, length: float, t_hot_c: float, t_cold_c: float) -> float:
    return k * area * (t_hot_c - t_cold_c) / length  # correct: a difference in degC equals one in K
```

```typescript
function conduction(k: number, area: number, length: number, tHotC: number, tColdC: number): number {
  return (k * area * (tHotC - tColdC)) / length; // correct: a difference in degC equals one in K
}
```
