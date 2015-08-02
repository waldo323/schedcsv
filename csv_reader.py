 # -*- coding: utf-8 -*-
"""This module is to be used to read in a csv file into a dictionary
This dictionary is then inserted into a database table as is.

Example:
  This can currently be used from the command line or by importing the module
  into another python script

      $ python csv_reader.py

If this is imported it will use the default sched.csv file

.. _Google Python Style Guide:
   http://google-styleguide.googlecode.com/svn/trunk/pyguide.html
"""
import csv, sys
import pprint
# is the file being listed in the command line?
if len(sys.argv) > 1:
    FILENAME = sys.argv[1]
else:
    # if not then use sched.csv as a  
    FILENAME = "sched.csv"
    """set the default file name to sched.scv
    """
# replace all function to help with the clean up
def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text


class Readincsv:
    # it would be a good idea to clean the content as it comes in
    """
    read in the csv file and add it to a list of dictionaries
    """
    replace_characters = {"\n": " " }
    laststring = []

    def __init__(self, filename):
        self.filename = filename
        self.schedule = []

        with open(self.filename) as csvfile:
            self.reader = csv.DictReader(csvfile)
            self.headers = self.reader.fieldnames 
            for row in self.reader:
                laststring = \
                    [self.schedule.append({event_data:row[event_data]})\
                    for event_data in row]
                #print [{event_data:row[event_data]} for event_data in row]

pp = pprint.PrettyPrinter(indent=4)
SCHEDULEFILE = Readincsv(FILENAME)
#print [eventData + "\n" for eventData in SCHEDULEFILE.schedule]
pp.pprint(SCHEDULEFILE.schedule)
print SCHEDULEFILE.laststring

"""
For locations, load a dictionary of locations from the db as events are read in,
find largest index and use that + 1 when adding a new entry
if a location in the csv isn't in the dictionary add it to the list of locations(as a dictionary) to be added to the db

do the same thing for speakers and tracks

"""

