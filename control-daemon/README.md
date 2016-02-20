Control Daemon
==============
NetworkTables-powered daemon that runs on the Raspberry Pi that can be used to control the Pi remotely.

Table
-----
Table used by this program is `control_daemon`.

Variables:

| Key                 | Type    | Description                                       |
|---------------------|---------|---------------------------------------------------|
| `reboot_flag`       | Boolean | When true, daemon will reboot the Raspberry Pi    |
| `shutdown_flag`     | Boolean | When true, daemon will power-off the Raspberry Pi |
| `start_vision_flag` | Boolean | When true, daemon will run the vision script      |
