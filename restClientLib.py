#!/usr/bin/env python2.7
# -*- encoding: utf-8 -*-
"""
    Home-rest
    ~~~~~~~~~

    :copyright: (c) 2013 by Aurélien Chabot <aurelien@chabot.fr>
    :license: LGPLv3, see COPYING for more details.
"""
try:
	import sys
	import json
	import urllib2
	import threading
	from traceback import print_exc
except ImportError as error:
	print 'ImportError: ', str(error)
	exit(1)

def update_sensor(sensor):
	try:
		url = urllib2.urlopen("%(host)s/sensors/%(id)s/" % { "host" : sensor["host"], "id": sensor["id"] })
		data = json.loads(url.read())
		sensor["value"] = data["value"]
	except:
		print("Failed to update sensor value of sensor %(name)s" % { "name": switch["name"] })
		print_exc()

def set_switch(switch, status):
	try:		
		url = urllib2.urlopen("%(host)s/switch/%(id)s/%(status)d" % { "host" : switch["host"], "id": switch["id"], "status": status  })
		data = json.loads(url.read())
		sensor["status"] = data["status"]
	except:
		print("Failed to set switch %(name)s" % { "name": switch["name"] })
		print_exc()

def get_nodes(servers):
	switches = []
	sensors = []
	for server in servers:
		try:
			# Get switches list
			url = urllib2.urlopen("http://%(host)s:%(port)d/switches/" % { "host" : server["host"], "port" : server["port"] })
			str = url.read()
			server_switches = json.loads(str)
			for switch in server_switches:
				switch["host"] = "http://%(host)s:%(port)d" % { "host" : server["host"], "port" : server["port"] }
			switches.extend(server_switches)
		except:
			print("Failed to load switches for server %(host)s" % { "host": server["host"] })
			print_exc()

		try:
			# Get sensors list
			url = urllib2.urlopen("http://%(host)s:%(port)d/sensors/" % { "host" : server["host"], "port" : server["port"] })
			str = url.read()
			server_sensors = json.loads(str)
			for sensor in server_sensors:
				sensor["host"] = "http://%(host)s:%(port)d" % { "host" : server["host"], "port" : server["port"] }
			sensors.extend(server_sensors)
		except:
			print("Failed to load sensors for server %(host)s" % { "host": server["host"] })
			print_exc()

	print("switches : %(switches)s" % { "switches": switches})
	print("sensors : %(sensors)s" % { "sensors": sensors})

	return switches,sensors