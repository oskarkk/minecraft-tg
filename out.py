import sys, re, requests, users, telegram as tg

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

loginsAndLogouts = []
re.sub('(\[.*\]).*\[.*\]:(.*\[.*\]){0,1}','\1',logs['console'], re.MULTILINE)
for li in logContent.splitlines():
  if 'logged in!' in li or 'left the game' in li: loginsAndLogouts.append(li)
  
if loginsAndLogouts: 
  loginsAndLogouts = '\n'.join(loginsAndLogouts)
  for userID in users.get():
    tg.send(token, userID, loginsAndLogouts)