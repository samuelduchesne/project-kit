"""Wind helpers."""

from __future__ import annotations

import math


def scale_wind_192(values: list[float], factor: float) -> list[float]:
    """Multiply every wind value by the same factor."""
    return [value * factor for value in values]


def relative_change_wind_193(before: float, after: float) -> float:
    """Relative change of a wind quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_wind_194(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced wind samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_wind_195(samples: list[float]) -> float:
    """Arithmetic mean of the wind samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_wind_196(value: float, low: float, high: float) -> float:
    """Clamp a wind value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_wind_197(values: list[float], factor: float) -> list[float]:
    """Multiply every wind value by the same factor."""
    return [value * factor for value in values]


def relative_change_wind_198(before: float, after: float) -> float:
    """Relative change of a wind quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_wind_199(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced wind samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_wind_200(samples: list[float]) -> float:
    """Arithmetic mean of the wind samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_wind_201(value: float, low: float, high: float) -> float:
    """Clamp a wind value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_wind_202(values: list[float], factor: float) -> list[float]:
    """Multiply every wind value by the same factor."""
    return [value * factor for value in values]


def relative_change_wind_203(before: float, after: float) -> float:
    """Relative change of a wind quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_wind_204(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced wind samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_wind_205(samples: list[float]) -> float:
    """Arithmetic mean of the wind samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_wind_206(value: float, low: float, high: float) -> float:
    """Clamp a wind value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_wind_207(values: list[float], factor: float) -> list[float]:
    """Multiply every wind value by the same factor."""
    return [value * factor for value in values]


def relative_change_wind_208(before: float, after: float) -> float:
    """Relative change of a wind quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_wind_209(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced wind samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_wind_210(samples: list[float]) -> float:
    """Arithmetic mean of the wind samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_wind_211(value: float, low: float, high: float) -> float:
    """Clamp a wind value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_wind_212(values: list[float], factor: float) -> list[float]:
    """Multiply every wind value by the same factor."""
    return [value * factor for value in values]


def relative_change_wind_213(before: float, after: float) -> float:
    """Relative change of a wind quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_wind_214(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced wind samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_wind_215(samples: list[float]) -> float:
    """Arithmetic mean of the wind samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_wind_216(value: float, low: float, high: float) -> float:
    """Clamp a wind value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_wind_217(values: list[float], factor: float) -> list[float]:
    """Multiply every wind value by the same factor."""
    return [value * factor for value in values]


def relative_change_wind_218(before: float, after: float) -> float:
    """Relative change of a wind quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_wind_219(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced wind samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_wind_220(samples: list[float]) -> float:
    """Arithmetic mean of the wind samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_wind_221(value: float, low: float, high: float) -> float:
    """Clamp a wind value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_wind_222(values: list[float], factor: float) -> list[float]:
    """Multiply every wind value by the same factor."""
    return [value * factor for value in values]


def relative_change_wind_223(before: float, after: float) -> float:
    """Relative change of a wind quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_wind_224(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced wind samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_wind_225(samples: list[float]) -> float:
    """Arithmetic mean of the wind samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_wind_226(value: float, low: float, high: float) -> float:
    """Clamp a wind value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_wind_227(values: list[float], factor: float) -> list[float]:
    """Multiply every wind value by the same factor."""
    return [value * factor for value in values]


def relative_change_wind_228(before: float, after: float) -> float:
    """Relative change of a wind quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_wind_229(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced wind samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_wind_230(samples: list[float]) -> float:
    """Arithmetic mean of the wind samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_wind_231(value: float, low: float, high: float) -> float:
    """Clamp a wind value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_wind_232(values: list[float], factor: float) -> list[float]:
    """Multiply every wind value by the same factor."""
    return [value * factor for value in values]


def relative_change_wind_233(before: float, after: float) -> float:
    """Relative change of a wind quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_wind_234(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced wind samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_wind_235(samples: list[float]) -> float:
    """Arithmetic mean of the wind samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_wind_236(value: float, low: float, high: float) -> float:
    """Clamp a wind value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_wind_237(values: list[float], factor: float) -> list[float]:
    """Multiply every wind value by the same factor."""
    return [value * factor for value in values]


def relative_change_wind_238(before: float, after: float) -> float:
    """Relative change of a wind quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_wind_239(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced wind samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_wind_240(samples: list[float]) -> float:
    """Arithmetic mean of the wind samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_wind_241(value: float, low: float, high: float) -> float:
    """Clamp a wind value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_wind_242(values: list[float], factor: float) -> list[float]:
    """Multiply every wind value by the same factor."""
    return [value * factor for value in values]


def relative_change_wind_243(before: float, after: float) -> float:
    """Relative change of a wind quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_wind_244(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced wind samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_wind_245(samples: list[float]) -> float:
    """Arithmetic mean of the wind samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_wind_246(value: float, low: float, high: float) -> float:
    """Clamp a wind value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_wind_247(values: list[float], factor: float) -> list[float]:
    """Multiply every wind value by the same factor."""
    return [value * factor for value in values]


def relative_change_wind_248(before: float, after: float) -> float:
    """Relative change of a wind quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_wind_249(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced wind samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_wind_250(samples: list[float]) -> float:
    """Arithmetic mean of the wind samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_wind_251(value: float, low: float, high: float) -> float:
    """Clamp a wind value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_wind_252(values: list[float], factor: float) -> list[float]:
    """Multiply every wind value by the same factor."""
    return [value * factor for value in values]


def relative_change_wind_253(before: float, after: float) -> float:
    """Relative change of a wind quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_wind_254(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced wind samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_wind_255(samples: list[float]) -> float:
    """Arithmetic mean of the wind samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_wind_256(value: float, low: float, high: float) -> float:
    """Clamp a wind value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_wind_257(values: list[float], factor: float) -> list[float]:
    """Multiply every wind value by the same factor."""
    return [value * factor for value in values]


def relative_change_wind_258(before: float, after: float) -> float:
    """Relative change of a wind quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_wind_259(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced wind samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_wind_260(samples: list[float]) -> float:
    """Arithmetic mean of the wind samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_wind_261(value: float, low: float, high: float) -> float:
    """Clamp a wind value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_wind_262(values: list[float], factor: float) -> list[float]:
    """Multiply every wind value by the same factor."""
    return [value * factor for value in values]


def relative_change_wind_263(before: float, after: float) -> float:
    """Relative change of a wind quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_wind_264(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced wind samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_wind_265(samples: list[float]) -> float:
    """Arithmetic mean of the wind samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_wind_266(value: float, low: float, high: float) -> float:
    """Clamp a wind value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_wind_267(values: list[float], factor: float) -> list[float]:
    """Multiply every wind value by the same factor."""
    return [value * factor for value in values]


def relative_change_wind_268(before: float, after: float) -> float:
    """Relative change of a wind quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_wind_269(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced wind samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_wind_270(samples: list[float]) -> float:
    """Arithmetic mean of the wind samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_wind_271(value: float, low: float, high: float) -> float:
    """Clamp a wind value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_wind_272(values: list[float], factor: float) -> list[float]:
    """Multiply every wind value by the same factor."""
    return [value * factor for value in values]


def relative_change_wind_273(before: float, after: float) -> float:
    """Relative change of a wind quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_wind_274(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced wind samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_wind_275(samples: list[float]) -> float:
    """Arithmetic mean of the wind samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_wind_276(value: float, low: float, high: float) -> float:
    """Clamp a wind value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_wind_277(values: list[float], factor: float) -> list[float]:
    """Multiply every wind value by the same factor."""
    return [value * factor for value in values]


def relative_change_wind_278(before: float, after: float) -> float:
    """Relative change of a wind quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_wind_279(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced wind samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_wind_280(samples: list[float]) -> float:
    """Arithmetic mean of the wind samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_wind_281(value: float, low: float, high: float) -> float:
    """Clamp a wind value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_wind_282(values: list[float], factor: float) -> list[float]:
    """Multiply every wind value by the same factor."""
    return [value * factor for value in values]


def relative_change_wind_283(before: float, after: float) -> float:
    """Relative change of a wind quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_wind_284(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced wind samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_wind_285(samples: list[float]) -> float:
    """Arithmetic mean of the wind samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_wind_286(value: float, low: float, high: float) -> float:
    """Clamp a wind value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))
