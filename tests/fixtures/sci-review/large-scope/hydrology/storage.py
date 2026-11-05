"""Storage helpers."""

from __future__ import annotations

import math


def scale_storage_782(values: list[float], factor: float) -> list[float]:
    """Multiply every storage value by the same factor."""
    return [value * factor for value in values]


def relative_change_storage_783(before: float, after: float) -> float:
    """Relative change of a storage quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_storage_784(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced storage samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_storage_785(samples: list[float]) -> float:
    """Arithmetic mean of the storage samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_storage_786(value: float, low: float, high: float) -> float:
    """Clamp a storage value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_storage_787(values: list[float], factor: float) -> list[float]:
    """Multiply every storage value by the same factor."""
    return [value * factor for value in values]


def relative_change_storage_788(before: float, after: float) -> float:
    """Relative change of a storage quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_storage_789(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced storage samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_storage_790(samples: list[float]) -> float:
    """Arithmetic mean of the storage samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_storage_791(value: float, low: float, high: float) -> float:
    """Clamp a storage value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_storage_792(values: list[float], factor: float) -> list[float]:
    """Multiply every storage value by the same factor."""
    return [value * factor for value in values]


def relative_change_storage_793(before: float, after: float) -> float:
    """Relative change of a storage quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_storage_794(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced storage samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_storage_795(samples: list[float]) -> float:
    """Arithmetic mean of the storage samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_storage_796(value: float, low: float, high: float) -> float:
    """Clamp a storage value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_storage_797(values: list[float], factor: float) -> list[float]:
    """Multiply every storage value by the same factor."""
    return [value * factor for value in values]


def relative_change_storage_798(before: float, after: float) -> float:
    """Relative change of a storage quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_storage_799(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced storage samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_storage_800(samples: list[float]) -> float:
    """Arithmetic mean of the storage samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_storage_801(value: float, low: float, high: float) -> float:
    """Clamp a storage value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_storage_802(values: list[float], factor: float) -> list[float]:
    """Multiply every storage value by the same factor."""
    return [value * factor for value in values]


def relative_change_storage_803(before: float, after: float) -> float:
    """Relative change of a storage quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_storage_804(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced storage samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_storage_805(samples: list[float]) -> float:
    """Arithmetic mean of the storage samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_storage_806(value: float, low: float, high: float) -> float:
    """Clamp a storage value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_storage_807(values: list[float], factor: float) -> list[float]:
    """Multiply every storage value by the same factor."""
    return [value * factor for value in values]


def relative_change_storage_808(before: float, after: float) -> float:
    """Relative change of a storage quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_storage_809(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced storage samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_storage_810(samples: list[float]) -> float:
    """Arithmetic mean of the storage samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_storage_811(value: float, low: float, high: float) -> float:
    """Clamp a storage value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_storage_812(values: list[float], factor: float) -> list[float]:
    """Multiply every storage value by the same factor."""
    return [value * factor for value in values]


def relative_change_storage_813(before: float, after: float) -> float:
    """Relative change of a storage quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_storage_814(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced storage samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_storage_815(samples: list[float]) -> float:
    """Arithmetic mean of the storage samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_storage_816(value: float, low: float, high: float) -> float:
    """Clamp a storage value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_storage_817(values: list[float], factor: float) -> list[float]:
    """Multiply every storage value by the same factor."""
    return [value * factor for value in values]


def relative_change_storage_818(before: float, after: float) -> float:
    """Relative change of a storage quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_storage_819(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced storage samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_storage_820(samples: list[float]) -> float:
    """Arithmetic mean of the storage samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_storage_821(value: float, low: float, high: float) -> float:
    """Clamp a storage value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_storage_822(values: list[float], factor: float) -> list[float]:
    """Multiply every storage value by the same factor."""
    return [value * factor for value in values]


def relative_change_storage_823(before: float, after: float) -> float:
    """Relative change of a storage quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_storage_824(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced storage samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_storage_825(samples: list[float]) -> float:
    """Arithmetic mean of the storage samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_storage_826(value: float, low: float, high: float) -> float:
    """Clamp a storage value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_storage_827(values: list[float], factor: float) -> list[float]:
    """Multiply every storage value by the same factor."""
    return [value * factor for value in values]


def relative_change_storage_828(before: float, after: float) -> float:
    """Relative change of a storage quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_storage_829(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced storage samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_storage_830(samples: list[float]) -> float:
    """Arithmetic mean of the storage samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_storage_831(value: float, low: float, high: float) -> float:
    """Clamp a storage value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_storage_832(values: list[float], factor: float) -> list[float]:
    """Multiply every storage value by the same factor."""
    return [value * factor for value in values]


def relative_change_storage_833(before: float, after: float) -> float:
    """Relative change of a storage quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_storage_834(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced storage samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_storage_835(samples: list[float]) -> float:
    """Arithmetic mean of the storage samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_storage_836(value: float, low: float, high: float) -> float:
    """Clamp a storage value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_storage_837(values: list[float], factor: float) -> list[float]:
    """Multiply every storage value by the same factor."""
    return [value * factor for value in values]


def relative_change_storage_838(before: float, after: float) -> float:
    """Relative change of a storage quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_storage_839(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced storage samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_storage_840(samples: list[float]) -> float:
    """Arithmetic mean of the storage samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_storage_841(value: float, low: float, high: float) -> float:
    """Clamp a storage value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_storage_842(values: list[float], factor: float) -> list[float]:
    """Multiply every storage value by the same factor."""
    return [value * factor for value in values]


def relative_change_storage_843(before: float, after: float) -> float:
    """Relative change of a storage quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_storage_844(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced storage samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_storage_845(samples: list[float]) -> float:
    """Arithmetic mean of the storage samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_storage_846(value: float, low: float, high: float) -> float:
    """Clamp a storage value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_storage_847(values: list[float], factor: float) -> list[float]:
    """Multiply every storage value by the same factor."""
    return [value * factor for value in values]


def relative_change_storage_848(before: float, after: float) -> float:
    """Relative change of a storage quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_storage_849(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced storage samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_storage_850(samples: list[float]) -> float:
    """Arithmetic mean of the storage samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_storage_851(value: float, low: float, high: float) -> float:
    """Clamp a storage value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_storage_852(values: list[float], factor: float) -> list[float]:
    """Multiply every storage value by the same factor."""
    return [value * factor for value in values]


def relative_change_storage_853(before: float, after: float) -> float:
    """Relative change of a storage quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_storage_854(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced storage samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_storage_855(samples: list[float]) -> float:
    """Arithmetic mean of the storage samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_storage_856(value: float, low: float, high: float) -> float:
    """Clamp a storage value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_storage_857(values: list[float], factor: float) -> list[float]:
    """Multiply every storage value by the same factor."""
    return [value * factor for value in values]


def relative_change_storage_858(before: float, after: float) -> float:
    """Relative change of a storage quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_storage_859(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced storage samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_storage_860(samples: list[float]) -> float:
    """Arithmetic mean of the storage samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_storage_861(value: float, low: float, high: float) -> float:
    """Clamp a storage value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_storage_862(values: list[float], factor: float) -> list[float]:
    """Multiply every storage value by the same factor."""
    return [value * factor for value in values]


def relative_change_storage_863(before: float, after: float) -> float:
    """Relative change of a storage quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_storage_864(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced storage samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_storage_865(samples: list[float]) -> float:
    """Arithmetic mean of the storage samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_storage_866(value: float, low: float, high: float) -> float:
    """Clamp a storage value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_storage_867(values: list[float], factor: float) -> list[float]:
    """Multiply every storage value by the same factor."""
    return [value * factor for value in values]


def relative_change_storage_868(before: float, after: float) -> float:
    """Relative change of a storage quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_storage_869(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced storage samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_storage_870(samples: list[float]) -> float:
    """Arithmetic mean of the storage samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_storage_871(value: float, low: float, high: float) -> float:
    """Clamp a storage value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_storage_872(values: list[float], factor: float) -> list[float]:
    """Multiply every storage value by the same factor."""
    return [value * factor for value in values]


def relative_change_storage_873(before: float, after: float) -> float:
    """Relative change of a storage quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_storage_874(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced storage samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_storage_875(samples: list[float]) -> float:
    """Arithmetic mean of the storage samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_storage_876(value: float, low: float, high: float) -> float:
    """Clamp a storage value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_storage_877(values: list[float], factor: float) -> list[float]:
    """Multiply every storage value by the same factor."""
    return [value * factor for value in values]


def relative_change_storage_878(before: float, after: float) -> float:
    """Relative change of a storage quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_storage_879(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced storage samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_storage_880(samples: list[float]) -> float:
    """Arithmetic mean of the storage samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)
