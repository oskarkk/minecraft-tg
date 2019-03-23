import sys, re, requests

token = ''
url = 'https://api.telegram.org/bot'+token+'/getUpdates'

# get first updates from bot (max 100)
resp = requests.post(url)
print(resp.json())
updatesNum = len(resp['result'])

while ( updatesNum > 0 ):
  
  # stop if there are no more updates
  #if( updatesNum < 100 ):
  #  break

  # get the next updates
  lastID = resp['result'][-1]['update_id']
  resp = requests.post( url+'offset='+(lastID + 1) )
  print(resp.json())