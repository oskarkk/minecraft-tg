import sys, re, requests

token = sys.argv[1]
url = 'https://api.telegram.org/bot'+token+'/sendMessage'
consoleChatID = sys.argv[2]
chatChatID = sys.argv[3]

# put log & chat strings to vars
logs = {'console': sys.argv[4]}
if sys.argv[5]:
  logs['chat'] = sys.argv[5]
  # change username font to monospace with markdown
  logs['chat'] = re.sub('(<.+>)', r'`\1`', logs['chat'], re.MULTILINE)

for logType, logContent in logs.items():
  # remove color formatting
  logContent = re.sub('[\x1B][^m]*m', '', logContent)
  lines = logContent.splitlines()
  span = 20  # how many lines per message
  lines = ['\n'.join(lines[r:r+span]) for r in range(0, len(lines), span)]

  for li in lines:
    if logType == 'console':  # console log
      dic = {'chat_id': consoleChatID, 'text': li}
    else:  # chat log
      dic = {'chat_id': chatChatID, 'text': li, 'parse_mode': 'Markdown'}
    print(dic)
    resp = requests.post(url, json=dic)
    print(resp.json())
