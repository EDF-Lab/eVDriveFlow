from shared.utils import float_to_rational
import pytest


# Positive values :
def test_float_to_rational_003() -> None:
    output = float_to_rational(0.003)
    assert output[0] == 3 and output[1] == -3


def test_float_to_rational_021() -> None:
    output = float_to_rational(0.021)
    assert output[0] == 21 and output[1] == -3


def test_float_to_rational_0321() -> None:
    output = float_to_rational(0.321)
    assert output[0] == 321 and output[1] == -3


def test_float_to_rational_1() -> None:
    output = float_to_rational(1)
    assert output[0] == 1 and output[1] == 0


def test_float_to_rational_1_3888888888888888() -> None:
    output = float_to_rational(1.3888888888888888)
    assert output[0] == 1389 and output[1] == -3


def test_float_to_rational_12() -> None:
    output = float_to_rational(12)
    assert output[0] == 12 and output[1] == 0

def test_float_to_rational_99_999() -> None:
    output = float_to_rational(99.999)
    assert output[0] == 9999 and output[1] == -2


def test_float_to_rational_123() -> None:
    output = float_to_rational(123)
    assert output[0] == 123 and output[1] == 0

def test_float_to_rational_12_201() -> None:
    output = float_to_rational(12.201)
    assert output[0] == 12201 and output[1] == -3

def test_float_to_rational_123_201() -> None:
    output = float_to_rational(123.201)
    assert output[0] == 12320 and output[1] == -2


def test_float_to_rational_3000() -> None:
    output = float_to_rational(3000)
    assert output[0] == 3000 and output[1] == 0


def test_float_to_rational_32769() -> None:
    output = float_to_rational(32769)
    assert output[0] == 3277 and output[1] == 1


def test_float_to_rational_100000() -> None:
    output = float_to_rational(100000)
    assert output[0] == 10000 and output[1] == 1


# Negative values :

def test_float_to_rational_neg_003() -> None:
    output = float_to_rational(-0.003)
    assert output[0] == -3 and output[1] == -3


def test_float_to_rational_neg_021() -> None:
    output = float_to_rational(-0.021)
    assert output[0] == -21 and output[1] == -3


def test_float_to_rational_neg_0321() -> None:
    output = float_to_rational(-0.321)
    assert output[0] == -321 and output[1] == -3


def test_float_to_rational_neg_1() -> None:
    output = float_to_rational(-1)
    assert output[0] == -1 and output[1] == 0


def test_float_to_rational_neg_1_3888888888888888() -> None:
    output = float_to_rational(-1.3888888888888888)
    assert output[0] == -1389 and output[1] == -3


def test_float_to_rational_neg_12() -> None:
    output = float_to_rational(-12)
    assert output[0] == -12 and output[1] == 0

def test_float_to_rational_neg_99_999() -> None:
    output = float_to_rational(-99.999)
    assert output[0] == -9999 and output[1] == -2


def test_float_to_rational_neg_123() -> None:
    output = float_to_rational(-123)
    assert output[0] == -123 and output[1] == 0

def test_float_to_rational_neg_12_201() -> None:
    output = float_to_rational(-12.201)
    assert output[0] == -12201 and output[1] == -3

def test_float_to_rational_neg_123_201() -> None:
    output = float_to_rational(-123.201)
    assert output[0] == -12320 and output[1] == -2


def test_float_to_rational_neg_3000() -> None:
    output = float_to_rational(-3000)
    assert output[0] == -3000 and output[1] == 0


def test_float_to_rational_32769() -> None:
    output = float_to_rational(32769)
    assert output[0] == 3277 and output[1] == 1


def test_float_to_rational_100000() -> None:
    output = float_to_rational(100000)
    assert output[0] == 10000 and output[1] == 1