from os import chdir, path
import time
from incoming import from_tg
from outgoing import to_tg
import subprocess
from multiprocessing import Process

bot_dir = path.dirname(path.realpath(__file__))
chdir(bot_dir)

def get_cfg():
    if path.exists('config.py'):
        global cfg
        import config as cfg
    else:
        with open('config.py', 'w') as f:
            f.write('\n'.join([
                "# Spigot server's path without slash at the end",
                'spigot_path = ""',
                "# Telegram bot's token",
                'token = ""',
                '# tg username (w/o @) of the user who will be able to send commands',
                'tgAdminUsername = "wanours"',
                '# minecraft username of admin',
                'mcAdminUsername = "okarkalic"',
                '# ID of chat which will get messages from Minecraft (user or group)',
                'chatID = 0',
                '# ID of chat which will get the entire content of the spigot console (user or group)',
                'consoleID = 0',
                '# @username of channel with login/logout messages',
                'channelID = "@"',
                '# whole words triggering admin mention, separated by vert lines',
                'triggers = "admin|admina"',
            ]))
        print('config genereated - fill it and restart')
        exit()

def from_tg_loop():
    while True:
        formatted_lines = from_tg()
        if formatted_lines:
            # screen -X won't work with other users, it's a bug which has been fixed after
            # something like 10 years, after I reminded the screen developers of that bug in 2020.
            # The fix hasn't been released yet so I must use sudo to execute commands in other users' screen
            subprocess.run(['sudo', '-u', 'mc', '/home/mc/command.sh', formatted_lines])

def to_tg_loop():
    log_file = cfg.spigot_path + '/tg/temp.log'
    chat_file = cfg.spigot_path + '/tg/chat.temp.log'

    while True:
        with open(log_file, 'r+') as l, open(chat_file, 'r+') as c:
            log = l.read()
            chat = c.read()

            l.truncate(0)
            c.truncate(0)

        if log or chat:
            resp = to_tg(log, chat)
            if resp: open('data/json.log', 'a').write(resp)

        time.sleep(0.2)

if __name__ == '__main__':
    get_cfg()
    f = Process(target=from_tg_loop)
    t = Process(target=to_tg_loop)
    f.start()
    t.start()
