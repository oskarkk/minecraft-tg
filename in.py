import sys, re, requests

token = sys.argv[1]
url = 'https://api.telegram.org/bot'+token+'/getUpdates'
consoleChatID = int(sys.argv[2])
chatChatID = int(sys.argv[3])
adminUsername = sys.argv[4]

data = requests.get(url).json()

with open('json.log', 'a') as f:
  f.write(str(data)+'\n')

updatesNum = len(data['result'])

while updatesNum > 0 :
  for update in data['result']:
    # go to the next update unless the update is a message and has text
    try:
      message = update['message']['text']
    except KeyError:
      continue

    messageChatID = update['message']['chat']['id']
    username = update['message']['from']['username']

    # check if message is from "console" or "chat" chat
    if messageChatID not in [consoleChatID, chatChatID]:
      continue

    for line in message.splitlines():
      # if the message was sent by the admin and it's a command
      if username == adminUsername and line[0] == '/' :
        del line[0]  # remove slash
      else:
        line = 'say <<' + username + '>> ' + line
      print(line+'\n')

  # get the next updates
  lastID = data['result'][-1]['update_id']
  data = requests.get( url+'?offset='+str(lastID + 1) ).json()
  with open('json.log', 'a') as f:
    f.write(str(data)+'\n')
  updatesNum = len(data['result'])
