#!/usr/bin/env bash
## git add . for adding all changes
SCHEDDATE=`date`
echo staging to local repo
git add .
## git commit for committing those changes to the local repo
echo committing to local repo
git commit -a -m "updated schedule to the lastest downloaded version as of $SCHEDDATE"

## git push sends it up to github
echo pushing up to github
git push


echo push successful!
