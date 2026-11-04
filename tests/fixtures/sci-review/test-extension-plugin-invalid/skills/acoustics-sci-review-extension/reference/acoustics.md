# Acoustics

This reference supports the acoustician perspective. Section 1 states the checks independently of language. Section 2 gives worked examples in Python and TypeScript, each pairing a defect with a look-alike that is correct and must not be flagged.

## 1. Language-neutral checks

1. **Level combination.** Levels in dB combine only through power quantities: `L_total = 10 log10(sum 10^(L_i / 10))`. Direct addition, subtraction or arithmetic mean of dB values is a defect, except where the operation is a gain applied to a level (adding a gain in dB to a level in dB is correct).
2. **Reference values.** Sound pressure level uses p_ref = 20 uPa = 2e-5 Pa. Sound power level uses W_ref = 1 pW = 1e-12 W. Sound intensity level uses I_ref = 1e-12 W/m^2. A pressure level referenced to 1e-12, or a power level referenced to 2e-5, is a defect.
3. **Field and power factors.** `20 log10(x / x_ref)` for field quantities (pressure, voltage, amplitude). `10 log10(x / x_ref)` for power quantities (power, intensity, mean-square pressure).
4. **Sampling rate.** Frequencies derived from a signal use the sampling rate read with that signal. The frequency of FFT bin k is `k * fs / N`. Any frequency at or above `fs / 2` is not representable.
5. **Filter normalisation.** Libraries differ: some take cut-offs in Hz with a separate `fs` argument, others take cut-offs normalised to Nyquist (0 to 1). A cut-off in Hz passed where a normalised value is expected is a defect.
6. **A-weighting.** The weighting is a set of gains in dB per frequency. It is added to band levels in the dB domain, or applied as a filter to the time signal, once. The result is labelled dB(A).
7. **Octave bands.** With base-ten ratio G = 10^(3/10), the edges of a 1/b-octave band with exact centre f_m are `f_m * G^(-1/(2b))` and `f_m * G^(1/(2b))`. Edges are multiplicative, never additive.

## 2. Worked examples

### 2.1 Python: level combination (defect)

```python
import numpy as np


def total_level(levels_db):
    return sum(levels_db)  # 60 dB + 60 dB reported as 120 dB
```

Two equal sources of 60 dB give 63.0 dB, not 120 dB. Finding: decibel arithmetic, check 1.

### 2.2 Python: level combination (look-alike, correct)

```python
import numpy as np


def total_level(levels_db):
    return 10 * np.log10(np.sum(10 ** (np.asarray(levels_db) / 10)))


def apply_gain(level_db, gain_db):
    return level_db + gain_db  # a gain added to a level: correct
```

Do not flag `apply_gain`: adding a gain in dB to a level in dB is a multiplication in the linear domain.

### 2.3 Python: sampling rate and filter normalisation (defect)

```python
import soundfile as sf
from scipy import signal

x, fs = sf.read("recording.wav")
b, a = signal.butter(4, 8000 / 22050, btype="low")  # assumes fs = 44100
```

If the file is sampled at 48 kHz, the cut-off is 8707 Hz rather than 8000 Hz. Finding: sample rate, checks 4 and 5.

### 2.4 Python: sampling rate (look-alike, correct)

```python
import soundfile as sf
from scipy import signal

x, fs = sf.read("recording.wav")
sos = signal.butter(4, 8000, btype="low", fs=fs, output="sos")
```

Do not flag: the cut-off is in Hz and `fs` is passed explicitly from the file.

### 2.5 TypeScript: reference value (defect)

```typescript
import { rms } from "web-audio-utils";

export function splDb(pressurePa: Float32Array): number {
  return 20 * Math.log10(rms(pressurePa) / 1e-12); // power reference used for pressure
}
```

The level is inflated by about 146 dB. Finding: reference values, check 2.

### 2.6 TypeScript: reference value (look-alike, correct)

```typescript
const P_REF_PA = 2e-5;
const W_REF_W = 1e-12;

export const splDb = (pRms: number): number => 20 * Math.log10(pRms / P_REF_PA);
export const swlDb = (powerW: number): number => 10 * Math.log10(powerW / W_REF_W);
```

Do not flag: each level uses its own reference and its own factor.

### 2.7 TypeScript: octave-band edges (defect and look-alike)

```typescript
// Defect: additive edges.
const edges = (fc: number): [number, number] => [fc - fc / 3, fc + fc / 3];

// Correct: multiplicative base-ten edges for a full octave.
const G = 10 ** (3 / 10);
const octaveEdges = (fm: number): [number, number] => [fm * G ** -0.5, fm * G ** 0.5];
```

Flag the first function under check 7; do not flag the second.
