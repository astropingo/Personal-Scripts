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

try:
    INPUT = sys.argv[1]
except:
    raise Exception("Date missing. Try passing a valid date as argument.\nExample: dayssince.py 1/1/2020 to 1/1/2021")

PATTERN = r"(\d{1,2})[-\/](\d{1,2})[-\/](\d{2,4})"
Date = namedtuple("Date", ["datetime", "str"])

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

#namedtuple was having a hard time parsing the results from formatdate...
#I found that the reason was because the list was a single argument,
#so I had to add * to unpack it into separate arguments
if "to" in INPUT:
    date1 = Date(*formatdate(PATTERN, INPUT.split(" to ")[0]))
    date2 = Date(*formatdate(PATTERN, INPUT.split(" to ")[1]))
else:
    date1 = Date(*formatdate(PATTERN, INPUT))
    today = datetime.today()
    date2 = Date(*formatdate(PATTERN, f"{today.day}-{today.month}-{today.year}"))

daysbetween = dayssince(date1.datetime, date2.datetime)
daystr = "dia" if daysbetween == 1 else "dias"
connective = "desde" if daysbetween > 0 else "até"

output = f"{abs(daysbetween)} {daystr} entre {date1.str} e {date2.str}"
print(output)
