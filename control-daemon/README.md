Control Daemon
==============
NetworkTables-powered daemon that runs on the Raspberry Pi that can be used to control the Pi remotely.

Table
-----
Table used by this program is `control_daemon`.

Variables:

| Key                 | Type    | Description                                                |
|---------------------|---------|------------------------------------------------------------|
| `reboot_flag`       | Boolean | When true, daemon will reboot the Raspberry Pi             |
| `shutdown_flag`     | Boolean | When true, daemon will power-off the Raspberry Pi          |
| `last_updated`      | Number  | UNIX timestamp of when the daemon last checked for updates |
