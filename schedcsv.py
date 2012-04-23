#!/usr/bin/env python
import csv, sys, re, os
from operator import itemgetter, attrgetter
#from bs4 import BeautifulSoup  ## I had hoped to use BeautifulSoup to help clean up the output

### the purpose of this script is to parse a csv file from a sched.org event,
### output the relevent information into useful output files that can be use for a convention.

# is the file being listed in the command line?
if len(sys.argv)>1:
    filename = sys.argv[1]
    
else:
    # if not then use penguicon.csv as a default
    filename = "sched.csv"

# quick and simple template for the output for the schedule book
template ="""<event><title>%(name)s</title>
<topic>%(event_type)s</topic>
<room>%(venue)s</room>
<blurb><participant>%(speakers)s</participant> %(description)s <duration>%(duration)s</duration></blurb></event>\n"""

hourtemplate ="""<event><title>%(name)s</title>
<topic>%(event_type)s</topic>
<room>%(venue)s</room>
<blurb><participant>%(speakers)s</participant> %(description)s</blurb></event>\n"""

extrainfo= """
<startday>%(startday)s</startday>
<starttime>%(starttimeampm)s</starttime>
<endday>%(endday)s</endday>
<endtime>%(endtimeampm)s</<endtime>
<hours>%(hours)s</hours>
<minutes>%(minutes)s</minutes>
"""
# replace all function to help with the clean up
def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text

### from http://love-python.blogspot.com/2008/02/read-csv-file-in-python.html then edited 
#read in the csv file and 
class readInCSV:
     def __init__(self,fileName):
         self.fileName = fileName
         self.fileReader = csv.reader(open(self.fileName, "rb"), delimiter = ',')
         self.schedule = []
         for data in self.fileReader:
             self.schedule.append(data)
         self.headers = self.schedule[0]
         self.headerdict = {}
         for index, header in enumerate(self.headers):
              self.headerdict[header] = index

def calcduration(startday, starttime, endday, endtime, minutes):
    day = endday - startday
    hour = endtime - starttime
    hours = (24 * day) + hour
    if hours == 1:
        hourstext = "1 hour"
    else:
        hourstext = str(hours) + " hours"
    if hours > 0:
        if minutes != "00":
            duration = hourstext +" and " + minutes + " minutes"
        else:
            duration = hourstext
    else:
        duration = minutes + " minutes"
    totalminutes = (hours * 60) + int(minutes)
    return duration, hours, minutes, totalminutes

### taken from http://www.codigomanso.com/en/2011/05/trucomanso-transformar-el-tiempo-en-formato-24h-a-formato-12h-python/ then edited
def ampmformat (hhmmss):
  """
    This method converts time in 24h format to 12h format
    Example:   "00:32" is "12:32 AM"
               "13:33" is "1:33 PM"
  """
  ampm = hhmmss.split (":")
  if (len(ampm) == 0) or (len(ampm) > 3):
    return hhmmss

  # is AM? from [00:00, 12:00[
  hour = int(ampm[0]) % 24
  isam = (hour >= 0) and (hour < 12)

  # 00:32 should be 12:32 AM not 00:32
  if isam:
    ampm[0] = ('12' if (hour == 0) else "%02d" % (hour))
  else:
    ampm[0] = ('12' if (hour == 12) else "%02d" % (hour-12))
  ret = ':'.join (ampm)[:-3] + (' AM' if isam else ' PM')
  if ret[0] == "0":
      return ret[1:]
  else:
      return ret
###

## eventually it would be good to use another class and then send the data to a templating engine to render it
#class pconsessions:
#    def __init__(self, ):

pconsched = readInCSV(filename)

fields =  ["event_start", "event_end", "name", "event_type", "venue", "speakers", "description"]

sessions = [] # list of sessions...empty so far!
speakers = [] # list of speakers...empty as well. imagine that
speakerdict = {}
hourslist = {}

for index, x in enumerate(pconsched.schedule):
    # (re)initialize a session dictionary object
    session = {} 
    # for each field grab the data and put it in the session dictionary
    for field in fields:
        # bring the field info into a variable to help keep the code clean
        fieldtext = pconsched.schedule[index][pconsched.headerdict[field]]

        # separate the time and day into different variables
        if (field == "event_start"):
            session['startday'] = fieldtext[:len(fieldtext)-fieldtext.find(" ") +1]
            if fieldtext[-8:] != "nt_start":
                session['starttime']= fieldtext[len(fieldtext)-fieldtext.find(" ") +2:]
                session['starttimeampm'] = ampmformat(session['starttime']) 
            else:   
                session['starttime'] = "event_start"
                session['starttimeampm'] = "starttime am/pm"
        if (field == "event_end"):
            session['endday'] = fieldtext[:len(fieldtext)-fieldtext.find(" ") +1]
            if fieldtext[-8:] != "vent_end":
                session['endtime'] = fieldtext[-8:] 
                session['endtimeampm'] = ampmformat(session['endtime'])
            else: 
                session['endtime'] = "event_end"
                session['endtimeampm'] = "endtime am/pm"
        # remove the beginning portion of http and mail links
        if fieldtext.find("<a") > 0:
            substart = fieldtext.find("href")-3
            subend = fieldtext.find(">",substart)+1
            fieldtext = fieldtext.replace(fieldtext[substart: subend], "")

        # dictionary of the other text to be converted to clean up the sched.org output
        reps = {"&nbsp;":" ","<br />":"","&amp;":" and ", "<p>":"", "</p>":"","</a>":"", "&ldquo;":"\"", "&rdquo;":"\"", "&rsquo;":"\'", "&ndash;":"-","\n":" ", "  ":" ", "\r":" "}
        amps = {"&":" and ", "  ":" "}
        # do the replacements and put the values into the proper session field
        temptext = replace_all(fieldtext, reps)
        temptext = replace_all(temptext, amps)
#        temptext.replace(os.linesep, " ")
        session[field] = replace_all(temptext, amps)
        if field == "speakers":
            testtext = fieldtext.split(', ')
            #for x in testtext:
            #    print x

    if session['startday'] ==  "event_start":
        session['duration'] = "duration"
        session['hours'] = 0
        session['minutes'] = 0
        session['totalminutes'] = 0
    else:
        session['duration'], session['hours'], session['minutes'], session['totalminutes']  = calcduration(int(session['startday'][8:]),int(session['starttime'][:-6]) ,int(session['endday'][8:]) , int(session['endtime'][:-6]), session['endtime'][3:-3])
        
    session['speakerlist'] = session['speakers'].split(", ")
    for speaker in session['speakerlist']:
        if speaker not in speakers:
            speakers.append(speaker)
            speakerdict[speaker] = session['totalminutes']
        else:
            speakerdict[speaker] += session['totalminutes']
    # add the session to the list of sessions
    sessions.append(session)

## sort the list of sessions here by day then by time.
sessions.sort(key=itemgetter('startday','starttime'))
speakers.sort()
tempstart = "test"

## for each session in the list of sessions 
#"""
with open("2012.penguicon.schedule.xml",'w') as myoutput:
    for index, y in enumerate(sessions):
      if "2012-04-27 14:00:00" != y['event_start'] and "duration" != y['duration']:
        if tempstart == "test":
            myoutput.write( "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?><events xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"><document>\n")
        if not y['event_start'] == tempstart:
            if y['event_start'] == "2012-04-27 15:59:00" :
                myoutput.write("<time>All Weekend</time>\n")
            else:
                temptext =  "<time>"+ y['starttimeampm'] + "</time>\n"
                myoutput.write(temptext)
            tempstart = y['event_start']

        if "50 minutes" == y['duration']:
            myoutput.write(hourtemplate % y)
        else: 
            myoutput.write(template % y)

    myoutput.write('</document></events>\n')
myoutput.close()
#"""

with open("2012.penguicon.speakers.3plus.txt",'w') as discountedspeaker:
  with open("2012.penguicon.speakers.txt",'w') as fullspeaker:
    for key, value in sorted(speakerdict.iteritems(), key=lambda (k,v): (k,v)):
      if value >= 150:
          discountedspeaker.write("%s\n" % (key))
      fullspeaker.write("%s\n" % (key))#, value))
	  
fullspeaker.close()
discountedspeaker.close()
