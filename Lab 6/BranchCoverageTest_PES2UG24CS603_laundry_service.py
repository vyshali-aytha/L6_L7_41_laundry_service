
import pytest

from laundry_service import (
    extra_weight_charge,
    order_acceptable,
    dropoff_status
)


# ==========================================
# EXTRA WEIGHT CHARGE
# ==========================================

def test_unknown_garment():
    with pytest.raises(ValueError):
        extra_weight_charge("unknown", 5, "standard", False)


def test_negative_weight():
    with pytest.raises(ValueError):
        extra_weight_charge("regular", -1, "standard", False)


def test_member_regular():
    assert extra_weight_charge("regular", 6, "standard", True) == 0


def test_non_member_regular():
    assert extra_weight_charge("regular", 8, "standard", False) == 90


def test_member_bedding():
    assert extra_weight_charge("bedding", 10, "standard", True) == 60


def test_no_extra_weight():
    assert extra_weight_charge("regular", 5, "standard", False) == 0


def test_standard_speed():
    assert extra_weight_charge("regular", 8, "standard", False) == 90


def test_express_speed():
    assert extra_weight_charge("regular", 8, "express", False) == 150


def test_extra_weight_above_10_standard():
    assert extra_weight_charge("regular", 16, "standard", False) == 495


def test_extra_weight_above_10_express():
    assert extra_weight_charge("regular", 16, "express", False) == 825


# ==========================================
# ORDER ACCEPTABILITY
# ==========================================

def test_delicate_order_accepted():
    assert order_acceptable(10, 5, True) is True


def test_delicate_order_rejected():
    assert order_acceptable(10, 6, True) is False


def test_non_delicate_overweight():
    assert order_acceptable(26, 20, False) is False


def test_non_delicate_within_weight():
    assert order_acceptable(20, 40, False) is True


def test_non_delicate_too_many_items():
    assert order_acceptable(20, 41, False) is False


# ==========================================
# DROPOFF STATUS
# ==========================================

def test_bedding_cutoff():
    assert dropoff_status(90, True, False) == "accepted"


def test_no_bedding_cutoff():
    assert dropoff_status(60, False, False) == "accepted"


def test_express_cutoff():
    assert dropoff_status(90, False, True) == "accepted"


def test_bedding_express_cutoff():
    assert dropoff_status(120, True, True) == "accepted"


def test_late_dropoff():
    assert dropoff_status(45, False, False) == "late"


def test_rejected_dropoff():
    assert dropoff_status(30, False, False) == "rejected"
