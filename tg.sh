#!/bin/bash

# Telegram bot's token
botToken=""
# spigot directory absolute path with slash at the end
spigot="/home/mcserver/spigot/"
# user who will be able to send commands
adminUsername=""
# ID of chat which will get messages from Minecraft (user or group)
messageChatID=""
# ID of chat which will get the entire server log (user or group)
adminChatID=""


# bot API URL
tgURL="https://api.telegram.org/bot"$botToken"/"
# spigot log file relative path
logfile="tg/temp.log"
# chat log file relative path
chatfile="tg/chat.temp.log"


cd $spigot
mkdir -p tg


# infinite loop
while true
do


#
# Spigot server -> Telegram
#

# copy and erase latest mc and chat log files to memory
log=`cat $logfile`
> $logfile
chat=`cat $chatfile`
> $chatfile

# remove color formatting
log=`echo -n "$log" | sed 's/[\x1B][^m]*m//g'`
chat=`echo -n "$chat" | sed 's/[\x1B][^m]*m//g'`

# escaping some chars
log=${log//\\/\\\\}
log=${log//\'/\\\'}
log=${log//\"/\\\"}
chat=${chat//\\/\\\\}
chat=${chat/\'/\\\'}
chat=${chat//\"/\\\"}

# while log isn't empty...
while [ ! -z "$log" ]
do
  # cut first 30 lines from it and put them to 'lines' variable
  lines=`echo "$log" | head -n 30`
  log=`echo "$log" | tail -n +31`

  # send 'lines' to the admin chat on Telegram...
  result=$(curl -sH "Content-Type: application/json" -d '{"chat_id":'"$adminChatID"',"text":"'"$lines"'"}' $tgURL"sendMessage")
  # and log server response (for debugging)
  echo $result | jq . >> tg/json.log
done

# while chat isn't empty...
while [ ! -z "$chat" ]
do
  # cut first 30 lines from it and put them to 'lines' variable
  lines=`echo "$chat" | head -n 30`
  chat=`echo "$chat" | tail -n +31`

  # send that to the non-admin chat on Telegram
  result=$(curl -sH "Content-Type: application/json" -d '{"chat_id":'"$messageChatID"',"text":"'"$lines"'"}' $tgURL"sendMessage")
  # log server response (for debugging)
  echo $result | jq . >> tg/json.log
  echo penla2
done





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

  # get chat ID from JSON
  chatID=$(echo $json | jq -r '.result[].message.chat.id')

  # if the meesage has content (if it hasn't it's image for example)
  # and it's from admin or message chat on Telegram
  if [[ "$message" != "null" ]] && [[ "$chatID" = "$messageChatID" || "$chatID" = "$adminChatID" ]]
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
