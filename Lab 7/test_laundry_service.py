from hypothesis import given, strategies as st
import pytest

from laundry_service import (
    parse_order,
    weight_average,
    payable_charge
)

# 1. PARSE ORDER TESTS

@given(st.text() | st.none())
def test_parse_order_no_crash(s):
    try:
        result = parse_order(s)
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], str)
        assert isinstance(result[1], float)
        assert result[1] >= 0
    except (ValueError, TypeError):
        pass


@given(
    st.text(min_size=1).filter(
        lambda x: ':' not in x
    )
)
def test_parse_order_missing_separator(s):
    with pytest.raises(ValueError):
        parse_order(s)


@given(
    st.text(min_size=1).filter(
        lambda x: ':' not in x and x.strip() != ''
    ),
    st.floats(
        min_value=0,
        max_value=10000,
        allow_nan=False,
        allow_infinity=False
    )
)
def test_parse_order_valid(garment, kg):
    result = parse_order(f"{garment}:{kg}")
    assert result[0] == garment.strip().title()
    assert result[1] == kg

# 2. WEIGHT AVERAGE TESTS

@given(st.text() | st.none())
def test_weight_average_no_crash(s):
    try:
        result = weight_average(s)
        assert isinstance(result, int)
    except (ValueError, TypeError):
        pass


@given(
    st.lists(
        st.integers(min_value=0),
        min_size=1
    )
)
def test_weight_average_valid(values):
    csv = ','.join(str(x) for x in values)
    expected = sum(values) // len(values)
    assert weight_average(csv) == expected


@given(st.integers(min_value=0))
def test_weight_average_single_value(value):
    assert weight_average(str(value)) == value

# 3. PAYABLE CHARGE TESTS

@given(st.text() | st.none())
def test_payable_charge_no_crash(s):
    try:
        result = payable_charge(s)
        assert isinstance(result, (int, float))
        assert result >= 0
    except (ValueError, TypeError):
        pass


@given(
    st.floats(
        min_value=0,
        max_value=100000,
        allow_nan=False,
        allow_infinity=False
    ),
    st.floats(
        min_value=0,
        max_value=100000,
        allow_nan=False,
        allow_infinity=False
    )
)
def test_payable_charge_valid(charge, discount):
    result = payable_charge(f"{charge}|{discount}")
    expected = max(charge * 1.18 - discount, 0)
    assert result == pytest.approx(expected)


@given(
    st.floats(
        min_value=0,
        max_value=100000,
        allow_nan=False,
        allow_infinity=False
    )
)
def test_payable_charge_never_negative(charge):
    result = payable_charge(f"{charge}|0")
    assert result >= 0
