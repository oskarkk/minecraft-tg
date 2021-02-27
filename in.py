import re, requests
from datetime import datetime

import users, telegram as tg, config as conf

updateURL = 'https://api.telegram.org/bot' + conf.token + '/getUpdates'

def getUpdates(url):
  global updatesNum
  global data
  data = requests.get(url).json()
  # writeToLog(data)
  updatesNum = len(data['result'])

getUpdates(updateURL)

# tg gives max 100 updates
# get more updates till there are none
while updatesNum > 0 :
  for update in data['result']:
    try:
      # get content of the message
      message = update['message']['text']
    except KeyError:
      # if key doesn't exist, discard update and go to the next update
      continue

    messageChatID = update['message']['chat']['id']
    chatType = update['message']['chat']['type']
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

    # check if private message is a command for login notifications
    if chatType == 'private':
      tg.log(update)
      if message == '/start':
        users.add(messageChatID)
        tg.send(conf.token, messageChatID, 'Włączono powiadomienia o logowaniach')
      elif message == '/stop':
        users.remove(messageChatID)
        tg.send(conf.token, messageChatID, 'Wyłączono powiadomienia o logowaniach')

    # discard message if it isn't from "console" or "chat" chat
    if messageChatID not in [conf.consoleID, conf.chatID]:
      continue

    for line in message.splitlines():
      # if the message was sent by the admin and it's a command
      if username == conf.adminUsername and line[0] == '/' :
        # remove slash
        line = line[1:]
      else:
        line = line.replace('^','\^') # without this you can stop server by sending just ^C
        line = line.replace('"','')
        line = line.replace('\\','')
        # add username, hour and Minecraft command "say"
        time = datetime.now().strftime('%H:%M')
        line = 'tellraw @a "' + time + ' <<' + displayname + '>> ' + line + '"'
      # send messages to output (which is passed to gnu screen)
      print(line+'\n')

  # get the next updates
  lastID = data['result'][-1]['update_id']
  getUpdates( updateURL+'?offset='+str(lastID + 1) )
