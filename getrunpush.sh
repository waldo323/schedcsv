#!/usr/bin/env bash
echo update repo first!
git pull

# clean up previous outpu files
git rm ./output/2014.*
git rm ./output/schedbyspeaker/*
git rm ./output/schedbyroom/*
git rm ./output/schedsbyspeaker.zip
echo get schedule and run the parsing script on the schedule 
./getsched.sh

# make it easier to find the schedule
cp penguicon.schedule.xml ./output/penguicon.schedule.xml 
# zip up the speakers' csv import to ical files
zip ./output/schedsbyspeaker.zip ./output/schedbyspeaker/*
git add ./output/schedsbyspeaker.zip
echo time and date of task
date
# push the schedule and output files to github ./pushsched.sh
git status|awk '/Changes/&&/not/&&/staged/{system("./pushsched.sh")}'
