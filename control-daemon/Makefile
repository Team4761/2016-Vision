install:
	cp control_daemon.py /usr/local/bin
	cp etc/control_daemon.service /etc/systemd/system
	service control_daemon enable
	@echo Install complete! Reboot so changes can take effect!
uninstall:
	service control_daemon stop
	service control_daemon disable
	rm /usr/local/bin/control_daemon.py
	rm /etc/systemd/system/control_daemon.service
