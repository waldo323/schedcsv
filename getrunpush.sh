#!/usr/bin/env bash
echo update repo first!
git pull

echo get schedule and run the parsing script on the schedule 
./getsched.sh


# push the schedule and output files to github
./pushsched.sh
