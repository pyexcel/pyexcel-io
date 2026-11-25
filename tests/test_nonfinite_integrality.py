import pytest

from pyexcel_io.service import has_no_digits_in_float


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_nonfinite_values_are_not_eligible_for_integer_conversion(value):
    assert has_no_digits_in_float(value) is False


@pytest.mark.parametrize(
    "value, expected",
    [
        (0.0, True),
        (-0.0, True),
        (1.0, True),
        (-2.0, True),
        (1.25, False),
        (-1.25, False),
        (1e-300, False),
        (1e300, True),
        (42, True),
        (10**400, True),
    ],
)
def test_finite_values_retain_integer_detection(value, expected):
    assert has_no_digits_in_float(value) is expected
