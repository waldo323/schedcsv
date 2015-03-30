schedcsv
========

simple project with the goal of parsing a csv file from an export
from the head of programming and generating output files which are particularly useful to Penguicon 2015 (on the master branch).

usage:
   * download the repository
   * update variables which are different in the current year if needed in schedcsv.py, getsched.sh
   * until sorting is done in the script, make sure that the spreadsheet is sorted the way you would like
     * with this suggested sort order the schedule be sorted into whether it is an all day event, then for each day the times will be in order with the rooms in alphabetical order 
       * name
       * room
       * start time
       * startday
       * all day
   * make sure the spreadsheet link is correct in getsched.sh
   * run getsched.sh to get the spreadsheet and process it
   * if you have access to the git repo you can run getrunpush.sh, otherwise you'll want to comment out the git push

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
   * add output for calendar by room in calendar importable csv
   * work with tuxtrax https://github.com/MattArnold/tuxtrax 
   * split code into separately functioning bits
     *  bring in the schedule (or use the parts needed from the db)
     *  process the schedule into usable pieces for later use (event start time, end times, location, speakers etc)
       *  not needed if working with tuxtrax
     *  clean the text so that it will be useable in various formats (specaial characters changed to uable formats in the cases of the InDesign importable xml file, no new lines for xml and csv outputs etc)
       *  work with tuxtrax to make sure the field clean before getting them so the data can be entered directly into templates
     *  create output files in all the various or optionally just particular formats
     *  upload to github or other public place for collaboration with staff and the public
   * add template files for each type of output

