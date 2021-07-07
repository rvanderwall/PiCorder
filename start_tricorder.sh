#!/bin/bash
# /etc/init.d/start_tricorder.sh
### BEGIN INIT INFO
# Provides:          start_tricorder.sh
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start daemon at boot time
# Description:       Enable service provided by daemon.
### END INIT INFO

cd /home/pi/projects/PiCorder/t_env
source bin/activate
cd /home/pi/projects/PiCorder
python main.py &
