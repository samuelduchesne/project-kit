"""Reproduction check for py-gap-fill-before-split.

The training part of a chronological split must not depend on the values of
the test part. Two records that differ only after the cut must give the same
training data.
"""

from _common import failed, passed, setup

setup()
from limno.calibrate import chronological_split  # noqa: E402

record = [10.0, 10.5, 11.0, 11.5, None, None, None, None, 14.0, 14.5]
other = list(record)
other[8] = 20.0
first = chronological_split(record, 0.5)
second = chronological_split(other, 0.5)
if first.train != second.train:
    failed(f"training data {first.train} changes to {second.train} when a test value after the cut changes")
passed(f"training data {first.train} independent of the test part")
