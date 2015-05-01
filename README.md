schedcsv
========

seemingly simple project with the goal of parsing a csv file from an export
from the head of programming and generating output files which are particularly useful to the upcoming Penguicon (on the master branch). typically the previous years will be made into a branch named the same as the Penguicon main event was held

usage:
   * download the repository
   * update variables which are different in the current year if needed in schedcsv.py, getsched.sh
   * until sorting is done in the script, make sure that the spreadsheet is sorted the way you would like
     * with this suggested sort order the schedule be sorted into whether it is an all day event, then for each day the times will be in order with the rooms in alphabetical order 
       * name(Title) (A->Z)
       * room(Location) (A->Z)
       * start time (A->Z)
       * startday (A->Z)
       * all day (Z->A, since True means all day event)
   * make sure the spreadsheet link is correct in getsched.sh
   * run getsched.sh to get the spreadsheet and process it
   * if you have access to the git repo you can run getrunpush.sh, otherwise you'll want to comment out the git push

current output:
   * custom xml for program book (currentyear.penguicon.final.schedule.xml, penguicon.schedule.xml)
   * list of speakers (./output/2015.penguicon.speakers.txt)
   * list of speakers giving 3+ "hours" of talks ( an hour in this case is defined as 50 minutes...I think) (./output/2015.penguicon.speakers.3plus.txt)
   * full schedule output into a csv which google calendar is be able to import (difficult to use as so many events are at the same time) (./output/calendars/currentyear.penguicon.fullcalendar.csv)
   * schedule by track  in a (google or other ical) calendar importable csv format  (./output/calendars/)
   * schedule by speaker in a (google or other ical) calendar importable csv format (./output/schedbyspeaker/)
   * zip of all speakers calender importable csv files (./output/schedsbyspeaker.zip)
   * schedules by room for dubugging (./output/schedbyroom/)
   * schedules by room for use in making signs for each room (./penguicon.schedules.per.room.xml)
 
Running wish list:
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
  * output of a file with each event with special characters which should be cleaned up in the source document and note or hi-light which characters
    * this is helpful even when the program cleans the entries 
       since some of those characters make it harder to fix the source spreadsheet
  * trifold grid csv 
    * need to add addressing or a map of somesort so that I can pull each item into the csv without a computationally expensive loop setup....there are already way too many loops in this script
    * probably something where the script could call room.time and it would get the title of the entries in that slot
    * ....maybe not for this year since there is a spreadsheet with schedule in a very similar format...so exporting that as csv might work better for now
