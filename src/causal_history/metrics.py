from __future__ import annotations

import numpy as np


def _vector(x):
    arr = np.asarray(x, dtype=np.float64)
    if arr.ndim != 1:
        raise ValueError("expected a one-dimensional vector")
    if not np.all(np.isfinite(arr)):
        raise ValueError("vector contains non-finite values")
    return arr


def donor_projection(recipient, moved, donor, eps: float = 1e-12) -> float:
    """Movement from recipient toward donor along that episode's route axis.

    0 means no movement along the route axis. 1 means full movement to the
    unpatched donor state along that axis. Values may fall outside [0, 1].
    """
    recipient = _vector(recipient)
    moved = _vector(moved)
    donor = _vector(donor)
    if recipient.shape != moved.shape or recipient.shape != donor.shape:
        raise ValueError("recipient, moved and donor must have the same shape")
    direction = donor - recipient
    denom = float(direction @ direction)
    if denom <= eps:
        raise ValueError("recipient and donor do not define a usable route axis")
    return float((moved - recipient) @ direction / denom)


def net_donor_movement(cross_route: float, same_route_control: float) -> float:
    """Frozen benchmark effect: cross-route movement minus same-route control."""
    values = np.asarray([cross_route, same_route_control], dtype=np.float64)
    if not np.all(np.isfinite(values)):
        raise ValueError("movement values must be finite")
    return float(cross_route - same_route_control)
