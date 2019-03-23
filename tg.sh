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
  python3 out.py "$log" "$chat" "$adminID" "$chatID" >> json.log
fi

#
# Telegram -> Spigot server (in)
#

# get the first message from bot
json=$(curl -s $tgURL"getUpdates?limit=1")

# loop which sends the message from bot to the server and gets the next messages
while (( $(echo $json | jq '.result | length') == 1 ))
do

  # log JSON data (for debugging)
  echo $json | jq . >> json.log
  # get message ID from JSON
  id=$(echo $json | jq -r '.result[].update_id')
  # get message content from JSON
  message=$(echo $json | jq -r '.result[].message.text')

  # get chat ID from JSON
  somechatID=$(echo $json | jq -r '.result[].message.chat.id')

  # if the meesage has content (if it hasn't it's image for example)
  # and it's from admin or message chat on Telegram
  if [[ "$message" != "null" ]] && [[ "$somechatID" = "$chatID" || "$somechatID" = "$adminID" ]]
  then
    # escape dollar sign
    message=${message//$/\"$\"}

    # get sender's username from JSON
    username=$(echo $json | jq -r '.result[].message.from.username')

    # temp var
    message2=""
    # for every line in "message"
    while read -r line; do

      # if the message was sent by the admin and it's a command...
      if [[ "$username" = "$adminUsername" ]] && [[ "$line" =~ ^/ ]]
      then
        # if it's a command, remove slash
        line=$(echo "$line" | sed 's/^\///g')
      else
        # add "say" and username to the line
        line="say <<""$username"">> ""$line"
      fi

      # add line to the message
      message2="$message2""$line"$'\n'

    done <<< "$message"
    message="$message2"

    # send message to the spigot server through screen, the terminal manager
    screen -p 0 -S spigot -X eval "stuff "'\042'"$message"'\042'"\\015"
  fi

  # get the next message from bot
  json=$(curl -s $tgURL"getUpdates?limit=1&offset="$((id + 1)) )

done


# wait a second before sending requests again
sleep 1
done
