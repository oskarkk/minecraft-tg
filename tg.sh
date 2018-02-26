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
adminChatID=""


# bot API URL
tgURL="https://api.telegram.org/bot"$botToken"/"
# spigot log file relative path
mclog="logs/latest.log"


cd $spigot
mkdir -p tg


# infinite loop
while true
do


#
# Spigot server -> Telegram
#

# copy latest log file
cp $mclog tg/current.log
# leave only lines that aren't in the previous log copy and remove color formatting
awk 'NR==FNR{a[$0]=1;next}!a[$0]' tg/last.log tg/current.log | sed 's/[\x1B][^m]*m//g' > tg/temp.log

# while temp.log isn't empty...
while [[ -s tg/temp.log ]]
do
  # cut first 30 lines from it and put them to "line" variable
  line=$(head -n 30 tg/temp.log)
  echo -n "$(tail -n +31 tg/temp.log)" > tg/temp.log
  # escaping some chars
  line=${line//\\/\\\\}
  line=${line//\'/\\\'}
  line=${line//\"/\\\"}

  # send everything to the admin chat on Telegram...
  result=$(curl -sH "Content-Type: application/json" -d '{"chat_id":138268771,"text":"'"$line"'"}' $tgURL"sendMessage")
  # and log server response (for debugging)
  echo $result | jq . >> tg/json.log


  # choose the lines which contain chat messages
  line=$(echo "$line" | grep "Chat Thread")
  if [ -n "$line" ]
  then
    # remove unneeded parts of the message, leave time
    line=$(echo "$line" | sed 's/^\(\[..:..:..\] \)[^<]*</\1</g')
    # send that to the non-admin chat on Telegram
    result=$(curl -sH "Content-Type: application/json" -d '{"chat_id":'"$chatID"',"text":"'"$line"'"}' $tgURL"sendMessage")
    # log server response (for debugging)
    echo $result | jq . >> tg/json.log
  fi

done

# replace the previous log with the current log
cp tg/current.log tg/last.log





#
# Telegram -> Spigot server
#

# get the first message from bot
json=$(curl -s $tgURL"getUpdates?limit=1")

# loop which sends the message from bot to the server and gets the next messages
while (( $(echo $json | jq '.result | length') == 1 ))
do

  # log JSON data (for debugging)
  echo $json | jq . >> tg/json.log
  # get message ID from JSON
  id=$(echo $json | jq -r '.result[].update_id')
  # get message content from JSON
  message=$(echo $json | jq -r '.result[].message.text')

  # if the meesage has content (if it hasn't it's image for example)
  if [ "$message" != "null" ]
  then
    # get sender's username from JSON
    username=$(echo $json | jq -r '.result[].message.from.username')
    # add "say" and username to the message
    messageToSend="say <<"$username">> "$message

    # if the message was sent by the admin, check if it's a command...
    if [ "$username" = "$adminUsername" ]
    then
      # if it's a command, remove "say", username and slash
      messageToSend=$(echo $messageToSend | sed 's/^say <<'"$adminUsername"'>> \///g')
    fi

    # send message to the spigot server through screen, the terminal manager
    screen -p 0 -S spigot -X eval "stuff "'\042'"$messageToSend"'\042'"\\015"
  fi

  # get the next message from bot
  json=$(curl -s $tgURL"getUpdates?limit=1&offset="$((id + 1)) )

done



# wait a second before sending requests again
sleep 1
done
