#!/usr/bin/env python
from operator import itemgetter
inputfile = open('penguicon.schedule.xml', 'r') 
outputfile = open('2019.penguicon.final.schedule.xml', 'w')

currenttime = '<time>4 PM</time>'
lasttime = '<time>All Weekend</time>'

for index, row in enumerate(inputfile):
    if '<time>' in row:
        currenttime = row
        if currenttime != lasttime:
            outputfile.write(row)
            lasttime = row
        if "<day>All Weekend</day>" in inputfile[index-1]:
            outputfile.write("<time>All Weekend</time>")
    else: # If this is not a time row
        outputfile.write(row)

inputfile.close()
outputfile.close()

