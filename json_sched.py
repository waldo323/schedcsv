# 5ea81a81d7732d9c00787a401fce3d3a
# https://penguicon2019.sched.com/api/session/list?api_key=5ea81a81d7732d9c00787a401fce3d3a&format=json&custom_data=Y

import jinja2
import json
import logging
import urllib2

""" set variables up """
logging.basicConfig(level=logging.WARN)
env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
web_template = env.get_template('programmingtemplate.html')
penguicon_tv = env.get_template('penguicon_tv')
testbook_template = env.get_template('testprogrambook.xml')
presentersgithubtoc = env.get_template('speakerstoc')
presenterpacket_template = env.get_template('presenter_packet_agenda')
tocspeakers = set()
speakersagendas = dict()

pcon_url = "https://penguicon2019.sched.com/api/session/list?api_key=5ea81a81d7732d9c00787a401fce3d3a&format=json&custom_data=Y"

pcon_schedule = json.load(urllib2.urlopen(pcon_url))
