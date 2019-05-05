#!/usr/bin/env bash
echo update repo first!
git pull
CWD="/home/jhice/projects/schedcsv"
# clean up previous output files
#git rm ./output/2014.*
#git rm ./output/2015.*
#git rm ./output/2016.*
#git rm ./2016.*
git rm $CWD/output/schedbyspeaker/*.csv
git rm $CWD/output/schedbyroom/*
git rm $CWD/output/schedsbyspeaker.zip
#git rm ./output/calendars/*
echo get schedule and run the parsing script on the schedule 
$CWD/getsched.sh 5ea81a81d7732d9c00787a401fce3d3a
$CWD/removeextratime.py
cp 2019.penguicon.final.schedule.xml penguicon.schedule.xml

# make it easier to find the schedule
cp $CWD/penguicon.schedule.xml $CWD/output/penguicon.schedule.xml 
# copy to final schedule
#cp penguicon.schedule.xml 2019.penguicon.final.schedule.xml 
# zip up the speakers' csv import to ical files
cd $CWD/output/schedbyspeaker && zip -j ../schedsbyspeaker.zip ./* && cd ../../
#git add ./output/schedsbyspeaker.zip
#git add -A
echo time and date of task  
date
# push the schedule and output files to github ./pushsched.sh
git status|awk '/Changes/&&/not/&&/staged/{system("./pushsched.sh")}'
$CWD/pushsched.sh
