import sys, re, requests

token = ''
url = 'https://api.telegram.org/bot'+token+'/getUpdates'

data = requests.get(url).json()
print(data)
updatesNum = len(data['result'])

while ( updatesNum > 0 ):

  # get the next updates
  lastID = data['result'][-1]['update_id']
  data = requests.get( url+'?offset='+str(lastID + 1) ).json()
  print(data)
  updatesNum = len(data['result'])
  print(str(lastID)+'\n')
  if (updatesNum > 0):
    print(data['result'][-1])