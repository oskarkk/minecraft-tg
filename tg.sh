#!/bin/bash

# spigot directory absolute path with slash at the end
spigot="/home/mc/spigot"
# spigot log file relative path
logFile=$spigot'/tg/temp.log'
# chat log file relative path
chatFile=$spigot'/tg/chat.temp.log'


while true
do

  #
  # Spigot server -> Telegram (out)
  #

  # copy log files to memory
  log=`cat $logFile`
  chat=`cat $chatFile`

  if [[ -n "$log" || -n "$chat" ]]; then
    > $logFile  # erase files
    > $chatFile
    python3 out.py "$log" "$chat" >> data/json.log
  fi

  #
  # Telegram -> Spigot server (in)
  #

  formattedLines=`python3 in.py`
  if [[ -n "$formattedLines" ]]; then
    # screen -X won't work with other users, it's a bug which has been fixed after
    # something like 10 years, after I reminded the screen developers of that bug in 2020.
    # The fix hasn't been released yet so I must use sudo to execute commands in other users' screen
    sudo -u mc /home/mc/command.sh "$formattedLines"
    # the old way, I don't know why it was that complicated
    # screen -p 0 -S mc/spigot -X eval "stuff "'\042'"$formattedLines"'\042'"\\015"
  fi

  # wait a second before sending requests again
  sleep 1
done
