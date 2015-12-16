#!/usr/bin/env python3

""" Assignment 3, Exercise 2, INF1340, Fall, 2015. DBMS

This module performs table operations on database tables
implemented as lists of lists. """

__author__ = "Kei'ichiro Yamamoto, Albert Tai, Niel Chah"
__email__ = "keiichiro.yamamoto@mail.utoronto.ca, albert.tai@mail.utoronto.ca, niel.chah@mail.utoronto.ca"
__copyright__ = "2015 Kei'ichiro Yamamoto, Albert Tai, Niel Chah"
__license__ = "MIT License"


#####################
# HELPER FUNCTIONS ##
#####################

def remove_duplicates(listoflists):
    """
    This function removes duplicates from l, where l is a List of Lists.
    :param listoflists: a List
    """

    d = {}
    result = []
    for row in listoflists:
        if tuple(row) not in d:
            result.append(row)
            d[tuple(row)] = True

    return result


class UnknownAttributeException(Exception):
    """
    Raised when attempting set operations on a table
    that does not contain the named attribute
    """
    pass


def selection(t, f):
    """
    Perform select operation on table t that satisfy condition f.

    Example:
    > R = [["A", "B", "C"], [1, 2, 3], [4, 5, 6]]
    ># Define function f that returns True iff
    > # the last element in the row is greater than 3.
    > def f(row): row[-1] > 3
    > select(R, f)
    [["A", "B", "C"], [4, 5, 6]]

    """

    return None


def projection(table, attributes):
    """
    Perform projection operation on table t
    using the attributes subset r.

    Example:
    > R = [["A", "B", "C"], [1, 2, 3], [4, 5, 6]]
    > projection(R, ["A", "C"])
    [["A", "C"], [1, 3], [4, 6]]

    """

def cross_product(t1, t2):
    """
    Return the cross-product of tables t1 and t2.

    Example:
    > R1 = [["A", "B"], [1,2], [3,4]]
    > R2 = [["C", "D"], [5,6]]
    [["A", "B", "C", "D"], [1, 2, 5, 6], [3, 4, 5, 6]]
    :param t1: First table that will be cross producted
    :param t2: Second table that will be matched to table 1

    :return: None if empty or list with result

    """
    result = [] # initalize result table
    if (t1 == [] or t2 == []):
        return None
    result += [t1[0] + t2[0]] # add the column titles together of table 1 and 2
    t1counter = 1 # counter for table 1
    for row in t1[0:-1]: # Retrieve each row of table1 starting from after column labels
        t2counter = 1 # counter for table 2
        for row in t2[0:-1]: # Retrieve each row of table2 starting from after column labels
            result += [t1[t1counter] + t2[t2counter]] # add it to the result table
            t2counter += 1 # increment the counter for table 2
        t1counter += 1 # increment the counter for table 1
    if (result != []):
        return result
    return None

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

