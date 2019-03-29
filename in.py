import sys, re, requests, users, telegram as tg

token = sys.argv[1]
updateURL = 'https://api.telegram.org/bot'+token+'/getUpdates'
consoleChatID = int(sys.argv[2])
chatChatID = int(sys.argv[3])
adminUsername = sys.argv[4]

def getUpdates(url):
  global updatesNum
  global data 
  data = requests.get(url).json()
  with open('json.log', 'a') as f:
    f.write(str(data)+'\n')
  updatesNum = len(data['result'])

getUpdates(updateURL)

while updatesNum > 0 :
  for update in data['result']:
    # go to the next update unless the update is a message and has text
    try:
      message = update['message']['text']
    except KeyError:
      continue

    messageChatID = update['message']['chat']['id']
    chatType = update['message']['chat']['type']
    username = update['message']['from']['username']

    if chatType == 'private':
      if message == '/start':
        users.add(messageChatID)
        tg.send(token,messageChatID,'Włączono powiadomienia o logowaniach')
      elif message == '/stop':
        users.remove(messageChatID)
        tg.send(token,messageChatID,'Wyłączono powiadomienia o logowaniach')

    # check if message is from "console" or "chat" chat
    if messageChatID not in [consoleChatID, chatChatID]:
      continue

    for line in message.splitlines():
      # if the message was sent by the admin and it's a command
      if username == adminUsername and line[0] == '/' :
        line = line[1:]  # remove slash
      else:
        line = 'say <<' + username + '>> ' + line
      print(line+'\n')

  # get the next updates
  lastID = data['result'][-1]['update_id']
  getUpdates( updateURL+'?offset='+str(lastID + 1) )