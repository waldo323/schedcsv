schedcsv
========

simple project with the goal of parsing a csv file from an export
from the head of programming and generating output files which are particularly useful to Penguicon 2015 (on the master branch).


current output:
   * custom xml for program book
   * list of speakers
   * list of speakers giving 3+ "hours" of talks ( an hour in this case is defined as 50 minutes...I think)
   * full schedule output into a csv which google calendar is be able to import (difficult to use as so many events are at the same time)
   * schedule by track  in a (google or other ical) calendar importable csv format
   * schedule by speaker in a (google or other ical) calendar importable csv format
   * zip of all speakers calender importable csv files
   * schedule by room for dubugging 



   
Running wish list:
   * split code into separately functioning bits
     *  bring in the schedule
     *  process the schedule into usable pieces for later use (event start time, end times, location, speakers etc)
     *  clean the text so that it will be useable in various formats (specaial characters changed to uable formats in the cases of the InDesign importable xml file, no new lines for xml and csv outputs etc)
     *  create output files in all the various or optionally just particular formats
     *  upload to gitub or other public place for collaboration with staff and the public
   * add template files for each type of output
   * work with tuxtrax https://github.com/MattArnold/tuxtrax 
