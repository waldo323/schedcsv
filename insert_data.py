import csv_reader
import models

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


"""database connection """
engine = create_engine(r'sqlite:////home/jhice/projects/schedcsv/schedule.db', echo=True) #connect to database
engine.text_factory = str
Session = sessionmaker(bind=engine)
session = Session()

""" read in csv file"""
FILENAME = "sched.csv"
SCHEDULEFILE = csv_reader.Readincsv(FILENAME)

"""add items to db"""
#for dk, di in csv_db_map.iteritems():
#	print dk, di
#print SCHEDULEFILE.dbsched[1]
for events in SCHEDULEFILE.dbsched:
	#for event in events:
	#[self.dbsched.append({self.db_csv_map.get(event_data):row[event_data]})\
    #                    for event_data in row]
    #add_event = models.spreadsheetdb(name='ed', fullname='Ed Jones', password='edspassword' for k,i in events.iteritems())


    add_event = models.spreadsheetdb(end_date=str(events.get("end_date")),
        all_day_event=str(events.get("all_day_event")),
        title=str(events.get("title")),
        track=str(events.get("track")),
        private=str(events.get("private")),
        start_time=str(events.get("start_time")),
        book_description=str(events.get("book_description")),
        presenters=str(events.get("presenters")),
        end_time=str(events.get("end_time")),
        location=str(events.get("location")),
        duration=str(events.get("duration")),
        start_date=str(events.get("start_date")),
        av_needs=str(events.get("av_needs")),)
    print session.dirty
    session.add(add_event)
    #print events.get("av_needs")
    #print events, "\n"
    #print "end_date", events.get("end_date"), "all_day_event", events.get("all_day_event"), events.get("title"), events.get("track"),\
    #      events.get("private"), events.get("start_time"), events.get("book_description"), events.get("presenters"),\
    #      events.get("end_time"), events.get("location"), events.get("duration"), events.get("start_date"), events.get("av_needs")
    #print "\n"

    #for k, i in events.iteritems():
    #	print k, i
    #	if k == "av_needs":
    #       print "\n"
session.commit()


    