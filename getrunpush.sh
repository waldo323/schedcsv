#!/usr/bin/env bash
echo update repo first!
git pull

# clean up previous output files
#git rm ./output/2014.*
#git rm ./output/2015.*
#git rm ./output/schedbyspeaker/*.csv
#git rm ./output/schedbyroom/*
git rm ./output/schedsbyspeaker.zip
#git rm ./output/calendars/*
echo get schedule and run the parsing script on the schedule 
./getsched.sh

# make it easier to find the schedule
cp penguicon.schedule.xml ./output/penguicon.schedule.xml 
# copy to final schedule
cp penguicon.schedule.xml 2015.penguicon.final.schedule.xml 
# zip up the speakers' csv import to ical files
cd ./output/schedbyspeaker && zip -j ../schedsbyspeaker.zip ./* && cd ../../
#git add ./output/schedsbyspeaker.zip
#git add -A
echo time and date of task  
date
# push the schedule and output files to github ./pushsched.sh
git status|awk '/Changes/&&/not/&&/staged/{system("./pushsched.sh")}'
./pushsched.sh
