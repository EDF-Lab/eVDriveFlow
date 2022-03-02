"""
.. module:: utils
   :platform: Unix
   :synopsis: A module that contains useful methods to process specific datatypes.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

from shared.xml_classes.dc import RationalNumberType as DcRationalNumberType


def rational_to_float(value) -> float:
    """Casts a RationalNumberType to a float.

    :param value: The value to cast.
    :return: float -- the cast result.
    """
    return value.value * (10 ** value.exponent)


def float_to_dc_rational(value: float) -> DcRationalNumberType:
    """Casts a float to a DcRationalNumberType.

    :param value: The value to cast.
    :return: DcRationalNumberType -- the cast result.
    """
    if value == 0:
        return DcRationalNumberType(0, 0)
    string = format(value, ".2e")
    if abs(value) < 1:
        string = string.split("e-")
    else:
        string = string.split("e+")
    try:
        value = int(string[0])
        exponent = int(string[1])
    except ValueError:
        value = int(string[0].replace('.', ''))
        exponent = int(string[1]) - 2
    return DcRationalNumberType(exponent, value)


def greater_rational(rational_1, rational_2):
    """Compares two RationalNumberType.

    :param rational_1: A RationalNumberType.
    :param rational_2: A RationalNumberType.
    :return: RationalNumberType -- the greater value.
    """
    if abs(rational_to_float(rational_1)) >= abs(rational_to_float(rational_2)):
        return rational_1
    return rational_2


def lower_rational(rational_1, rational_2):
    """Compares two RationalNumberType.

    :param rational_1: A RationalNumberType.
    :param rational_2: A RationalNumberType.
    :return: RationalNumberType -- the lower value.
    """
    if abs(rational_to_float(rational_1)) <= abs(rational_to_float(rational_2)):
        return rational_1
    return rational_2


def negative_dc_rational(value):
    """Turns a RationalNumberType negative.

    :param value: The value to change.
    :return: RationalNumberType -- the result.
    """
    return DcRationalNumberType(value.exponent, -value.value)
