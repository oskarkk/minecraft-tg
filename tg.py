import sys, re, requests

token = ''
url = 'https://api.telegram.org/bot'+token+'/sendMessage'

# log & chat
logs = [ sys.argv[1] ]
if sys.argv[2]:
  logs.append(sys.argv[2])
  # bold usernames with markdown
  logs[1] = re.sub('(<.+>)', r'`\1`', logs[1], re.MULTILINE)

for i, log in enumerate(logs):
  # remove color formatting
  log = re.sub('[\x1B][^m]*m', '', log)
  lines = log.splitlines()
  span = 20  # how many lines per message
  lines = ['\n'.join(lines[r:r+span]) for r in range(0, len(lines), span)]

  for li in lines:
    dic = {'chat_id': sys.argv[i+3], 'text': li}
    if i == 1:
      dic['parse_mode'] = 'Markdown'
    print(dic)
    resp = requests.post(url, json=dic)
    print(resp.json())
