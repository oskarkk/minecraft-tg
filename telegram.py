import requests

def send(token, id, text, parse_mode=0):
  url = 'https://api.telegram.org/bot'+token+'/sendMessage'
  dic = {'chat_id': id, 'text': text}
  if parse_mode: dic['parse_mode'] = parse_mode
  return requests.post(url, json=dic).json()

def log(text):
  with open('json.log', 'a') as f:
    f.write(str(text)+'\n')