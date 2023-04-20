'''
This script calculates the difference between two dates.
If only one date is given, it defaults to the difference between the given date and today.

The date format can be either dd/mm/yyyy or dd-mm-yyyy. The year can be either 4 digits or 2 digits.
Examples:
    dayssince.py 1/1/2020 to 1/1/2021
    dayssince.py 1-1-2020
    dayssince.py 1-1-20 to 1-1-21
'''

from datetime import datetime
from collections import namedtuple
import sys
import re

def main():
    try:
        INPUT = sys.argv[1]
        date_1, date_2 = parse_date(INPUT)
    except:
        raise Exception("Date missing or incorrect. Try passing a valid date as argument (e.g. dd/mm/yyy).\nExample: dayssince.py 13/09/2012 to 12/12/2012")
    daysbetween = dayssince(date_1.datetime, date_2.datetime)
    daystr = "dia" if daysbetween == 1 else "dias"
    connective = "desde" if daysbetween > 0 else "até"

    print(f"{abs(daysbetween)} {daystr} entre {date_1.str} e {date_2.str}.")

def formatdate(PATTERN, date):
    datestr = re.match(PATTERN, date)
    day = int(datestr.group(1))
    month = int(datestr.group(2))
    year = int(datestr.group(3)) if len(
        datestr.group(3)) > 2 else 2000 + int(datestr.group(3))
    return datetime(year, month, day), f"{day}/{month}/{year}"

def dayssince(date1, date2):
    d = max(date1, date2) - min(date1, date2)
    return d.days

def parse_date(datestr):
    # PATTERN = r"(\d{1,2})[-\/](\d{1,2})[-\/](\d{2,4})"
    PATTERN = r"(0?[1-9]|[12][0-9]|3[01])[-\/](0?[1-9]|1[012])[-\/](\d{2,4})"


    Date = namedtuple("Date", ["datetime", "str"])
    if "to" in datestr:
        date_1 = Date(*formatdate(PATTERN, datestr.split(" to ")[0]))
        date_2 = Date(*formatdate(PATTERN, datestr.split(" to ")[1]))
    else:
        date_1 = Date(*formatdate(PATTERN, datestr))
        today = datetime.today()
        date_2 = Date(*formatdate(PATTERN, f"{today.day}-{today.month}-{today.year}"))
    return date_1, date_2

if __name__ == '__main__':
    main()