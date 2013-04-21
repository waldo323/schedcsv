#!/usr/bin/env bash

# get schedule from google docs
#wget --output-documuent sched.csv "https://docs.google.com/spreadsheet/ccc?key=0AiCkD773xnvKdHZ5NU9OcThZNXVDZDBONXdVQjJ5T3c&output=csv"

SCHEDDATE=`date`

wget --output-document sched.csv "https://docs.google.com/spreadsheet/ccc?key=0AiCkD773xnvKdHZ5NU9OcThZNXVDZDBONXdVQjJ5T3c&output=csv"

# process schedule into its various output files
python schedcsv.py


# git add . for adding all changes
git add .
# git commit for committing those changes to the local repo
git commit -m "updated schedule to the lastest downloaded version as of $SCHEDDATE"

# git push sends it up to github
git push


