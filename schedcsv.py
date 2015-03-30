#!/usr/bin/env python
import csv, json, sys, re, os
from operator import itemgetter, attrgetter
from git import *
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
programbook_template ="""<event><title>%(bookname)s</title>
<topic>%(event_type)s</topic>
<room>%(venue)s</room>
<blurb><participant>%(speakers)s</participant> %(bookdescrip)s <duration>%(duration)s</duration></blurb></event>"""
"""took out \n"""
programbook_template_no_room ="""<event><title>%(bookname)s</title>
<topic>%(event_type)s</topic>
<blurb><participant>%(speakers)s</participant> %(bookdescrip)s <duration>%(duration)s</duration></blurb></event>"""
"""took out \n"""

hourtemplate ="""<event><title>%(bookname)s</title>
<topic>%(event_type)s</topic>
<room>%(venue)s</room>
<blurb><participant>%(speakers)s</participant> %(bookdescrip)s </blurb></event>"""
"""took out \n"""

extrainfo= """
<startday>%(startday)s</startday>
<starttime>%(starttimeampm)s</starttime>
<endday>%(endday)s</endday>
<endtime>%(endtimeampm)s</<endtime>
<hours>%(hours)s</hours>
<minutes>%(minutes)s</minutes>
"""
### configure these variables each year ###
hoteladdress = "1500 Town Center, Southfield, Michigan 48075 USA"
friday_header = "FRIDAY, APRIL 24"
friday_date = "4/24/2015"
saturday_header = "SATURDAY, APRIL 25"
saturday_date = "4/25/2015"
sunday_header = "SUNDAY, APRIL 26"
friday_date = "4/26/2015"

###
calendar_header= """Subject,Start Date,Start Time,End Date,End Time,All Day Event,Description,Location,Private\n"""
schedule_header= """Start Date,Start Time,End Date,End Time,Duration,Location,Track,Title,Presenters,Book Description,All Day Event,Private,AV Needs\n"""
schedule_csv_template= """%(startday)s,%(starttime)s,%(endday)s,%(endtime)s,%(duration)s,"%(venue)s",%(event_type)s,"%(name)s","%(speakers)s",'%(csvsafedescrip)s',%(allday)s,%(private)s,%(avneeds)s\n"""
calendar_template=""""%(name)s",%(startday)s,%(starttime)s,%(endday)s,%(endtime)s,%(allday)s,"%(caldescrip)s  Speakers include:%(calspeakers)s","%(venue)s",%(private)s\n"""
speaker_calendar_template=""""%(name)s",%(startday)s,%(starttime)s,%(endday)s,%(endtime)s,%(allday)s,"%(caldescrip)s  Speakers include:%(calspeakers)s - Track: %(event_type)s  - Duration: %(duration)s - Audio/video needs: %(avneeds)s ","%(venue)s",%(private)s\n"""
all_weekend_header = "ALL WEEKEND"

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
         self.schedule.pop(0)   # remove header line from data

def calcduration(startday, starttime, endday, endtime, minutes):
    #print "in calc duration start day ", startday
    #print "in calc duration start time", starttime
    #print "in cacl duration end day ", endday
    #print "in calc duration end time ", endtime
    #print "in calc duration end minutes", minutes
    day = endday - startday
    #print "day diff ", day
    hour = endtime - starttime
    #print "hour diff ", hour
    hours = (24 * day) + hour
    #print "hours + 24 * days", hours
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
        #print minutes
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

  # is AM? from [00:00, 12:00]
#  print "ampm " + ampm[0]
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

## 2012 fields
#fields =  ["event_start", "event_end", "name", "event_type", "venue", "speakers", "description"]

## 2013 fields
#fields =  ["Start Date", "Start Time", "End Date", "End Time", "Location", "Track","Title", "Presenters", "Book Description", "All Day Event","Private"]

## 2015 fields
fields =  ["Start Date", "Start Time", "End Date", "End Time", "Location", "Track","Title", "Presenters", "Book Description", "All Day Event","Private","AV Needs"]
## fields needed for google calendar
calfields = ["Subject", "Start Date", "Start Time", "End Date", "End Time", "All Day Event", "Description", "Location", "Private"]

sessions = [] # list of sessions...empty so far!
speakers = [] # list of speakers...empty as well. imagine that
speakernosplist = []
#speaker_events_dict[speakernosp] = []
tracks = []   # list of tracks
tracksdict = {}   # for use in creating a dictionary of tracks with no space in their name 
rooms = []
roomsdict = {}
speakerdict = {}
hourslist = {}
speaker_events_dict = {}
# go through the schedule row by row
for index, x in enumerate(pconsched.schedule):
    # (re)initialize a session dictionary object
    session = {} 
    # for each field grab the data and put it in the session dictionary
    for field in fields:
        # bring the field info into a variable to help keep the code clean
        fieldtext = pconsched.schedule[index][pconsched.headerdict[field]]

        # separate the time and day into different variables
        
        session['input'] = x
        session['index'] = index
        ##start day and time assignments
        if  (field == "Start Date"):
            session['startday'] = fieldtext
            if (fieldtext == friday_date):
                session['dayheader'] = friday_header
            if (fieldtext == saturday_date):
                session['dayheader'] = sunday_header
            if (fieldtext == sunday_date):
                session['dayheader'] = sunday_header
                
            #print fieldtext

        if  (field == "Start Time"):
            if fieldtext != "Start Time":
                session['starttime'] = fieldtext
                session['event_start'] = fieldtext
                #print fieldtext
                #session['starttime']= fieldtext[len(fieldtext)-fieldtext.find(" ") +2:]   
                session['starttimeampm'] = ampmformat(session['starttime']) 
            else:   
                session['starttime'] = "event_start"
                session['event_start'] = "event_start"
                session['starttimeampm'] = "starttime am/pm"
            
                

        if  (field == "End Date"):
            session['endday'] = fieldtext

        if  (field == "End Time"):
            if fieldtext != "End Time":
                session['endtime'] = fieldtext
                #print "setting endtime " + fieldtext
                session['event_end'] = fieldtext            
                #session['starttime']= fieldtext[len(fieldtext)-fieldtext.find(" ") +2:]
                session['endtimeampm'] = ampmformat(session['endtime']) 
            else:   
                session['endtime'] = "event_end"
                session['event_end'] = "event_end"
                session['endtimeampm'] = "endtime am/pm"

        if  (field == "Book Description"): 
                    session['description'] = fieldtext
        if  (field == "Location"):
            session['venue'] = fieldtext
            temproom = re.sub(r'\s','', fieldtext)
            temproom = re.sub(r'\(','', temproom)
            temproom = re.sub(r'\)','', temproom)
            temproom = re.sub(r'/','', temproom)
            session['roomnosp'] = temproom
            if fieldtext not in rooms:
              rooms.append(fieldtext)
              roomsdict[fieldtext] = temproom
        if  (field == "Presenters"):
            session['speakers'] = fieldtext
        if  (field == "Title"):
            session['name'] = fieldtext
            temptext = replace_all(fieldtext, addamps)         
            session['bookname'] = temptext

        if  (field == "Track"):
            session['event_type'] = fieldtext
            session['event_type_list'] = fieldtext.split(", ")
            session['tracknosp'] = []
            for eventtype in session['event_type_list']:
                temptrack = re.sub(r'\s','', eventtype)
                temptrack = re.sub(r'\(','', temptrack)
                temptrack = re.sub(r'\)','', temptrack)
                temptrack = re.sub(r'/','', temptrack)
                #print temptrack
                session['tracknosp'].append(temptrack)
                if eventtype not in tracks:
                  tracks.append(eventtype)
                  tracksdict[eventtype] = temptrack
        if  (field == "All Day Event"):
            if  (fieldtext == ""):
              session['allday'] = "FALSE"
            else:
              session['allday'] = fieldtext 
        if  (field == "Private"):
            if  (fieldtext == ""):
              session['private'] = "DEFAULT"
            else:
              session['private'] = fieldtext
        if (field == "AV Needs"):
            if  (fieldtext == ""):
              session['avneeds'] = "none"
            else:
              session['avneeds'] = fieldtext
        ## remove the beginning portion of http and mail links 
        if fieldtext.find("<a") > 0:
            substart = fieldtext.find("href")-3
            subend = fieldtext.find(">",substart)+1
            fieldtext = fieldtext.replace(fieldtext[substart: subend], "")

        ## this is clean up below was required because the sched output 
        ## included some html symbols and tags which would not have looked
        ## good in the program book
        # dictionary of the other text to be converted to clean up the sched.org output
        reps = {"&nbsp;":" ","<br />":"","&":" and ","&amp;":" and ", "<p>":"", "</p>":"","</a>":"", "&ldquo;":"\"", "&rdquo;":"\"", "&rsquo;":"\'", "&ndash;":"-","\n":" ", "  ":" ", "\r":" "}
        amps = {"&":" and ", "  ":" "}
        quoterep = {"\"":"'"}
        addamps = {"&":"&amp;", "\n":" "}
        commarep = {",":"-","\n":" "}
        # do the replacements and put the values into the proper session field
        temptext = replace_all(fieldtext, reps)
        temptext = replace_all(temptext, amps)
#        temptext.replace(os.linesep, " ")
        session[field] = replace_all(temptext, amps)
        if field == "Book Description":
            temptext = replace_all(fieldtext, quoterep)         
            session['caldescrip'] = temptext
            temptext = replace_all(temptext, commarep)
            session['csvsafedescrip'] = temptext
            temptext = replace_all(fieldtext, addamps)         
            session['bookdescrip'] = temptext
        if field == "Presenters":
            temptext = replace_all(fieldtext, quoterep)         
            session['calspeakers'] = temptext
#        if field == "speakers":
        if field == "Presenters":
            testtext = fieldtext.split(', ')
            #for x in testtext:
            #    print x
# this first one is a for the first entry which is intentionally dummy data
    if (session['starttime'] ==  "event_start") or (session['startday'] ==  "Start Day"):
        session['duration'] = "duration"
        #print "duration"
        session['hours'] = 0
        session['minutes'] = 0
        session['totalminutes'] = 0
        session['avneeds'] = "none"
    else:
        ##print session['name']
        #print "start day " + session['startday'][2:-5] 
        #print "start time " + session['starttime'][:-3]
        #print "end day " + session['endday'][2:-5]
        ##print "end time " + session['endtime'][-5:-3]
        #print "end minutes " + session['endtime'][3:]
        #print "event_start " + session['event_start']
        #print "event_end " + session['event_end']

        session['duration'], session['hours'], session['minutes'], session['totalminutes']  = calcduration(int(session['startday'][2:-5]), int(session['starttime'][:-3]) , int(session['endday'][2:-5]) , int(session['endtime'][-5:-3]), session['endtime'][-2:])
   
    
    session['speakerlist'] = session['speakers'].split(", ")
    session['speakernosp'] = ""
    for speaker in session['speakerlist']:
            tempspeaker = re.sub(r'\s','', speaker)
            tempspeaker = re.sub(r'\(','', tempspeaker)
            tempspeaker = re.sub(r'\)','', tempspeaker)
            tempspeaker = re.sub(r'/','', tempspeaker)
            tempspeaker = re.sub(r'"','-', tempspeaker)
            if session['speakernosp'] == "":
                session['speakernosp'] = session['speakernosp'] + tempspeaker
            else:
                session['speakernosp'] = session['speakernosp'] + "," + tempspeaker
    session['speakernosplist'] = session['speakernosp'].split(",")
    for speaker in session['speakerlist']:
      if speaker != "":
        if speaker not in speakers:
            speakers.append(speaker)
            speakerdict[speaker] = session['totalminutes']
            #speaker_events_dict[speaker].append(session['name'])
            #print speaker, session['name']
            
        else:
            speakerdict[speaker] += session['totalminutes']
            #speaker_events_dict[speaker].append(session['name'])
            #print speaker, session['name']
    for speakernosp in session['speakernosplist']:
      if (speakernosp != ""):
        if speakernosp not in speakernosplist:
            #speakers.append(speaker)
            #speakerdict[speaker] = session['totalminutes']
            speaker_events_dict[speakernosp] = []
            speaker_events_dict[speakernosp].append(session['name'])
            #print speaker, session['name']
            
        else:
            #speakerdict[speaker] += session['totalminutes']
            speaker_events_dict[speakernosp].append(session['name'])
            #print speaker, session['name']
            
    # add the session to the list of sessions
    sessions.append(session)

## sort the list of sessions here by day then by time.
# if the spreadsheet is in order use the index for sorting
# otherwise implement an index for the sessions in another ways
sessions.sort(key=itemgetter('index'))

# old n busted sort 
##sessions.sort(key=itemgetter('venue'))
#sessions.sort(key=itemgetter('startday','starttime','venue'))
##sessions.sort(key=itemgetter('starttime'))
##sessions.sort(key=itemgetter('startday'))
##sessions.sort(key=itemgetter('allday'), reverse=True)
sessions = sorted(sessions, key=lambda thing: ('0' if thing['allday'] else '1')  + thing['startday'] + thing['starttimeampm'] + thing['venue'] + thing['name']) ## thanks Walter!

#sessions.sort(key=itemgetter('allday'), reverse=True)

speakers.sort()
tempstart = "test"


rp = "./output/"
caldir = rp +"calendars/"
schedulebyroomdir = rp + "schedbyroom/"
speakerdir = rp +"schedbyspeaker/"
if not os.path.exists(rp):
    os.makedirs(rp)
if not os.path.exists(caldir):
    os.makedirs(caldir)  
if not os.path.exists(schedulebyroomdir):
    os.makedirs(schedulebyroomdir)
if not os.path.exists(speakerdir):
    os.makedirs(speakerdir)  
## dump to a json file
with open(rp + "2015.penguicon.schedule.alldata.json",'w') as myoutput:
    json.dump(sessions, myoutput, indent=4, separators=(',', ': '))
with open(rp + "2015.penguicon.schedule.json",'w') as myoutput:
    fields = {"location":"Location", "book_description":"Book Description", \
              "title":"Title", "track":"Track", "minutes":"totalminutes", \
              "start_date":"Start Date", "end_date":"End Date", \
              "start_time":"starttime", "end_time":"endtime",
              "presenters":"speakerlist"
    }
    json_output = [
        {k: y.get(ok,'') for k,ok in fields.items()}
        for y in sessions
    ]
    json.dump(json_output, myoutput, indent=4, separators=(',', ': '))
## for each session in the list of sessions 
#"""
with open(rp + "2015.penguicon.schedule.alltimes.xml",'w') as myoutput:
    for index, y in enumerate(sessions):
#      print y
      if "2015-04-24 14:00:00" != y['event_start'] and "duration" != y['duration']:
        if tempstart == "test":
            myoutput.write( "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?><events xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">")
        #print y
        if not y['All Day Event'] == tempstart:
            if y['All Day Event'] == "TRUE" :
                myoutput.write("<day>All Weekend</day>\n")
            else:
                temptext =  "\n<day>"+ y['dayheader'] + "</day>\n<time>"+ y['starttimeampm'] + "</time>\n"
                myoutput.write(temptext)
            tempstart = y['event_start']

        if "50 minutes" == y['duration']:
            myoutput.write(hourtemplate % y)
        elif ""  == y['venue']:
            myoutput.write(programbook_template_no_room % y)
        else: 
            myoutput.write(programbook_template % y)

    myoutput.write('</events>\n')
myoutput.close()
#"""

# schedule by room and by speaker output

with open( rp + "2015.penguicon.fullschedule.csv",'w') as fullschedule:
    fullschedule.write(schedule_header) # schedule_header needs to be written
    for room in roomsdict:
        with open(schedulebyroomdir + roomsdict[room] + ".csv",'w') as temproomsched:
            temproomsched.write(schedule_header)
            temproomsched.close()
    for index, y in enumerate(sessions):
      for speakernosp in y['speakernosplist']:
        with open(speakerdir  + speakernosp + ".csv",'w') as tempspeakersched:        
        #with open(speakerdir + speakernosplist[speakernosp] + ".cvs", 'w') as tempspeakersched:
            tempspeakersched.write(calendar_header)
            tempspeakersched.close()
    for index, y in enumerate(sessions):
        #if not y['All Day Event'] == 'All Day Event':
            fullschedule.write(schedule_csv_template % y)
            with open(schedulebyroomdir + y['roomnosp'] + ".csv",'a') as temproomsched:
                temproomsched.write(schedule_csv_template % y)
            temproomsched.close()
            for speaker in y['speakernosplist']:
                with open(speakerdir  + speaker + ".csv",'a') as tempspeakersched:
                    tempspeakersched.write(speaker_calendar_template % y)
                tempspeakersched.close()

fullschedule.close()

with open(rp + "2015.penguicon.speakers.3plus.txt",'w') as discountedspeaker:
  with open(rp + "2015.penguicon.speakers.txt",'w') as fullspeaker:
    for key, value in sorted(speakerdict.iteritems(), key=lambda (k,v): (k,v)):
      if value >= 150:
          discountedspeaker.write("%s\n" % (key))
      fullspeaker.write("%s, %s\n" % (key,value))

fullspeaker.close()
discountedspeaker.close()
fullspkrlist = []
with open(rp + "2015.penguicon.spkrs.bylast.3plus.txt",'w') as dscountedspkr:
  with open(rp + "2015.penguicon.spkrs.bylast.txt",'w') as fullspkr:
    for key, value in sorted(speakerdict.iteritems(), key=lambda (k,v): (k,v)):
      if value >= 150:
          dscountedspkr.write("%s\n" % (key))
      fullspkrlist.append( str(value)+ " "+ key)
      #fullspkr.write("%s\n" % (key, value))
    for x in sorted(fullspkrlist):
      fullspkr.write("%s\n" % (x) )

fullspkr.close()
dscountedspkr.close()

# one calendar per track/type of programming
#  also output the full calendar
with open( caldir + "2015.penguicon.fullcalendar.csv",'w') as fullcalendar:
  #with open(caldir + "2015.penguicon.speakers.txt",'w') as fullspeaker:
    fullcalendar.write(calendar_header)
    for track in tracks:
        with open(caldir + tracksdict[track] + ".csv",'w') as tempcal:
            tempcal.write(calendar_header)
            tempcal.close()
    for index, y in enumerate(sessions):
        if not y['All Day Event'] == 'All Day Event':
            fullcalendar.write(calendar_template % y)
            #print y['tracknosp']
            for caltrack in y['tracknosp']:
              with open(caldir + caltrack + ".csv",'a') as tempcal:
                tempcal.write(calendar_template % y)
              tempcal.close()

fullcalendar.close()
#fullcalendar.close()

#with open(rp + "sessiondata.csv",'w') as sessiondata:
writer = csv.writer(open(rp + 'dict.csv', 'wb'))
for index, y in enumerate(sessions):
    for key, value in y.items():
        writer.writerow([key, value])

# write out the speakers and their events ...this doesn't work yet
#speaker_events_dict
#writer = csv.writer(open(rp + 'speaker_events_dict.csv', 'wb'))
#for x,y in enumerate(speaker_events_dict):
#for key, value in speaker_events_dict.items():
#    writer.writerow([key, ', '.join(value)] )
#    print key, "is in",len(value)," event(s) which is/are", ', '.join(value)


# Fix the multiple entries of the current time issue  (thanks Matt)
inputfile = open(rp + '2015.penguicon.schedule.alltimes.xml', 'r')
outputfile = open('penguicon.schedule.xml', 'w')

# current time is set to the initial start time of 4 pm for the 2015 year... this could change year to year
currenttime = '<time>4 PM</time>'

# this line is used for 'all weekend events' 
# which are typically listed in the beginning
# before any other events in the program book
# then the variable is reused in the loop
lasttime = '<day>All Weekend</day>'

for row in inputfile:
    if '<time>' in row:
        currenttime = row
        if currenttime != lasttime:
            outputfile.write(row)
            lasttime = row
    else: # If this is not a time row
        outputfile.write(row)

inputfile.close()
outputfile.close()



print "probable success processing csv and exporting to various formats"
