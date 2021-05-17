import sys, re, requests
import users, telegram as tg, config as conf

admin_call = re.compile(r'(.+: `.*\b(admin|prezes|prezesie)\b)', re.IGNORECASE)
discord = re.compile('Chat: \[Discord]')
message_prefix = re.compile('([0-9]{2}:[0-9]{2} )?(\[Discord] )?(.+?) > ', re.MULTILINE)

# put log & chat strings to vars
logs = {'console': sys.argv[1]}
if sys.argv[2]:
  logs['chat'] = sys.argv[2]
  # change username font to monospace with markdown and strip timestamp
  logs['chat'] = discord.sub('[Discord]', logs['chat'])
  logs['chat'] = message_prefix.sub(r'`\2\3: `', logs['chat'])
  logs['chat'] = admin_call.sub(r'\1 \[@' + conf.adminUsername + ']', logs['chat'])

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
      tg.send(conf.token, conf.consoleID, lines)
    else:  # chat log
      tg.send(conf.token, conf.chatID, lines, 'Markdown')

try:
  with open('data/users.txt', 'r') as file:
    usersOnline = {line[:-1] for line in file}
except FileNotFoundError:
  usersOnline = set()

loginsAndLogouts = ''

# choose only lines with logging in and out
for line in logs['console'].splitlines():
  if 'logged in with entity id' in line:
    user = line.split('[',1)[0]
    usersOnline.add(user)
    loginsAndLogouts += '✅  ' + user + ' wszedł do gry!\n'
  elif 'left the game' in line:
    user = line.split(' left the',1)[0]
    usersOnline.discard(user)
    loginsAndLogouts += '❌  ' + user + ' wyszedł z gry\n'

# send these lines to the channel
if loginsAndLogouts:
  #loginsAndLogouts = '\n'.join(loginsAndLogouts)
  tg.send(conf.token, conf.channelID, loginsAndLogouts)
  tg.chatTitle(conf.token, conf.channelID, 'Wieliczka (' + str(len(usersOnline)) + ' online)')
  with open('data/users.txt', 'w') as file:
    out = ''
    for user in usersOnline:
      out += user + '\n'
    file.write(out)
