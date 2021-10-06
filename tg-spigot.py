import json
from os import chdir, path
import time
from incoming import from_tg
from outgoing import to_tg
import subprocess

bot_dir = path.dirname(path.realpath(__file__))
chdir(bot_dir)

def init():
    if path.exists('config.py'):
        global cfg
        import config as cfg
        while True:
            start_bot()
            time.sleep(2)
            
    else:
        with open('config.py', 'w') as f:
            f.write('\n'.join([
                "# Spigot server's path without slash at the end",
                'spigot_path = ""',
                "# Telegram bot's token",
                'token = ""',
                '# username (w/o @) of the user who will be able to send commands',
                'adminUsername = ""',
                '# ID of chat which will get messages from Minecraft (user or group)',
                'chatID = 0',
                '# ID of chat which will get the entire content of the spigot console (user or group)',
                'consoleID = 0',
                '# @username of channel with login/logout messages',
                'channelID = "@"',
            ]))
        print('config genereated - fill it and restart')

def start_bot():
    
    log_file = cfg.spigot_path + '/tg/temp.log'
    chat_file = cfg.spigot_path + '/tg/chat.temp.log'

    with open(log_file, 'r+') as l, open(chat_file, 'r+') as c:
        log = l.read()
        chat = c.read()

        l.truncate(0)
        c.truncate(0)

    if log or chat:
        resp = to_tg(log, chat)
        if resp: open('data/json.log', 'a').write(resp)

    if not (formatted_lines := from_tg()): return
    subprocess.run(['sudo', '-u', 'mc', '/home/mc/command.sh', formatted_lines])

init()

