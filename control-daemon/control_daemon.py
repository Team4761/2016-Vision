import logging
from networktables import NetworkTable
import os
import time

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()

log.debug("Initializing NetworkTables...")
NetworkTable.setIPAddress("roborio-4761-frc.local")
NetworkTable.setClientMode()
NetworkTable.initialize()
table = NetworkTable.getTable("control_daemon")
log.debug("NetworkTables intitialized!")

log.debug("Setting default values for flags...")
table.putBoolean("shutdown_flag", False)
table.putBoolean("reboot_flag", False)
table.putBoolean("start_vision_flag", False)
log.debug("Default flag values set!")

log.debug("Entering main loop...")
while True:
	if table.getBoolean("reboot_flag", False):
		log.info("Reboot flag is true! Rebooting...")
		os.system("reboot")
	if table.getBoolean("shutdown_flag", False):
		log.info("Shutdown flag is true! Shutting down...")
		os.system("shutdown -h now")
	if table.getBoolean("start_vision_flag", False):
		log.info("Vision flag is true! Starting vision program...")
		os.system("python 2016-Vision/python/vision.py")
	log.debug("No flags set to true. Sleeping for five seconds...")
	time.sleep(5)
