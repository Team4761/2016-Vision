import logging
from networktables import NetworkTable
import subprocess
import time

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()

log.debug("Initializing NetworkTables...")
NetworkTable.setIPAddress("roborio-4761-frc.local")
NetworkTable.setClientMode()
NetworkTable.initialize()
table = NetworkTable.getTable("control_daemon")
log.debug("NetworkTables intitialized!")

def reset_flags():
	log.debug("Setting default values for flags...")
	table.putBoolean("shutdown_flag", False)
	table.putBoolean("reboot_flag", False)
	log.debug("Default flag values set!")

reset_flags()

log.debug("Entering main loop...")

while True:
	table.putNumber("last_updated", time.time())
	if table.getBoolean("reboot_flag", False):
		reset_flags()
		log.info("Reboot flag is true! Rebooting...")
		subprocess.Popen(["reboot"])
	if table.getBoolean("shutdown_flag", False):
		reset_flags()
		log.info("Shutdown flag is true! Shutting down...")
		subprocess.Popen(["shutdown", "-h", "now"])
	log.debug("No flags set to true. Sleeping for five seconds...")
	time.sleep(5)
