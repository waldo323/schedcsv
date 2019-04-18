import AsciiDammit
import csv
import jinja2
import logging
"""#import consettings"""
logging.basicConfig(level=logging.INFO)

conyear = "2019"
rp = "./output/"

trackinfo = [
    {"ACTION ADVENTURE": 'Action Adventure focuses on "how tos" like demonstrations and workshops on martial arts skills, weaponry, archery, as well as the popular Geeks with Guns event.'},
    {"AFTER DARK": "Come explore our events including frank and often hilarious discussion of sex, kink, and other adult-oriented content. Must be over 18."},
    {"ANIME": "Do you love Anime or Manga? There will be panels on everything from GITS (Ghost in the Shell) to MLP (My Little Pony).  You'll find passionate fans to discuss anime with, presenters to show you some you've never seen, and thought provoking questions about some of the classics!"},
    {"COMICS": "This year, our comics track won't only be a celebration of web based comics - we're going to cover every medium from the comic shop to the best Marvel and DC movies."},
    {"COSTUMING":
        "What goes into a costume? Just like that thrift store find, with a bit of creativity (and maybe a hot glue gun) it can be whatever you want it to be.  The costuming track is a place to learn to create or modify costumes and props with a bit of makeup thrown in so you can really inhabit your character."},
    {"DIY": "Whether it be a new craft or odd jobs around the home or even running your own business, DIY wants to help you learn. Pick up new tools to use in daily life, start a new hobby, or find an interest in a new branch of creativity."},
    {"FOOD": "From kitchen basics to imaginative recipes, the Food Track hosts tastings and general demos on cooking and mixology, to demos on specialty processes like brewing and cheese-making."},
    {"GAMING":
        "Gaming Track is bigger and better than ever.  Literally.  This year, in addition to our awesome gaming area and library, U-Con will be bringing their board game library to share (all 145 of their games!), and Lansing Maker Network ]is bringing some of their giant versions of popular games like Mega-Operation, GianTRIS (aka Mega-Tetris), and Colossal Connect Four! "},
    {"LIFE": "If you want to learn how to survive the apocalypse, make friends as an introvert, sleep entirely with naps, or talk about spirituality, sexuality, gender in fandom, or geek lifestyle topics in general, this is the track for you!"},
    {"LITERATURE": "Writers working in the field of speculative fiction discuss relevant issues, from shop talk on the craft of writing to changes and standards in the world of publishing. Thinking of starting that short story or novel?  Want to know what's hot in] the field of science fiction, fantasy, and horror, from Star Wars to Stephen King and all things in between?  Come check out the Literature track!"},
    {"MAYHEM": "Mayhem is what happens when you leave the panels behind.  Play some giant Jenga, earn some con badges from the Scouts or get your fortune read.  There are lots of activities going on all convention long, look around and you'll find some fun!"},
    {"MEDIA": "The Media Track is a combination of video, film, social media (including YouTube), and other fields for creators and fans of any medium. Panels for creators and entrepreneurs will have tips on screen writing, podcasting, and other emergin mediums. Local films will also be shown with Question/Answer periods for the creative minds behind them."},
    {"PENGUICON": "Official Penguicon Events that don't fit into other tracks, such as Opening Ceremonies, Closing Ceremonies,the Penguicon Board Meeting and the Costume Contest too!"},
    {"SCIENCE": "Science Fiction inspires and has been inspired by work done by scientists. The Science track brings you telescope viewings, hands-on chemistry and robotics, discussions on the future of disease prevention, and a chance to walk the scale of the solar system."},
    {"TECH": "Tux the Penguin is the official mascot of the open source operating system Linux, and at Penguicon we bring you experts in all kinds of open source software, security, and privacy at various levels of expertise, so even a relative novice will find something interesting and useful. If you use a computer or a smartphone, you will find something useful."}
]
tracklist = [
    'actionadventure',
    'afterdark',
    'anime',
    'comics',
    'costuming',
    'diy',
    'food',
    'gaming',
    'life',
    'literature',
    'mayham',
    'media',
    'penguicon',
    'science',
    'tech'
]

with open('sched.csv', 'rb') as infile:
    reader = csv.reader(infile)
    build = list(reader)

trackdict = {}

logging.debug("schedule in list form: \n%s", build)

for line in build:
    logging.debug("line: %s", line)
    logging.debug(len(line))
    atrac = line[5].split(',')[0]
    for currenttrac in trackinfo:
        if currenttrac.keys()[0][0:3] == atrac[0:3].upper():
            logging.debug("track: %s", atrac[0:3].upper())
            logging.debug("current track: %s", currenttrac.keys()[0])
            logging.debug("line[6] %s", line[6])
            trackcontent = [AsciiDammit.asciiDammit(line[6]),  # .decode('unicode_escape').encode('ascii', 'ignore'),
                            AsciiDammit.asciiDammit(line[8]),
                            AsciiDammit.asciiDammit(line[7]), ]  # .decode('unicode_escape').encode('ascii', 'ignore')]
            if currenttrac.keys()[0] not in trackdict.keys():
                trackdict[currenttrac.keys()[0]] = [trackcontent]
            else:
                if trackcontent not in trackdict[currenttrac.keys()[0]]:
                    trackdict[currenttrac.keys()[0]].append(trackcontent)
    logging.debug(line)

for track in trackdict:
    trackdict[track].sort()
logging.debug("sorted dict's list\n\n")
logging.debug("track dictionary: %s", trackdict)

env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
template = env.get_template('programmingtemplate.html')

test = template.render(data=trackdict, trackdata=trackinfo)

with open(rp + conyear + ".full_current_data_for_website.html", 'w') as myoutput:
    myoutput.write(test)

#print test
