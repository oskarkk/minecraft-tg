from requests import post, get
from requests.exceptions import RequestException
from datetime import datetime as time
from config import token
import logging as log
from time import sleep


def logg(text):
  with open('data/json.log', 'a') as f:
    f.write( str(time.now()) + " " + str(text) + '\n' )


def api(method, request, data=None):
  url = 'https://api.telegram.org/bot' + token + '/' + method
  log.debug(f'request: {method} {data}')
  
  while True:
    try:
      if request == post:
        resp = request(url, json=data).json()
      elif request == get:
        if data: url += data
        resp = request(url).json()
      break
    except RequestException as e:
      log.error(e)
      sleep(1)
      continue
    
  # if not {'ok': True, 'result': []}
  if not resp.get('ok'):
    log.error(resp)
  elif not resp['result']:
    log.debug('no updates')

  return resp


def getUpdates(timeout=0, offset=None):
  data = '?timeout=' + str(timeout)
  if offset:
    data += '&offset=' + str(offset)
  return api('getUpdates', get, data)


def send(id, text, parse_mode=None):
  dic = {'chat_id': id, 'text': text}
  if parse_mode: dic['parse_mode'] = parse_mode
  return api('sendMessage', post, dic)


def chatTitle(id, title):
  dic = {'chat_id': id, 'title': title}
  return api('setChatTitle', post, dic)


def delete(chat, message):
  dic = {'chat_id': chat, 'message_id': message}
  return api('deleteMessage', post, dic)
