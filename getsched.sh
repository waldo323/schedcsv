#!/usr/bin/env bash

# get schedule from google docs
#wget --output-documuent sched.csv "https://docs.google.com/spreadsheet/ccc?key=0AiCkD773xnvKdHZ5NU9OcThZNXVDZDBONXdVQjJ5T3c&output=csv"

#rm ./sched.csv
echo get the schedule from google drive
wget --output-document sched.csv "https://docs.google.com/spreadsheet/ccc?key=0AiCkD773xnvKdHZ5NU9OcThZNXVDZDBONXdVQjJ5T3c&output=csv"

SCHEDDATE=`date`

# process schedule into its various output files
echo process the data
python schedcsv.py
echo looks good!

# git add . for adding all changes
echo staging to local repo
git add .
# git commit for committing those changes to the local repo
echo committing to local repo
git commit -m "updated schedule to the lastest downloaded version as of $SCHEDDATE"

# git push sends it up to github
echo pushing up to github
git push


echo successful!
