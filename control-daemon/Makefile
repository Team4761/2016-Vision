install:
	cp control_daemon.py /usr/local/bin
	cp etc/control_daemon.service /etc/systemd/system
	systemctl enable /etc/systemd/system/control_daemon.service
	@echo Install complete! Reboot so changes can take effect!
uninstall:
	systemctl stop /etc/systemd/system/control_daemon.service
	systemctl disable /etc/systemd/system/control_daemon.service
	rm /usr/local/bin/control_daemon.py
	rm /etc/systemd/system/control_daemon.service
