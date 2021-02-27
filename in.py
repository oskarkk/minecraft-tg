import re, requests
from datetime import datetime

import telegram as tg, config as conf

data = tg.getUpdates(conf.token)
updatesNum = len(data['result'])

# tg gives max 100 updates
# get more updates till there are none
while updatesNum > 0 :
  for update in data['result']:
    try:
      if update['channel_post']['chat']['username'] == conf.channelID[1:]:
        if 'new_chat_title' in update['channel_post']:
          postID = update['channel_post']['message_id']
          tg.delete(conf.token, conf.channelID, postID)
    except KeyError:
      pass

    try:
      # get content of the message
      message = update['message']['text']
    except KeyError:
      # if key doesn't exist, discard update and go to the next update
      continue

    chatID = update['message']['chat']['id']
    # try block added 2021-01
    # after user without username caused endless spam on the server
    try:
      username = update['message']['from']['username']
      displayname = '@' + username
    except KeyError:
      username = None
      displayname = update['message']['from']['first_name']
      if lastname := update['message']['from'].get('last_name'):
        displayname += ' ' + lastname

    # discard message if it isn't from "console" or "chat" chat
    if chatID not in [conf.consoleID, conf.chatID]: continue
    # discard messages from linked channel
    if displayname == 'Telegram': continue

    for line in message.splitlines():
      # if the message was sent by the admin and it's a command
      if username == conf.adminUsername and line[0] == '/' :
        line = line[1:]  # remove slash
      else:
        line = line.replace('^','\^')  # without this you can stop server by sending just ^C
        line = line.replace('"','')
        line = line.replace('\\','')
        # add username, hour and Minecraft command "say"
        time = datetime.now().strftime('%H:%M')
        line = 'tellraw @a "' + time + ' <<' + displayname + '>> ' + line + '"'
      # send messages to output (which is passed to gnu screen)
      print(line+'\n')

  # get the next updates
  lastID = data['result'][-1]['update_id']
  data = tg.getUpdates(conf.token, lastID + 1)
  updatesNum = len(data['result'])
