#!/usr/bin/env python

""" Assignment 3, Exercise 1, INF1340, Fall, 2015. DBMS

Test module for exercise3.py

"""

__author__ = "Kei'ichiro Yamamoto, Albert Tai, Niel Chah"
__email__ = "keiichiro.yamamoto@mail.utoronto.ca, albert.tai@mail.utoronto.ca, niel.chah@mail.utoronto.ca"
__copyright__ = "2015 Kei'ichiro Yamamoto, Albert Tai, Niel Chah"
__license__ = "MIT License"

#IMPORTS
import pytest
from exercise1 import selection, projection, cross_product, UnknownAttributeException


###########
# TABLES ##
###########

EMPLOYEES = [["Surname", "FirstName", "Age", "Salary"],
             ["Smith", "Mary", 25, 2000],
             ["Black", "Lucy", 40, 3000],
             ["Verdi", "Nico", 36, 4500],
             ["Smith", "Mark", 40, 3900]]

R1 = [["Employee", "Department"],
      ["Smith", "sales"],
      ["Black", "production"],
      ["White", "production"]]

R2 = [["Department", "Head"],
      ["production", "Mori"],
      ["sales", "Brown"]]


#####################
# HELPER FUNCTIONS ##
#####################
def is_equal(t1, t2):

    t1.sort()
    t2.sort()

    return t1 == t2


#####################
# FILTER FUNCTIONS ##
#####################
def filter_employees(row):
    """
    Check if employee represented by row
    is AT LEAST 30 years old and makes
    MORE THAN 3500.
    :param row: A List in the format:
        [{Surname}, {FirstName}, {Age}, {Salary}]
    :return: True if the row satisfies the condition.
    """
    return row[-2] >= 30 and row[-1] > 3500


###################
# TEST FUNCTIONS ##
###################

def test_selection():
    """
    Test select operation.
    """

    result = [["Surname", "FirstName", "Age", "Salary"],
              ["Verdi", "Nico", 36, 4500],
              ["Smith", "Mark", 40, 3900]]

    assert is_equal(result, selection(EMPLOYEES, filter_employees))

def test_selection_empty_table():
    """
    Test select operation with empty table
    """
    assert selection([], filter_employees) == None

def test_selection_result_empty():
    """
    Test select operation result with empty table
    """
    def returnNone(row):
        return row[-1] < -1
    assert selection(EMPLOYEES, returnNone) == None


def test_projection():
    """
    Test projection operation.
    """

    result = [["Surname", "FirstName"],
              ["Smith", "Mary"],
              ["Black", "Lucy"],
              ["Verdi", "Nico"],
              ["Smith", "Mark"]]

    assert is_equal(result, projection(EMPLOYEES, ["Surname", "FirstName"]))


def test_projection_empty_attributes():
    """
    Test projection operation.
    """

    result = [["Surname", "FirstName"],
              ["Smith", "Mary"],
              ["Black", "Lucy"],
              ["Verdi", "Nico"],
              ["Smith", "Mark"]]
    try:
        assert is_equal(result, projection(EMPLOYEES, []))
    except UnknownAttributeException:
        return True


def test_projection_wrong_attributes():
    """
    Test projection operation.
    """

    result = [["Surname", "FirstName"],
              ["Smith", "Mary"],
              ["Black", "Lucy"],
              ["Verdi", "Nico"],
              ["Smith", "Mark"]]
    try:
        assert is_equal(result, projection(EMPLOYEES, ["fat guy"]))
    except UnknownAttributeException:
        return True

def test_cross_product():
    """
    Test cross product operation.
    """

    result = [["Employee", "Department", "Department", "Head"],
              ["Smith", "sales", "production", "Mori"],
              ["Smith", "sales", "sales", "Brown"],
              ["Black", "production", "production", "Mori"],
              ["Black", "production", "sales", "Brown"],
              ["White", "production", "production", "Mori"],
              ["White", "production", "sales", "Brown"]]

    assert is_equal(result, cross_product(R1, R2))

def test_cross_product_result_empty():
    """
    Test cross product operation with a result empty table.
    """

    t1 = [["Surname", "FirstName"],
              ["Smith", "Mary"],
              ["Black", "Lucy"],
              ["Verdi", "Nico"],
              ["Smith", "Mark"]]
    t2 = [["Surname", "FirstName"]]

    assert cross_product(t1,t2) == None
