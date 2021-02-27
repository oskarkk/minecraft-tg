import requests

def getUpdates(token, offset=None):
  url = 'https://api.telegram.org/bot' + token + '/getUpdates'
  if offset:
    url += '?offset=' + str(offset)
  return requests.get(url).json()

def log(text):
  with open('data/json.log', 'a') as f:
    f.write(str(text)+'\n')

def send(token, id, text, parse_mode=0):
  url = 'https://api.telegram.org/bot'+token+'/sendMessage'
  dic = {'chat_id': id, 'text': text}
  if parse_mode: dic['parse_mode'] = parse_mode
  log(dic)
  resp = requests.post(url, json=dic).json()
  log(resp)

def chatTitle(token, id, title):
  url = 'https://api.telegram.org/bot'+token+'/setChatTitle'
  dic = {'chat_id': id, 'title': title}
  log(dic)
  resp = requests.post(url, json=dic).json()
  log(resp)

def delete(token, chat, message):
  url = 'https://api.telegram.org/bot'+token+'/deleteMessage'
  dic = {'chat_id': chat, 'message_id': message}
  log(dic)
  resp = requests.post(url, json=dic).json()
  log(resp)

