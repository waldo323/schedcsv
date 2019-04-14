#!/usr/bin/env python
import os
import csv
import jinja2
import json
import sys
import re
import logging
from operator import itemgetter
import AsciiDammit

#logging.basicConfig(level=logging.WARN)
logging.basicConfig(level=logging.DEBUG)
env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
web_template = env.get_template('programmingtemplate.html')
penguicon_tv = env.get_template('penguicon_tv')
testbook_template = env.get_template('testprogrambook.xml')
presentersgithubtoc = env.get_template('speakerstoc')
presenterpacket_template = env.get_template('presenter_packet_agenda')
tocspeakers = set()
tocsrooms = set()
speakersagendas = dict()

# the purpose of this script is to parse a csv file of events,
# output the relevant information into useful output files that can be use for
# a convention.

# is the file being listed in the command line?
if len(sys.argv) > 1:
    filename = sys.argv[1]

else:
    # if not then use penguicon.csv as a default
    filename = "sched.csv"

# quick and simple template for the output for the schedule book
programbook_template = """<event><title>%(bookname)s</title>
<topic>%(event_type)s</topic>
<room>%(venue)s</room>
<blurb><participant>%(speakers)s</participant> %(bookdescrip)s <duration>%(duration)s</duration></blurb></event>"""
"""took out \n"""
programbook_template_no_room = """<event><title>%(bookname)s</title>
<topic>%(event_type)s</topic>
<blurb><participant>%(speakers)s</participant> %(bookdescrip)s <duration>%(duration)s</duration></blurb></event>"""
"""took out \n"""

hourtemplate = """<event><title>%(bookname)s</title>
<topic>%(event_type)s</topic>
<room>%(venue)s</room>
<blurb><participant>%(speakers)s</participant> %(bookdescrip)s </blurb></event>"""
"""took out \n"""

schedule_by_room = """<event>
<room>%(venue)s</room>
<day>%(dayheader)s</day>
<title>%(bookname)s</title>
<topic>%(event_type)s</topic>
<time>%(starttimeampm)s</time></event>"""

schedule_by_room_hour_template = """<event>
<room>%(venue)s</room>
<day>%(dayheader)s</day>
<title>%(bookname)s</title>
<topic>%(event_type)s</topic>
<time>%(starttimeampm)s</time></event>"""

schedule_by_room_allweekend_template = """<event>
<room>%(venue)s</room>
<title>%(bookname)s</title>
<topic>%(event_type)s</topic>
<time>%(starttimeampm)s</time></event>"""

# configure these variables each year
hoteladdress = "1500 Town Center, Southfield, Michigan 48075 USA"
noday_header = "NoDay, MAY 3"
friday_header = "FRIDAY, MAY 3"
friday_date = "5/3/2019"
saturday_header = "SATURDAY, MAY 4"
saturday_date = "5/4/2019"
sunday_header = "SUNDAY, MAY 5"
sunday_date = "5/5/2019" 
conyear = "2019"
constart = "2019-05-03 12:00:00"



calendar_header = """Subject,Start Date,Start Time,End Date,End Time,All Day Event,Description,Location,Private\n"""
schedule_header = """Start Date,Start Time,End Date,End Time,Duration,Location,Track,Title,Presenters,Book Description,All Day Event,Private,AV Needs\n"""
schedule_csv_template = """%(startday)s,%(starttime)s,%(endday)s,%(endtime)s,%(duration)s,"%(venue)s","%(event_type)s","%(name)s","%(speakers)s","%(csvsafedescrip)s",%(allday)s,%(private)s,"%(avneeds)s"\n"""
calendar_template = """"%(name)s",%(startday)s,%(starttime)s,%(endday)s,%(endtime)s,%(allday)s,"%(caldescrip)s  Speakers include:%(calspeakers)s","%(venue)s",%(private)s\n"""
speaker_calendar_template = """"%(name)s",%(startday)s,%(starttime)s,%(endday)s,%(endtime)s,%(allday)s,"%(caldescrip)s  Speakers include:%(calspeakers)s - Track: %(event_type)s  - Duration: %(duration)s ","%(venue)s",%(private)s\n"""
all_weekend_header = "ALL WEEKEND"

daylist = [all_weekend_header, friday_header, saturday_header, sunday_header]
starttimeampmset = set()
# replace all function to help with the clean up
def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text

# from http://love-python.blogspot.com/2008/02/read-csv-file-in-python.html then edited 
# read in the csv file and
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
    logging.debug("in calc duration start day: %s ", startday)
    logging.debug("in calc duration start time %s", starttime)
    logging.debug("in cacl duration end day %s", endday)
    logging.debug("in calc duration end time %s", endtime)
    logging.debug("in calc duration end minutes %s", minutes)
    day = endday - startday
    logging.debug("day diff %s", day)
    hour = endtime - starttime
    logging.debug("hour diff %s", hour)
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
  if ampm == ['']:
    print ampm
    ampm = ['16','00']
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
# 2019 fields
fields =  [
    "event_start",
    "event_end",
    "name",
    "event_type",
    "venue",
    "speakers",
    "description"]

# 2015 fields
oldfields =  [
    "Start Date",
    "Start Time",
    "End Date",
    "End Time",
    "Location",
    "Track",
    "Title",
    "Presenters",
    "Book Description",
    "All Day Event",
    "Private",
    "AV Needs"]
# fields needed for google calendar
calfields = [
    "Subject",
    "Start Date",
    "Start Time",
    "End Date",
    "End Time",
    "All Day Event",
    "Description",
    "Location",
    "Private"]

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
        fieldtext = AsciiDammit.asciiDammit(pconsched.schedule[index][pconsched.headerdict[field]])

        # separate the time and day into different variables
        
        session['input'] = x
        session['index'] = index
        session['All Day Event'] = ''
        session['private'] = "PUBLIC"
        session['avneeds'] = ""
        session['alldayorder'] = "3"
        ##start day and time assignments
# separate the time and day into different variables
        if (field == "event_start"):
            logging.debug(fieldtext[:len(fieldtext)-fieldtext.find(" ") +1])
            dashdate = fieldtext[:len(fieldtext)-fieldtext.find(" ") +1]
            slashdate = "{}/{}/{}".format(dashdate[6:7], dashdate[9:10], dashdate[0:4]) 
            session['startday'] = slashdate
            session["Start Date"] = session['startday']
            if fieldtext[-8:] != "nt_start":
                logging.debug(fieldtext[len(fieldtext)-fieldtext.find(" ") +2:-3])
                session['starttime'] = fieldtext[len(fieldtext)-fieldtext.find(" ") +2:-3]
                session["Start Time"] = session['starttime']
                session['starttimeampm'] = ampmformat(session['starttime']) 
            else:   
                session['starttime'] = "event_start"
                session['starttimeampm'] = "starttime am/pm"
        if (field == "event_end"):
            logging.debug(fieldtext[:len(fieldtext)-fieldtext.find(" ") +1])
            dashdate = fieldtext[:len(fieldtext)-fieldtext.find(" ") +1]
            slashdate = "{}/{}/{}".format(dashdate[6:7], dashdate[9:10], dashdate[0:4]) 
            logging.debug("slashdate: {}".format(slashdate))
            session['endday'] = slashdate
            if fieldtext[-8:] != "vent_end":
                logging.debug("**********here***********")
                logging.debug(fieldtext)
                session['endtime'] = fieldtext[len(fieldtext)-fieldtext.find(" ") +2:-3] 
                session['endtimeampm'] = ampmformat(session['endtime'])
            else: 
                session['endtime'] = "event_end"
                session['endtimeampm'] = "endtime am/pm"
             
        session['startday'] = session["Start Date"]
        logging.debug(session['startday'])
        if (session['startday'] == friday_date):
            session['dayheader'] = friday_header
        elif (session['startday'] == saturday_date):
            session['dayheader'] = saturday_header
        elif (session['startday'] == sunday_date):
            session['dayheader'] = sunday_header
        elif (session['startday'] == ''):
            session['dayheader'] = noday_header
            session['startday'] = "5/3/2019"
        else:
            logging.debug("start date doesn't match'")
            logging.debug(session['startday'])
        logging.debug(session['dayheader'])        
            #print fieldtext

        if  (field == "Start Time"):
            if fieldtext != "Start Time":
                if fieldtext == '':
                    fieldtext = "16:20"
                session['starttime'] = fieldtext
                session['event_start'] = fieldtext
                #print fieldtext
                #session['starttime']= fieldtext[len(fieldtext)-fieldtext.find(" ") +2:]   
                session['starttimeampm'] = ampmformat(session['starttime']) 
                starttimeampmset.add(session['starttimeampm'])
            else:   
                session['starttime'] = "event_start"
                session['event_start'] = "event_start"
                session['starttimeampm'] = "starttime am/pm"
        if  (field == "End Date"):
            session['endday'] = fieldtext
            if (fieldtext == ''):
                session['endday'] = "5/5/2019"

        if  (field == "End Time"):
            if fieldtext != "End Time":
                if fieldtext == '':
                    fieldtext = "16:42"
                session['endtime'] = fieldtext
                #print "setting endtime " + fieldtext
                session['event_end'] = fieldtext            
                #session['starttime']= fieldtext[len(fieldtext)-fieldtext.find(" ") +2:]
                session['endtimeampm'] = ampmformat(session['endtime']) 
            else:   
                session['endtime'] = "event_end"
                session['event_end'] = "event_end"
                session['endtimeampm'] = "endtime am/pm"

        if  (field == "Book Description" or field == "description"): 
                    session['description'] = \
                        re.sub(r', , ',', ', re.sub(r',,',', ', re.sub(r'\n',', ', fieldtext))).strip(', \t\n\r')
                    session['descriptionascii'] = session['description'] 
        if  (field == "Location" or field == "venue"):
            session['venue'] = re.sub(r'\n',', ', fieldtext).strip(', \t\n\r')
            temproom = re.sub(r'\s','', fieldtext)
            temproom = re.sub(r'\(','', temproom)
            temproom = re.sub(r'\)','', temproom)
            temproom = re.sub(r'/','', temproom)
            if temproom == '':
                temproom = "Hotel"
            session['roomnosp'] = temproom
            tempbookroom = replace_all(session['venue'], {"&":" ","  ":" "})
            session['booklocation'] = tempbookroom
            if fieldtext not in rooms:
              rooms.append(fieldtext)
              roomsdict[fieldtext] = temproom
            
        if  (field == "Presenters" or field == "speakers"):
            session['speakers'] = \
                re.sub(r', , ',', ' ,re.sub(r',,',', ' ,re.sub(r'\n',', ', fieldtext))).strip(', \t\n\r')
        if  (field == "Title" or field == "name"):
            session['name'] = re.sub(r'"','\'' ,re.sub(r', , ',', ' ,re.sub(r',,',', ' ,re.sub(r'\n',', ', fieldtext))))
            temptext = replace_all(fieldtext, addamps)
            temptext = re.sub(r', , ',', ' ,re.sub(r',,',', ' ,re.sub(r'\n',', ', temptext))).strip(', \t\n\r')
            session['bookname'] = temptext

        if  (field == "Track" or field == "event_type"):
            session['event_type'] = fieldtext.strip(', \t\n\r')
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
              session['private'] = "PUBLIC"#fieldtext
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

        # this is clean up below was required because the sched output
        # included some html symbols and tags which would not have looked
        # good in the program book
        # dictionary of the other text to be converted to clean up the sched.org output
        reps = {"&nbsp;":" ", "<br />":"", "&":" and ", "&amp;":" and ", "<p>":"", "</p>":"", "</a>":"", "&ldquo;":"\"", "&rdquo;":"\"", "&rsquo;":"\'", "&ndash;":"-", "\n":" ", "  ":" ", "\r":" "}
        amps = {"&":" and ", "  ":" "}
        quoterep = {"\"":"'"}
        addamps = {"&":"&amp;", "\n":" "}
        commarep = {",":"-","\n":" "}
        # do the replacements and put the values into the proper session field
        temptext = replace_all(fieldtext, reps)
        temptext = replace_all(temptext, amps)
        session[field] = replace_all(temptext, amps)
        if field == "Book Description" or field == "description":
            temptext = replace_all(fieldtext, quoterep)
            session['caldescrip'] = temptext
            temptext = replace_all(temptext, commarep)
            session['csvsafedescrip'] = temptext
            temptext = replace_all(fieldtext.strip('\n'), addamps).strip(', \t\n\r')
            session['bookdescrip'] = temptext
        if field == "Presenters" or field == "speakers":
            temptext = replace_all(fieldtext, quoterep)
            session['calspeakers'] = re.sub(r'\n',',', temptext).strip(', \t\n\r')
        if field == "Presenters" or field == "speakers":
            testtext = fieldtext.split(', ')
            #for x in testtext:
            #    print x
# this first one is a for the first entry which is intentionally dummy data
    if (session['starttime'] ==  "event_start") or (session['startday'] ==  "Start Day"):
        session['duration'] = "duration"
        session['hours'] = 0
        session['minutes'] = 0
        session['totalminutes'] = 0
        session['avneeds'] = "none"
    else:
        logging.debug("Session: %s", session['name'])
        logging.debug("start day %s",  session['startday'])
        logging.debug("start day %s",  session['startday'][3:-5])
        logging.debug("start time %s", session['starttime'][:-3])
        logging.debug("end day %s", session['endday'])
        logging.debug("end day %s", session['endday'][3:-5])
        logging.debug("end time %s", session['endtime'][-5:-3])
        logging.debug("end minutes %s", session['endtime'][-2:])
        logging.debug("event_start %s", session['event_start'])
        logging.debug("event_end %s", session['event_end'])

        session['duration'], session['hours'], session['minutes'], session['totalminutes']  = calcduration(int(session['startday'][2:-5]), int(session['starttime'][:-3]) , int(session['endday'][2:-5]) , int(session['endtime'][-5:-3]), session['endtime'][-2:])
        if session['hours'] > 8:

            session['allday'] = "TRUE"
            session['All Day Event'] = "TRUE"
            session['alldayorder'] = "1"
        else:
            session['allday'] = "FALSE"
            session['alldayorder'] = "2"
            session['All Day Event'] = "FALSE"

    session['speakerlist'] = session['speakers'].split(", ")
    session['speakernosp'] = ""
    for speaker in session['speakerlist']:
            tempspeaker = re.sub(r'\s','', speaker)
            tempspeaker = re.sub(r'\(','', tempspeaker)
            tempspeaker = re.sub(r'\)','', tempspeaker)
            tempspeaker = re.sub(r'/','', tempspeaker)
            tempspeaker = re.sub(r'"','-', tempspeaker).strip('., \t\n\r')
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

# sort the list of sessions here by day then by time.
# if the spreadsheet is in order use the index for sorting
# otherwise implement an index for the sessions in another ways
#sessions = sessions.sort(key=itemgetter('name'))
#sessions = sessions.sort(key=itemgetter('tracknosp'))
sessions = sorted(sessions, key=itemgetter('starttime'))
sessions = sorted(sessions, key=itemgetter('startday'))
#sessions = sessions.sort(key=itemgetter('name'))
#logging.debug( sorted(sessions, key=itemgetter('alldayorder')))

sessions = sorted(sessions, key=itemgetter('alldayorder'))
logging.debug( sessions[1])
starttimelist = sorted(starttimeampmset)
rooms.sort()
alphabetical_rooms = {}
for room in rooms:
    alphabetical_rooms[room] = {'name':room,'Friday':{},'Saturday':{},'Sunday':{}}

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
with open(rp + conyear + ".penguicon.schedule.alldata.json",'w') as myoutput:
    json.dump(sessions, myoutput, indent=4, separators=(',', ': '))
with open(rp + conyear + ".penguicon.schedule.json",'w') as myoutput:
    fields = {"location":"Location", "book_description":"Book Description",
              "title":"Title", "track":"Track", "minutes":"totalminutes",
              "start_date":"Start Date", "end_date":"End Date",
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
with open(rp + conyear + ".penguicon.schedule.alltimes.xml",'w') as myoutput:
  with open(rp + conyear + ".penguicon.schedule.allrooms.mixedin.xml",'w') as schedbyroom:
    for index, y in enumerate(sessions):
#      print y
      if constart != y['event_start'] and "duration" != y['duration']:
        if tempstart == "test":
            heading = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?><events xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">"
            myoutput.write(heading)
            schedbyroom.write(heading)
        #print y
        #logging.debug("in programbook output")
        #logging.debug(y['duration'])
        if not y['All Day Event'] == tempstart:
            if y['All Day Event'] == "TRUE" :
                myoutput.write("\n<day>All Weekend</day>\n")
            else:
                temptext = "\n<day>"+ y['dayheader'] + "</day>\n<time>"+ y['starttimeampm'] + "</time>\n"
                myoutput.write(temptext)
            tempstart = y['event_start']

        if "50 minutes" == y['duration']:
            myoutput.write(hourtemplate % y)
            schedbyroom.write(schedule_by_room_hour_template % y)
        elif "" == y['venue']:
            myoutput.write(programbook_template_no_room % y)
            schedbyroom.write(schedule_by_room % y)
        else: 
            myoutput.write(programbook_template % y)
            schedbyroom.write(schedule_by_room % y)

    myoutput.write('</events>\n')
    schedbyroom.write('</events>\n')
myoutput.close()
#"""

# schedule by room and by speaker output

with open( rp + conyear + ".penguicon.fullschedule.csv",'w') as fullschedule:
    fullschedule.write(schedule_header) # schedule_header needs to be written
    for room in roomsdict:
        with open(schedulebyroomdir + roomsdict[room] + ".csv",'w') as temproomsched:
            tocrooms.add(room)
            temproomsched.write(schedule_header)
            temproomsched.close()
    for index, y in enumerate(sessions):
      for speakernosp in y['speakernosplist']:
        if speakernosp != '':
            with open(speakerdir  + speakernosp + ".csv",'w') as tempspeakersched:        
            #with open(speakerdir + speakernosplist[speakernosp] + ".cvs", 'w') as tempspeakersched:
                tocspeakers.add(speakernosp)
                tempspeakersched.write(calendar_header)
                tempspeakersched.close()
    for index, y in enumerate(sessions):
        #if not y['All Day Event'] == 'All Day Event':
            fullschedule.write(schedule_csv_template % y)
            with open(schedulebyroomdir + y['roomnosp'] + ".csv",'a') as temproomsched:
                temproomsched.write(schedule_csv_template % y)
            temproomsched.close()
            for speaker in y['speakernosplist']:
                if speaker != '':
                    with open(speakerdir  + speaker + ".csv",'a') as tempspeakersched:
                        tempspeakersched.write(speaker_calendar_template % y)
            for speaker in y['speakerlist']:
                if speaker in speakersagendas:
                    speakersagendas[speaker].append(y)
                else:
                    speakersagendas[speaker] = [y]


fullschedule.close()
#print "check this out"
#print speakersagendas['James Hice'][1]

#print "\n\n"

with open(rp + conyear + ".penguicon.speakers.3plus.txt",'w') as discountedspeaker:
    with open(rp + conyear + ".penguicon.speakers.txt",'w') as fullspeakerlist:
        with open(rp + conyear + ".penguicon.speakers.with.minutes.txt",'w') as fullspeaker:
            for key, value in sorted(speakerdict.iteritems(), key=lambda (k, v): (k, v)):
                if value >= 150:
                    discountedspeaker.write("%s\n" % (key))
                fullspeaker.write("%s, %s\n" % (key, value))
                fullspeakerlist.write("%s\n" % (key))

fullspeaker.close()
discountedspeaker.close()
fullspkrlist = []
with open(rp + conyear + ".penguicon.spkrs.bylast.3plus.txt", 'w') as dscountedspkr:
  with open(rp + conyear + ".penguicon.spkrs.bylast.txt", 'w') as fullspkr:
    for key, value in sorted(speakerdict.iteritems(), key=lambda (k, v): (k, v)):
        if value >= 150:
            dscountedspkr.write("%s\n" % (key))
        fullspkrlist.append( str(value)+ " "+ key)
        #fullspkr.write("%s\n" % (key, value))
    for x in sorted(fullspkrlist):
        fullspkr.write("%s\n" % x)

fullspkr.close()
dscountedspkr.close()

# one calendar per track/type of programming
#  also output the full calendar
with open( caldir + conyear + ".penguicon.fullcalendar.csv",'w') as fullcalendar:
  #with open(caldir + conyear + ".penguicon.speakers.txt",'w') as fullspeaker:
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

test = penguicon_tv.render(events=sessions)
testbook = testbook_template.render(events=sessions)
speakersgithubtoc = presentersgithubtoc.render(presenters=sorted(tocspeakers))
roomsgithubtoc = presentersgithubtoc.render(presenters=sorted(tocrooms))
presenterpacket = presenterpacket_template.render(agendas=speakersagendas, speakers=sorted(speakers))
#for x in sessions:
#    print x['bookname']

with open(rp + conyear + ".penguicon_tv.txt", 'w') as myoutput:
    myoutput.write(test)

with open(rp + conyear + ".testingprogrambook.xml", 'w') as myoutput:
    myoutput.write(testbook)
with open("penguicon.schedule.xml", 'w') as myoutput:
    myoutput.write(testbook)
    
with open(speakerdir +"README.md", 'w') as myoutput:
    myoutput.write(speakersgithubtoc)
with open(schedulebyroomdir +"README.md", 'w') as myoutput:
    myoutput.write(speakersgithubtoc)
with open(rp + conyear + ".presenters_packets.txt", 'w') as myoutput:
    myoutput.write(presenterpacket)

"""
schedule by room
"""
""" reset the tempstart variable so that the heading is added to the top of the files """
tempstart = "test" 
printallday = True

sessions.sort(key=itemgetter('venue'))
with open(rp + conyear + ".penguicon.schedule.roomorder.xml",'w') as myoutput:
  with open(rp + conyear + ".penguicon.schedule.allrooms.xml",'w') as schedbyroom:
    for index, y in enumerate(sessions):
#      print y
      if constart != y['event_start'] and "duration" != y['duration']:
        if tempstart == "test":
            heading =  "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?><events xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">"
            myoutput.write(heading)
            schedbyroom.write(heading)
        #print y
        if not y['All Day Event'] == tempstart:
            if y['All Day Event'] == "TRUE" and printallday:
                myoutput.write("\n<day>All Weekend</day>\n")
                schedbyroom.write("\n<day>All Weekend</day>\n") #schedule_by_room_allweekend_template
                printallday = False
            else:
                temptext =  "\n<day>"+ y['dayheader'] + "</day>\n<time>"+ y['starttimeampm'] + "</time>\n"
                myoutput.write(temptext)
                
            tempstart = y['event_start']

        if "50 minutes" == y['duration']:
            myoutput.write(hourtemplate % y)
            schedbyroom.write(schedule_by_room_hour_template % y)
        elif y['All Day Event'] == "TRUE":
            myoutput.write(programbook_template_no_room % y)
            schedbyroom.write(schedule_by_room_allweekend_template % y)
        else: 
            myoutput.write(programbook_template % y)
            schedbyroom.write(schedule_by_room % y)

    myoutput.write('</events>\n')
    schedbyroom.write('</events>\n')
myoutput.close()

### end schedule by room ###

# write out the speakers and their events ...this doesn't work yet
#speaker_events_dict
#writer = csv.writer(open(rp + 'speaker_events_dict.csv', 'wb'))
#for x,y in enumerate(speaker_events_dict):
#for key, value in speaker_events_dict.items():
#    writer.writerow([key, ', '.join(value)] )
#    print key, "is in", len(value), " event(s) which is/are", ', '.join(value)


### conyear.penguicon.schedule.allrooms.xml ###

# Fix the multiple entries of the current room issue  (thanks Matt)
inputfile = open(rp + conyear + '.penguicon.schedule.allrooms.xml', 'r')
outputfile = open('penguicon.schedules.per.room.xml', 'w')

# current room is set to the initial room which is currently no room... this could change year to year
currentroom = '<room>Algonquin A</room>'

# this line is used for 'all weekend events' 
# which are typically listed in the beginning
# before any other events in the program book
# then the variable is reused in the loop
lastroom = '<room></room>'
last = '<room></room>'
lasttime = '<day>All Weekend</day>'
lastday = '<day>All Weekend</day>'
firstroom = True
firstday = True
for row in inputfile:
    if '<room>' in row:
        currentroom = row
        if currentroom != lastroom:
            outputfile.write(row)
            lastroom = row
            lastday = "<day>All Weekend</day>"
    elif '<day>' in row:
        currentday = row
        if row == "<day>All Weekend</day>":
            outputfile.write("got here")
            outputfile.write(lastday)
        if currentday != lastday:
            outputfile.write(row)
            lastday = row
        #if firstday == True:
        #    outputfile.write(row)
        #    firstday = False
        #else:
        #    print "made it here"
        #    print row
        #    outputfile.write(row)
        #    firstroom = False
    else: # If this is not a time row
        outputfile.write(row)

inputfile.close()
outputfile.close()
print "probable success processing csv and exporting to various formats"

linetoprint = []
for x in rooms:
    if x == '':
        x = "''"
    linetoprint.append(x)
linetoprint = ",".join(linetoprint)
