#!/usr/bin/env python3

""" Module to test papers.py  """

__author__ = "Kei'ichiro Yamamoto, Albert Tai, Niel Chah"
__email__ = "keiichiro.yamamoto@mail.utoronto.ca, albert.tai@mail.utoronto.ca, niel.chah@mail.utoronto.ca"
__copyright__ = "2015 Kei'ichiro Yamamoto, Albert Tai, Niel Chah"
__license__ = "MIT License"

__status__ = "Prototype"

# imports one per line
import pytest
import os
from exercise2 import decide, is_more_than_x_years_ago, valid_passport_format, valid_visa_format, valid_date_format

if os.name == 'nt':
    DIR = "test_json\\"  # Windows
else:
    DIR = "test_jsons/"  # other (unix)

# DIR = "test_jsons/"
os.chdir(DIR)


def test_returning():
    """
    Travellers are returning to KAN.
    """
    assert decide("test_returning_citizen.json", "countries.json") == \
           ["Accept", "Accept", "Quarantine"]


def test_further_cases():
    """
    1. Traveller 1 = Reject because Rule 1. traveller's record is incomplete or malformed
    2. Traveller 2 = Reject because Rule 1. traveller's birth date record is invalid 1936-13-25
    3. Traveller 3 = Reject because Rule 1. traveller's passport information is not included
    4. Traveller 4 = Reject because Rule 2. traveller is from an unknown country
    5. Traveller 5 = Reject because Rule 4. traveller visa is out of date
    6. Traveller 6 = Reject because Rule 4. traveller has an invalid Visa number
    """
    assert decide("exercise2_further_tests.json", "countries.json") == \
           ["Reject", "Reject", "Reject", "Reject", "Reject", "Reject"]


def test_x_years_ago():
    """
    Check if if inputs are valid for x years ago
    """
    try:
        assert is_more_than_x_years_ago(3, "2012-02-27")
    except True:
        return True

    try:
        assert is_more_than_x_years_ago(4, 2015 - 05 - 28)
    except TypeError:
        return True

    try:
        assert is_more_than_x_years_ago(3, "2019-02-27")
    except AssertionError:
        return True


def test_valid_passport_format():
    """
    Tests to see if Invalid formats are accepted
    """
    try:
        assert valid_passport_format("FWO9A-B8MDF-TGXW5-H49SO-HI5VE")
    except True:
        return True

    try:
        assert valid_passport_format(9083 - 9876 - 4659 - 3845 - 9345 - 3845)
    except TypeError:
        return True

    try:
        assert valid_passport_format("asdfadsf")
    except AssertionError:
        return True


def test_valid_visa_format():
    """
    Test to see if the visa is accepted
    """

    try:
        assert valid_visa_format("CKC6X-XSMVA")
    except True:
        return True

    try:
        assert valid_visa_format(99999 - 9999)
    except TypeError:
        return True

    try:
        assert valid_visa_format("nopee-nopee")
    except AssertionError:
        return True


def test_correct_date_format():
    """
    Test to see if different dates are accepted.
    """
    try:
        assert valid_date_format("2015-02-22")
    except True:
        return True

    try:
        assert valid_date_format("2012-30-40")
    except False:
        return True

    try:
        assert valid_date_format(2015 - 02 - 22)
    except TypeError:
        return True


def test_correct_visa_format():
    """
    Test to see if the visa is accepted
    """

    try:
        assert valid_visa_format("CFR6X-XSMVA")
    except True:
        return True

    try:
        assert valid_visa_format(99999 - 9999)
    except TypeError:
        return True
