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
import sys
import  unicodecsv as csv
import pprint

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
    """Map csv columns to db columns"""
    csv_db_map = {"end_date":"End Date",
        "all_day_event":"All Day Event",
        "title":"Title",
        "track":"Track",
        "private":"Private",
        "start_time":"Start Time",
        "book_description":"Book Description",
        "presenters":"Presenters",
        "end_time":"End Time",
        "location":"Location",
        "duration":"Duration",
        "start_date":"Start Date",
        "av_needs":"AV Needs",}
    db_csv_map = {"End Date":"end_date",
        "All Day Event":"all_day_event",
        "Title":"title",
        "Track":"track",
        "Private":"private",
        "Start Time":"start_time",
        "Book Description":"book_description",
        "Presenters":"presenters",
        "End Time":"end_time",
        "Location":"location",
        "Duration":"duration",
        "Start Date":"start_date",
        "AV Needs":"av_needs",}

    def __init__(self, filename="sched.csv"):
        self.filename = filename
        self.schedule = []
        self.dbsched = []

        with open(self.filename) as csvfile:
            self.reader = csv.DictReader(csvfile)
            self.headers = self.reader.fieldnames 
            for row in self.reader:
                addthis = {}
                laststring = \
                    [self.schedule.append({event_data:row[event_data]})\
                    for event_data in row]
                [addthis.update({self.db_csv_map.get(event_data):row[event_data]})\
                        for event_data in row]
                self.dbsched.append(addthis)
                #print [{event_data:row[event_data]} for event_data in row]

"""
For locations, load a dictionary of locations from the db as events are read in,
find largest index and use that + 1 when adding a new entry
if a location in the csv isn't in the dictionary add it to the list of locations(as a dictionary) to be added to the db

do the same thing for speakers and tracks

"""
if __name__ == '__main__':
    # is the file being listed in the command line?
    if len(sys.argv) > 1:
        FILENAME = sys.argv[1]
    else:
        # if not then use sched.csv as a  
        FILENAME = "sched.csv"
        """set the default file name to sched.scv
        """

    #pp = pprint.PrettyPrinter(indent=4)
    SCHEDULEFILE = Readincsv(FILENAME)
    #print [eventData + "\n" for eventData in SCHEDULEFILE.schedule]
    #pp.pprint(SCHEDULEFILE.dbsched)
    #print SCHEDULEFILE.laststring


