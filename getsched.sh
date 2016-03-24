#!/usr/bin/env bash

# get schedule from google docs
#wget --output-documuent sched.csv "https://docs.google.com/spreadsheet/ccc?key=0AiCkD773xnvKdHZ5NU9OcThZNXVDZDBONXdVQjJ5T3c&output=csv"

#rm ./sched.csv
echo get the schedule from google drive
# wget --output-document sched.csv "https://docs.google.com/spreadsheet/ccc?key=0AsysQw--cSRTdEd4b005YmhGZmVTNUtzZXlCR0Z0WlE&output=csv"


wget --output-document sched.csv https://docs.google.com/spreadsheets/d/1WFOl4XmKqsfvPQz46d2gRzFZEYrqIBj9Urmgsj0sNq4/pub?output=csv &
wait %1

#schedule for 2015
#wget --output-document sched.csv https://docs.google.com/spreadsheets/d/1WFOl4XmKqsfvPQz46d2gRzFZEYrqIBj9Urmgsj0sNq4/export?format=csv&id=1WFOl4XmKqsfvPQz46d2gRzFZEYrqIBj9Urmgsj0sNq4 &
#wait %1


# schedule for 2014
#wget --output-document sched.csv "https://docs.google.com/a/penguicon.org/spreadsheet/ccc?key=0AiCkD773xnvKdHlLQS1FR2gyS2ppR0Q5a3FGSWlQUkE&output=csv"

#wget --output-document sched.csv "https://docs.google.com/spreadsheet/ccc?key=0AiCkD773xnvKdHZ5NU9OcThZNXVDZDBONXdVQjJ5T3c&output=csv"

SCHEDDATE=`date`

# process schedule into its various output files
echo process the data
python schedcsv.py sched.csv && echo looks good!

echo post process the speakerlists
awk '{x=$NF; $NF=""; print x ", " $0 }' ./output/2016.penguicon.speakers.3plus.txt |sort > ./output/2016.penguicon.spkrs.bylast.3plus.txt 

awk '{x=$NF; $NF=""; print x ", " $0 }' ./output/2016.penguicon.speakers.txt |sort> ./output/2016.penguicon.spkrs.bylast.txt 

echo got schedule and ran parsing script
