import sys, re, requests

token = sys.argv[1]
url = 'https://api.telegram.org/bot'+token+'/getUpdates'
consoleChatID = sys.argv[2]
chatChatID = sys.argv[3]
adminUsername = sys.argv[4]

data = requests.get(url).json()
with open('json.log', 'a') as f:
  f.write(data)
updatesNum = len(data['result'])

while updatesNum > 0 :
  for update in data['result']:
    message = update['message']['text']
    messageChatID = update['message']['chat']['id']
    # if the meesage has content (if it hasn't it's image for example)
    # and it's from admin or message chat on Telegram
    if message and (messageChatID in [consoleChatID, chatChatID]):
      username = update['message']['from']['user']
      for line in message.splitlines():
        # if the message was sent by the admin and it's a command...
        if username == adminUsername and line[0] == '/' :
          line = line[1:]  # remove slash
        else:
          line = 'say <<' + username + '>> ' + line
        print(line+'\n')

  # get the next updates
  lastID = data['result'][-1]['update_id']
  data = requests.get( url+'?offset='+str(lastID + 1) ).json()
  with open('json.log', 'a') as f:
    f.write(data)
  updatesNum = len(data['result'])