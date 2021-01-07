#!/bin/bash

umask 0002

trap './command.sh stop; wait' SIGTERM
screen -DmS spigot -h 5000 java -Dlog4j.configurationFile=log4j2.xml -Xmx9100M -Xms9100M -jar spigot-1.16.4.jar nogui &
wait
