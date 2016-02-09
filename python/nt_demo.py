#!/usr/bin/python

#python nt_demo.py roborio-4671-frc.local

import sys
import time
from networktables import NetworkTable

import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()

try:
	ip = sys.argv[1]
except IndexError:
	ip = "roborio-4761-frc.local"
	log.warning("No IP address set; assuming default")

log.info("Using IP address: {}".format(ip))

log.info("Setting up NetworkTables...")
NetworkTable.setIPAddress(ip)
NetworkTable.setClientMode()
NetworkTable.initialize()

table = NetworkTable.getTable("TestTable")

i = 0
while True:
	table.putNumber("xxx", i)
	try:
		log.info("local: {} & remote: {}".format(i, table.getNumber("xxx")))
	except KeyError:
		log.warning("Could not read from NetworkTable. This is bad.")
	i += 1
	time.sleep(1)
