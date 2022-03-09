import os
import time
import subprocess
import threading
import logging as log
import sys
import signal
import requests

from incoming import from_tg
from outgoing import to_tg


log.basicConfig(
    format='%(asctime)s [%(levelname)s %(threadName)s] %(message)s',
    handlers=[
        log.FileHandler('data/bot.log'),
        log.StreamHandler(sys.stdout)
    ],
    level=log.DEBUG
)
# remove "Starting new HTTPS connection" etc.
log.getLogger('urllib3').setLevel(log.INFO)


def log_exit(sig, *args):
    log.info(f"bot stopped: {sig} {signal.strsignal(sig)}\n\n")
    os._exit(0)


for sig in (signal.SIGABRT, signal.SIGINT, signal.SIGTERM):
    signal.signal(sig, log_exit)

bot_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(bot_dir)


def get_cfg():
    if os.path.exists('config.py'):
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
                '# request timeout in seconds (appears that max is 50 or so)',
                'timeout = 300'
            ]))
        log.warning('config genereated - fill it and restart')
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
    mc_log_file = cfg.spigot_path + '/tg/temp.log'
    mc_chat_file = cfg.spigot_path + '/tg/chat.temp.log'
    
    while True:
        with open(mc_log_file, 'r+') as l, open(mc_chat_file, 'r+') as c:
            mc_log = l.read()
            mc_chat = c.read()

            l.truncate(0)
            c.truncate(0)

        if mc_log or mc_chat:
            to_tg(mc_log, mc_chat)

        time.sleep(0.2)


if __name__ == '__main__':
    log.info(" ")
    log.info("  BOT STARTED")
    log.info(" ")
    get_cfg()

    # reset online users (user count will be inaccurate)
    with open('data/users.txt', 'w') as file:
        pass

    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            return

        log.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

    sys.excepthook = handle_exception
    threading.excepthook = handle_exception

    in_thread = threading.Thread(target=from_tg_loop)
    in_thread.name = "from_tg"
    out_thread = threading.Thread(target=to_tg_loop)
    out_thread.name = "to_tg"
    in_thread.start()
    out_thread.start()
