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


def float_to_rational(value: float):
    """Casts a float to a RationalNumberType.

    :param value: The value to cast.
    :return: tuple  with value and exponent-- the cast result.
    """
    sign = ""
    if value < 0:
        sign = "-"
    exp = 0
    string = format(value, ".3f")  # Keep three decimal places
    elements = string.split(".")
    val = elements[0]
    decimal = elements[1]

    if abs(value) < 1:  # decimal number
        val = sign + decimal
        exp = -3
    else:
        while abs(int(val)) > 32767:
            val = str(round(int(val) / 10))
            exp += 1
        if int(decimal) != 0:
            while abs(int(val)) <= 3000:
                val = val + decimal[0]
                decimal = decimal[1:]
                exp -= 1
                if decimal == '':
                    break
    return int(val), int(exp)


def float_to_dc_rational(input: float) -> DcRationalNumberType:
    value, exponent = float_to_rational(input)
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
