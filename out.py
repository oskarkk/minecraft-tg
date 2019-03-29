import sys, re, requests, telegram as tg

token = sys.argv[1]
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
      resp = tg.send(token, consoleChatID, li)
    else:  # chat log
      resp = tg.send(token, chatChatID, li, 'Markdown')
    print(resp)