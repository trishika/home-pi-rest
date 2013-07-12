#!/usr/bin/env python2.7
# -*- encoding: utf-8 -*-
"""
    Home-rest
    ~~~~~~~~~

    :copyright: (c) 2013 by Aurélien Chabot <aurelien@chabot.fr>
    :license: LGPLv3, see COPYING for more details.
"""
try:
	from flask import Flask
	from flask import request, abort
	from flask import json
	from subprocess import call, Popen, PIPE
	from traceback import print_exc
	import threading
	import ConfigParser
	import sys
	import os
except ImportError as error:
	print 'ImportError: ', str(error)
	exit(1)


if len(sys.argv) > 1:
	config = sys.argv[1]
else:
	print("You need to provide a configuration")
	exit(1)

app = Flask(__name__)
app.config.from_pyfile(config, silent=True)

print(config)

try:
	# Switches config
	switches_config = app.config["SWITCHES"]
	with open(switches_config) as f:
		switchesjson = json.load(f)

	# Sensors config
	sensors_config = app.config["SENSORS"]
	with open(sensors_config) as f:
		sensorsjson = json.load(f)
except:
	print('Unabled to load switches or sensors configuration')
	exit(1)

mutex_switches = threading.RLock()
switches = {}
for c in switchesjson:
	switches[c["id"]] = c

mutex_sensors = threading.RLock()
sensors = {}
for c in sensorsjson:
	sensors[c["id"]] = c
	sensors[c["id"]]["cache"] = 0

################### SWITCHES

def call_switch(switchId, status):

	with mutex_switches:
		try:
			#app.logger.info("Set switch %d status, status: %d, new status: %d", switchId, switches[switchId]["status"], status)
			#app.logger.info("command: " + switches[switchId]["command"])

			# Do switch command
			call([switches[switchId]["command"], switches[switchId]["code"], switches[switchId]["number"], str(status)])
			switches[switchId]["status"] = status
		except:
			app.logger.error("Unable to set switches status")
			print_exc()

################### SWITCHES API

# Get list of switches
@app.route("/switches/")
def get_switches():
	return json.dumps(switchesjson)

# Get one switch
@app.route("/switches/<int:switchId>/", methods = ["GET"])
def get_switch(switchId):
	try:
		return json.dumps(switches[switchId])
	except:
		return json.dumps({})

# Set switch status
@app.route("/switches/<int:switchId>/<int:status>/", methods = ["GET"])
def set_switch_status(switchId, status):
	try:
		if not status in ( 1 , 0):
			raise Exception("Invalid status")

		# Take mutex sensors
		with mutex_switches:
			call_switch(switchId, status)
			return json.dumps({"id" : switchId, "status" : switches[switchId]["status"]})
	except:
		return json.dumps({})

################### SENSORS


def invalidate_sensor_cache(sensorId):

	# Take mutex sensors
	with mutex_sensors:
		app.logger.info("Invalidate cache for sensor %d", sensorId)
		sensors[sensorId]["cache"] = 0

def fill_sensor_value(sensorId):

	# Take mutex sensors
	with mutex_sensors:

		if sensors[sensorId]["cache"] == 0:

			# Refresh cache
			try:
				# Get sensor value
				process = Popen([sensors[sensorId]["command"]], stdout=PIPE)
				exit_code = os.waitpid(process.pid, 0)
				output = process.communicate()[0]

				app.logger.info("Get sensor %d value: %s", sensorId, output)
				sensors[sensorId]["value"] = float(output)

			except:
				app.logger.error("Unable to get sensors value")
				print_exc()

			# Set cache
			try:
				threading.Timer(int(app.config["SENSORS_CACHE_TIME"]), invalidate_sensor_cache, [sensorId]).start()
				sensors[sensorId]["cache"] = 1
			except:
				app.logger.error("Unable to set cache")
				print_exc()

################### SENSORS API

# Get list of sensors
@app.route("/sensors/")
def get_sensors():
	return json.dumps(sensorsjson)

# Get one sensors
@app.route("/sensors/<int:sensorId>/", methods = ["GET"])
def get_sensor(sensorId):
	try:
		# Take mutex sensors
		with mutex_sensors:
			fill_sensor_value(sensorId)
			return json.dumps(sensors[sensorId])
	except:
		return json.dumps({})

app.run("0.0.0.0", app.config["PORT"])

