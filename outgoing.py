import re
import telegram as tg, config as cfg


regex_admin_mention = r'(.+: `.*\b(' + cfg.triggers + r')\b)'

re_admin_mention = re.compile(regex_admin_mention, re.IGNORECASE | re.MULTILINE)
re_message_prefix = re.compile('([0-9]{2}:[0-9]{2} )?(\[Dsc] )?(.+?) > ', re.MULTILINE)
re_color_formatting = re.compile('[\x1B][^m]*m', re.MULTILINE)

re_login = re.compile(r'^(\w*)\[.* logged in with entity id')
re_logout = re.compile(r'^(\w*) lost connection: ')


def to_tg(console, chat):
    # put log & chat strings to vars
    logs = {cfg.consoleID: console}
    if chat:
        chat = chat.replace('Chat: [Dsc]', '[Dsc]')
        # change username font to monospace with markdown and strip timestamp
        chat = re_message_prefix.sub(r'`\2\3: `', chat)
        chat = re_admin_mention.sub(r'\1 \[@' + cfg.tgAdminUsername + ']', chat)
        logs[cfg.chatID] = chat

    for chat_id, msg_content in logs.items():
        # remove color formatting
        msg_content = re_color_formatting.sub('', msg_content)
        lines = msg_content.splitlines()
        span = 20  # how many lines per message
        # join every <span> lines
        joined_lines = ['\n'.join(lines[r:r+span]) for r in range(0, len(lines), span)]

        markdown = 'Markdown' if chat_id == cfg.chatID else None
        # send logs to the respective chats
        for lines in joined_lines:
            tg.send(chat_id, lines, markdown)

    try:
        with open('data/users.txt', 'r') as file:
            users_online = {line[:-1] for line in file}
    except FileNotFoundError:
        users_online = set()

    logins_logouts = ''

    # choose only lines with logging in and out
    for line in logs[cfg.consoleID].splitlines():
        # 'logged in with entity id' in line
        if login := re_login.match(line):
            user = login.group(1)
            if user == cfg.mcAdminUsername: continue
            users_online.add(user)
            logins_logouts += '✅  ' + user + ' wszedł do gry!\n'
        elif logout := re_logout.match(line):
            user = logout.group(1)
            if user == cfg.mcAdminUsername: continue
            users_online.discard(user)
            logins_logouts += '❌  ' + user + ' wyszedł z gry\n'
        elif line.startswith('Prezes zstąpił na Wieliczkę.'):
            user = cfg.mcAdminUsername
            users_online.add(user)
            logins_logouts += '✅  ' + user + ' wszedł do gry!\n'
        elif line.startswith('Prezes opuścił grę.'):
            user = cfg.mcAdminUsername
            users_online.discard(user)
            logins_logouts += '❌  ' + user + ' wyszedł z gry\n'

    # send these lines to the channel
    if logins_logouts:
        #loginsAndLogouts = '\n'.join(loginsAndLogouts)
        tg.send(cfg.channelID, logins_logouts)
        tg.chatTitle(cfg.channelID, 'Wieliczka (' + str(len(users_online)) + ' online)')
        with open('data/users.txt', 'w') as file:
            out = ''
            for user in users_online:
                out += user + '\n'
            file.write(out)
