#!/usr/bin/env bash
echo update repo first!
git pull

echo get schedule and run the parsing script on the schedule 
./getsched.sh
echo time and date of task
date
# push the schedule and output files to github ./pushsched.sh
git status|awk '/Changes/&&/not/&&/staged/{system("./pushsched.sh")}'
