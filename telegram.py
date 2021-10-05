from requests import post, get
from datetime import datetime as time

def log(text):
  with open('data/json.log', 'a') as f:
    f.write( str(time.now()) + " " + str(text) + '\n' )

def api(token, method, request, data=None):
  url = 'https://api.telegram.org/bot' + token + '/' + method
  if data: log(data)
  if request == post:
    resp = request(url, json=data).json()
  elif request == get:
    if data: url += data
    resp = request(url).json()
  # if not {'ok': True, 'result': []}
  if not resp.get('ok') or resp.get('result'):
    log(resp)
  return resp

def getUpdates(token, offset=None):
  data = None
  if offset:
    data = '?offset=' + str(offset)
  return api(token, 'getUpdates', get, data)

def send(token, id, text, parse_mode=None):
  dic = {'chat_id': id, 'text': text}
  if parse_mode: dic['parse_mode'] = parse_mode
  api(token, 'sendMessage', post, dic)

def chatTitle(token, id, title):
  dic = {'chat_id': id, 'title': title}
  api(token, 'setChatTitle', post, dic)

def delete(token, chat, message):
  dic = {'chat_id': chat, 'message_id': message}
  api(token, 'deleteMessage', post, dic)
