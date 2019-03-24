#!/bin/bash

# Telegram bot's token
botToken=""
# spigot directory absolute path with slash at the end
spigot="/home/mcserver/spigot/"
# user who will be able to send commands
adminUsername=""
# ID of chat which will get messages from Minecraft (user or group)
chatID=""
# ID of chat which will get the entire server log (user or group)
adminID=""


# bot API URL
tgURL="https://api.telegram.org/bot"$botToken"/"
# spigot log file relative path
logFile="$spigot/tg/temp.log"
# chat log file relative path
chatFile="$spigot/tg/chat.temp.log"


# infinite loop
while true
do

  #
  # Spigot server -> Telegram (out)
  #

  # copy log files to memory
  log=`cat $logFile`
  chat=`cat $chatFile`

  if [[ ! -z "$log" || ! -z "$chat" ]]; then
    > $logFile  # erase files
    > $chatFile
    python3 out.py "$botToken" "$adminID" "$chatID" "$log" "$chat" >> json.log
  fi

  #
  # Telegram -> Spigot server (in)
  #

  python3 in.py "$botToken" "$adminID" "$chatID" "$adminUsername" >> json.log

  #
  # wait a second before sending requests again
  #
  
  sleep 1
done
