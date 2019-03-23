import sys, re, requests

token = ''
url = 'https://api.telegram.org/bot'+token+'/getUpdates'

# get first updates from bot (max 100)
resp = requests.post(url)
print(resp.json())
updatesNum = len(resp['result'])

while ( updatesNum > 0 ):
  
  # stop if there are no more updates
  if( updatesNum < 100 ):
    break

  # get the next updates
  lastId = resp['result'][99]['update_id']
  resp = requests.post( url+'offset='+(lastId + 1) )
  print(resp.json())