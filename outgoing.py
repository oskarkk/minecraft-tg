import re
import logging as log

import telegram as tg
import config as cfg


regex_admin_mention = r'(.+: `.*\b(' + cfg.triggers + r')\b)'

re_admin_mention = re.compile(regex_admin_mention, re.IGNORECASE | re.MULTILINE)
re_message_prefix = re.compile('([0-9]{2}:[0-9]{2} )?(\[Dsc] )?(.+?) > ', re.MULTILINE)
re_color_formatting = re.compile('[\x1B][^m]*m', re.MULTILINE)

re_login = re.compile(r'^(\w*)\[.* logged in with entity id')
re_logout = re.compile(r'^(\w*) lost connection: ')


def to_tg(console, chat):
    # put log & chat strings to vars
    logs = {cfg.console_id: console}
    if chat:
        chat = chat.replace('Chat: [Dsc]', '[Dsc]')
        # change username font to monospace with markdown and strip timestamp
        chat = re_message_prefix.sub(r'`\2\3: `', chat)
        chat = re_admin_mention.sub(r'\1 \[@' + cfg.tg_admin_username + ']', chat)
        logs[cfg.chat_id] = chat

    for chat_id, msg_content in logs.items():
        # remove color formatting
        msg_content = re_color_formatting.sub('', msg_content)
        lines = msg_content.splitlines()
        span = 20  # how many lines per message
        # join every <span> lines
        joined_lines = [
            '\n'.join(lines[r : r + span]) for r in range(0, len(lines), span)
        ]

        markdown = 'Markdown' if chat_id == cfg.chat_id else None
        # send logs to the respective chats
        for lines in joined_lines:
            tg.send(chat_id, lines, markdown)

    logins_logouts(console)


def logins_logouts(console_log):
    user_logins = []
    user_logouts = []

    admin = cfg.mc_admin_username

    # choose only lines with logging in and out
    for line in console_log.splitlines():
        # 'logged in with entity id' in line
        if login := re_login.match(line):
            user = login.group(1)
            if user == admin:
                continue
            user_logins.append(user)
        elif logout := re_logout.match(line):
            user = logout.group(1)
            if user == admin:
                continue
            user_logouts.append(user)
        elif line.startswith('Prezes zstąpił na Wieliczkę.'):
            user_logins.append(admin)
        elif line.startswith('Prezes opuścił grę.'):
            user_logouts.append(admin)

    if not (user_logins or user_logouts):
        return

    with open('data/users.txt', 'r') as file:
        users_online = {line[:-1] for line in file}

    logins_logouts_message = ''

    if user_logins:
        log.info(f'logged in: {user_logins}')
        for user in user_logins:
            users_online.add(user)
            logins_logouts_message += f'✅  {user} wszedł do gry!\n'

    if user_logouts:
        log.info(f'logged in: {user_logouts}')
        for user in user_logouts:
            users_online.discard(user)
            logins_logouts_message += f'❌  {user} wyszedł z gry\n'

    # send these lines to the channel
    if logins_logouts_message:
        # loginsAndLogouts = '\n'.join(loginsAndLogouts)
        tg.send(cfg.channel_id, logins_logouts_message)

        newtitle = f'Wieliczka ({len(users_online)} online)'
        tg.chat_title(cfg.channel_id, newtitle)
        log.info(f'new title: {newtitle}')

        with open('data/users.txt', 'w') as file:
            file.write('\n'.join(users_online) + '\n')
