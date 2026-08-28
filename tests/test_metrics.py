import pytest

from causal_history.metrics import donor_projection, net_donor_movement


def test_projection_endpoints():
    recipient = [0.0, 0.0]
    donor = [2.0, 0.0]
    assert donor_projection(recipient, recipient, donor) == pytest.approx(0.0)
    assert donor_projection(recipient, donor, donor) == pytest.approx(1.0)
    assert donor_projection(recipient, [1.0, 0.0], donor) == pytest.approx(0.5)


def test_same_route_subtraction():
    assert net_donor_movement(0.70, 0.05) == pytest.approx(0.65)


def test_zero_axis_fails():
    with pytest.raises(ValueError):
        donor_projection([1.0], [1.0], [1.0])
