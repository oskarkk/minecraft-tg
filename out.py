import sys, re, requests, users, telegram as tg

token = sys.argv[1]
consoleChatID = sys.argv[2]
chatChatID = sys.argv[3]

# put log & chat strings to vars
logs = {'console': sys.argv[4]}
if sys.argv[5]:
  logs['chat'] = sys.argv[5]
  # change username font to monospace with markdown and strip timestamp
  logs['chat'] = re.sub('[0-9]{2}:[0-9]{2} (<.+?>)', r'`\1`', logs['chat'], re.MULTILINE)

for logType, logContent in logs.items():
  # remove color formatting
  logContent = re.sub('[\x1B][^m]*m', '', logContent)
  lines = logContent.splitlines()
  span = 20  # how many lines per message
  # join every <span> lines
  joinedLines = ['\n'.join(lines[r:r+span]) for r in range(0, len(lines), span)]

  # send logs to the respective chats
  for lines in joinedLines:
    if logType == 'console':  # console log
      tg.send(token, consoleChatID, lines)
    else:  # chat log
      tg.send(token, chatChatID, lines, 'Markdown')

loginsAndLogouts = []
# this doesn't work because the time is already stripped:
# re.sub(r'(\[.*\]).*\[.*\]:(.*\[.*\]){0,1}',r'\1', logs['console'], re.MULTILINE)

# choose only lines with logging in and out
for li in logContent.splitlines():
  if 'logged in with entity id' in li:
    user = li.split('[',1)[0]
    loginsAndLogouts.append(user+' logged in')
  elif 'left the game' in li:
    loginsAndLogouts.append(li)

# send these lines to every "subscribing" user
if loginsAndLogouts:
  loginsAndLogouts = '\n'.join(loginsAndLogouts)
  for userID in users.get():
    tg.send(token, userID, loginsAndLogouts)
