 # -*- coding: utf-8 -*-
"""This module is to be used to read in a csv file into a dictionary

Example:
  This can currently be used from the command line or by importing the module
  into another python script

      $ python csv_reader.py

If this is imported it will use the default sched.csv file

.. _Google Python Style Guide:
   http://google-styleguide.googlecode.com/svn/trunk/pyguide.html
"""
import csv, sys

# is the file being listed in the command line?
if len(sys.argv) > 1:
    FILENAME = sys.argv[1]
else:
    # if not then use sched.csv as a  
    FILENAME = "sched.csv"
    """set the default file name to sched.scv
    """

class Readincsv:
    # it would be a good idea to clean the content as it comes in
    """
    read in the csv file and add it to a list of dictionaries
    """

    def __init__(self, filename):
        self.filename = filename
        self.schedule = []
        with open(self.filename) as csvfile:
            self.reader = csv.DictReader(csvfile)
            self.headers = self.reader.fieldnames
            for row in self.reader:
                self.laststring = \
                    [self.schedule.append({event_data:row[event_data]})\
                    for event_data in row]
                #print [{event_data:row[event_data]} for event_data in row]


SCHEDULEFILE = Readincsv(FILENAME)
print [eventData for eventData in SCHEDULEFILE.schedule]
print SCHEDULEFILE.laststring
