# minecraft-tg

Bash/python script which links chats in Telegram messenger with in-game chat on Spigot Minecraft server and allows sending commands to Spigot remotely. Optionally it also sends notifications every time someone logs in/out to Telegram users which send "/start" command to the bot.

Every chat message on the Minecraft server is sent to the selected Telegram chat and every message from that chat is sent to the Minecraft server. Another selected chat gets the entire server log sent to it live.

If selected user (admin) starts his message on Telegram with slash, it's sent to the server as a command. Effects of that command can be seen in the chat which gets server log.

Script in action: https://imgur.com/a/yRjor

# Usage

[First you must make a Telegram bot for your server.](https://core.telegram.org/bots#6-botfather) It's very easy, no coding required, everything's in the Telegram app. When you're done, start chat with your bot or make a group (and make your bot admin of that group so it can see the messages). Then you must edit tg.sh and put chat IDs and other configuration variables at the start of the file.

Spigot must be run with [GNU screen](https://www.gnu.org/software/screen/manual/screen.html). Screen session must be named "spigot" for tg.sh to work correctly. See file spigot.service for the exact command.

You must copy log4j2.xml to your server's directory and change the command you're using to start the server (in start.sh) to something like "java -Dlog4j.configurationFile=log4j2.xml -jar spigot-1.11.2.jar". For information on what it does look [here](https://www.reddit.com/r/admincraft/comments/69271l/guide_controlling_console_and_log_output_with/).

Now you can run tg.sh. When you will send message to the bot, it will appear in Spigot with some small delay (usually 0.5-2s).

If you want tg.sh to run automatically with system startup you can use the spigottg.service file.

When someone will start a private converstion with the bot, the bot will start sending messages to that user every time when someone logs in or out. To stop this, the user must stop the bot by clicking "Stop bot" in converstion settings or send "/stop" command to the bot. The latter way is preferred as only then the bot stops trying to send notifications to the user. 

# Files

* tg.sh - main file,  which starts sending messages between Telegram and Spigot when executed

* spigot.service - example systemd service unit to run spigot with [GNU screen](https://www.gnu.org/software/screen/manual/screen.html) when Linux is starting

* spigottg.service - example systemd service unit to run tg.sh when Linux is starting

# Config variables at the start of tg.sh

* botToken - Telegram bot's token

* spigot - spigot directory absolute path with slash at the end (tg.sh will make directory "tg" for its files there)

* adminUsername - user who will be able to send commands

* chatID - ID of chat which will get messages from Minecraft (user or group chat)

* adminID - ID of chat which will get the entire server log (user or group chat)

# Dependencies

* python3

* [requests for python](http://docs.python-requests.org/en/master/)

* [screen](https://www.gnu.org/software/screen/)

To install on Debian-like distros:

    sudo apt-get install screen python3
    pip install requests

# Links

* [Telegram bot API](https://core.telegram.org/bots/api)

* [how to find chat ID](https://stackoverflow.com/questions/32683992/find-out-my-own-user-id-for-sending-a-message-with-telegram-api/)
