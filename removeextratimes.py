inputfile = open('2013.penguicon.schedule.xml', 'r', encoding='utf-8')
outputfile = open('2013.penguicon.schedule2.xml', 'w', encoding='utf-8')

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
