#!/usr/bin/env python
inputfile = open('penguicon.schedule.xml', 'r') 
outputfile = open('2019.penguicon.final.schedule.xml', 'w')

currenttime = '<time>4 PM</time>'
lasttime = '<time>All Weekend</time>'

for row in inputfile:
    if '<time>' in row:
        currenttime = row
        if currenttime != lasttime:
            outputfile.write(row)
            lasttime = row
    else: # If this is not a time row
        outputfile.write(row)

inputfile.close()
outputfile.close()

