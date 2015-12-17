#!/usr/bin/env python3

""" Assignment 3, Exercise 2, INF1340, Fall, 2015. Kanadia

Computer-based immigration office for Kanadia

"""

__author__ = "Kei'ichiro Yamamoto, Albert Tai, Niel Chah"
__email__ = "keiichiro.yamamoto@mail.utoronto.ca, albert.tai@mail.utoronto.ca, niel.chah@mail.utoronto.ca"
__copyright__ = "2015 Kei'ichiro Yamamoto, Albert Tai, Niel Chah"
__license__ = "MIT License"

import re
import datetime
import json

######################
## global constants ##
######################
REQUIRED_FIELDS = ["passport", "first_name", "last_name",
                   "birth_date", "home", "entry_reason", "from"]
ADDITIONAL_FIELDS = ["visa_location", "visa"]

# Sample Valid Visa
valid_visa = [
  {
    "passport": "FWO9A-B8MDF-TGXW5-H49SO-HI5VE",
    "first_name": "VICKI",
    "last_name": "NOYES",
    "birth_date": "1969-12-11",
    "home": {
      "city": "a",
      "region": "a",
      "country": "III"
    },
    "entry_reason": "visit",
    "visa": {
      "date": "2012-12-31",
      "code": "CFR6X-XSMVA"
    },
    "from": {
      "city": "a",
      "region": "a",
      "country": "JIK"
    }
  }
]

######################
## global variables ##
######################
'''
countries:
dictionary mapping country codes (lowercase strings) to dictionaries
containing the following keys:
"code","name","visitor_visa_required",
"transit_visa_required","medical_advisory"
'''
COUNTRIES = None


#####################
# HELPER FUNCTIONS ##
#####################
def is_more_than_x_years_ago(x, date_string):
    """
    Check if date is less than x years ago.

    :param x: int representing years
    :param date_string: a date string in format "YYYY-mm-dd"
    :return: True if date is less than x years ago; False otherwise.
    """

    now = datetime.datetime.now()
    x_years_ago = now.replace(year=now.year - x)
    date = datetime.datetime.strptime(date_string, '%Y-%m-%d')

    return (date - x_years_ago).total_seconds() < 0


def valid_passport_format(passport_number):
    """
    Checks whether a passport number is five sets of five alpha-number characters separated by dashes
    :param passport_number: alpha-numeric string
    :return: Boolean; True if the format is valid, False otherwise
    """
    # passport_number matching is case-insensitive as per assignment outline
    passport_regex = re.compile('\w\w\w\w\w-\w\w\w\w\w-\w\w\w\w\w-\w\w\w\w\w-\w\w\w\w\w' , re.IGNORECASE)
    passport_match = passport_regex.match(passport_number)

    # A proper passport_number is only 29 chars, otherwise RE matching would work when it should be False
    if len(passport_number) > 29 or passport_match is None:
        return False
    else:
        return True


def valid_visa_format(visa_code):
    """
    Checks whether a visa code is two groups of five alphanumeric characters
    :param visa_code: alphanumeric string
    :return: Boolean; True if the format is valid, False otherwise
    """
    # Regex matching is case-insensitive as per assignment outline
    visa_regex = re.compile('\w\w\w\w\w-\w\w\w\w\w', re.IGNORECASE)
    visa_match = visa_regex.match(visa_code)

    # A proper visa_code is only 11 chars, otherwise RE matching would work when it should be False
    if len(visa_code) > 11 or visa_match is None:
        return False
    else:
        return True


def valid_date_format(date_string):
    """
    Checks whether a date has the format YYYY-mm-dd in numbers
    :param date_string: date to be checked
    :return: Boolean True if the format is valid, False otherwise
    """
    date_regex = re.compile('\d\d\d\d-[0-1]\d-[0-3]\d')
    date_match = date_regex.match(date_string)

    # A proper date time is only 10 chars, otherwise RE matching would work when it should be False
    # Checking for valid MM and DD values - a more comprehensive MM-DD check requires more code
    if (len(date_string) > 10
            or date_match is None
            or int(date_string[5:7]) > 12
            or int(date_string[8:10]) > 31):  # legal under https://www.python.org/dev/peps/pep-0008/#indentation
        return False
    else:
        return True


def decide(input_file, countries_file):
    """
    Decides whether a traveller's entry into Kanadia should be accepted

    :param input_file: The name of a JSON formatted file that contains
        cases to decide
    :param countries_file: The name of a JSON formatted file that contains
        country data, such as whether an entry or transit visa is required,
        and whether there is currently a medical advisory
    :return: List of strings. Possible values of strings are:
        "Accept", "Reject", and "Quarantine"
    """
    """
    Rules for categorizing travellers:
    1. If the required information for an entry record is incomplete, the traveller must be rejected.
    2. If any location mentioned in the entry record is unknown, the traveller must be rejected.
    3. If the traveller's home country is Kanadia (country code: KAN), the traveller will be accepted.
    4. If the reason for entry is to visit and the visitor has a passport from a country from which a
    visitor visa is required, the traveller must have a valid visa. A valid visa is one that is less than
    two years old.
    5. If the traveller is coming from or travelling through a country with a medical advisory, she or he
    must be sent to quarantine.
    * It is possible for a traveller to receive more than one distinct immigration decisions. Conflicts should
    be resolved according the order of priority for the immigration decisions: quarantine, reject, and accept.
    """
    input_raw = open(input_file, "r").read()
    input_json = json.loads(input_raw)

    countries_raw = open(countries_file, "r").read()
    countries_json = json.loads(countries_raw)

    known_countries = [country for country in countries_json]  # Get list of 12 known countries
    known_countries.append("KAN")  # KAN is not in the list but as the home country should be
    known_countries = json.dumps(known_countries)

    visa_countries = []
    for country in countries_json:
        if countries_json[country]["visitor_visa_required"] == "1":
            visa_countries.append(country)

    quarantine_countries = []
    for country in countries_json:
        if len(countries_json[country]["medical_advisory"]) > 0:
            quarantine_countries.append(country)

    decision_list = []
    for traveller in input_json:
        # decisions_list.append(traveller["first_name"])  # for debugging
        traveller_decision = []

        # Rule 1: If required information for entry record incomplete, traveller is rejected
        completeness_checklist = []
        try:
            completeness_checklist.append(len(traveller["first_name"]))
            completeness_checklist.append(traveller["last_name"])
            if valid_date_format(traveller["birth_date"]) == False and len(traveller_decision) == 0:
                traveller_decision.append("Reject")
            if valid_passport_format(traveller["passport"]) == False and len(traveller_decision) == 0:
                traveller_decision.append("Reject")

            completeness_checklist.append(traveller["home"]["country"])
            completeness_checklist.append(traveller["from"]["country"])
            completeness_checklist.append(traveller["entry_reason"])
            if 0 in completeness_checklist and len(traveller_decision) == 0:
                traveller_decision.append("Reject")

        except KeyError:
            if len(traveller_decision) == 0:
                traveller_decision.append("Reject")

        # Rule 2: If any unknown location noted, traveller is rejected
        if traveller["home"]["country"] not in known_countries \
                or traveller["from"]["country"] not in known_countries \
                and len(traveller_decision) == 0:
            traveller_decision.append("Reject")

        # Rule 3: If home country is KAN, traveller is accepted
        if traveller["home"]["country"] == "KAN" and len(traveller_decision) == 0:
            traveller_decision.append("Accept")

        # Rule 4: If reason is visit and has passport from country where visa required,
        # traveller must have valid visa less than 2 years old
        if len(traveller_decision) == 0:
            if traveller["entry_reason"] == "visit" \
                    and traveller["from"]["country"] in visa_countries \
                    and not is_more_than_x_years_ago(2, traveller["visa"]["date"]):
                traveller_decision.append("Accept")
            else:
                traveller_decision.append("Reject")

        # Rule 5: If coming from or travelling through country with medical advisory, quarantine
        if traveller["from"]["country"] in quarantine_countries and len(traveller_decision) == 0:
            traveller_decision.append("Quarantine")

        decision_list += traveller_decision

    return decision_list

print decide("test_jsons/test_returning_citizen.json", "countries.json")
# print decide("valid_visa_example.json", "countries.json")

# print valid_visa_format("CFR6X-XSMVA")