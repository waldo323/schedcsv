
import csv, sys


#import csv
#test_file = 'test.csv'
#csv_file = csv.DictReader(open(test_file, 'rb'), delimiter=',', quotechar='"')



# is the file being listed in the command line?
if len(sys.argv) > 1:
    filename = sys.argv[1]
    
else:
    # if not then use penguicon.csv as a default
    filename = "sched.csv"

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

schedule_file = readInCSV(filename)

# go through the schedule row by row
for index, x in enumerate(schedule_file.schedule):
    # (re)initialize a session dictionary object
    session = {} 
    # for each field grab the data and put it in the session dictionary
    for field in fields:
        # bring the field info into a variable to help keep the code clean
        fieldtext = schedule_file.schedule[index][schedule_file.headerdict[field]]

        # separate the time and day into different variables
        
        session['input'] = x
        session['index'] = index