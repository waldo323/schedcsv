#!/usr/bin/env python
inputfile = open('penguicon.schedule.xml', 'r') 
outputfile = open('2019.penguicon.final.schedule.xml', 'w')

currenttime = '<time>4 PM</time>'
lasttime = '<time>All Weekend</time>'
lastrow = ''

for row in inputfile:
    if '<time>' in row:
        currenttime = row
        if currenttime != lasttime:
            if "<day>All Weekend</day>" in lastrow:
                outputfile.write("<time>All Weekend</time>")
            else:
                outputfile.write(row)
                lasttime = row
    else: # If this is not a time row
        outputfile.write(row)
    lastrow = row

inputfile.close()
outputfile.close()

