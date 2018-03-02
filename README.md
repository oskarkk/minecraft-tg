# minecraft-tg

Bash script which links chats in Telegram messenger with in-game chat on Spigot Minecraft server and allows sending commands to Spigot remotely. 

Every chat message on the Minecraft server is sent to the selected Telegram chat and every message from that chat is sent to the Minecraft server. Another selected chat gets the entire server log sent to it live.

If selected user (admin) starts his message on Telegram with slash, it's sent to the server as a command. Effects of that command can be seen in the chat which gets server log.

Script in action: https://imgur.com/a/yRjor

# Usage

[First you must make a Telegram bot for your server.](https://core.telegram.org/bots#6-botfather) It's very easy, no coding required, everything's in the Telegram app. When you're done, start chat with your bot or make a group (and make your bot admin of that group so it can see the messages). Then you must edit tg.sh and put chat IDs and other configuration variables at the start of the file. Then run it.

Spigot must be run with [GNU screen](https://www.gnu.org/software/screen/manual/screen.html). Screen session must be named "spigot" for tg.sh to work correctly. See file spigot.service for the exact command.

When you will send message to the bot, it will appear in Spigot with some small delay (usually 0.5-2s).

If you want tg.sh to run automatically with system startup you can use the spigottg.service file.

# Files

* tg.sh - main file,  which starts sending messages between Telegram and Spigot when executed

* spigot.service - example systemd service unit to run spigot with [GNU screen](https://www.gnu.org/software/screen/manual/screen.html) when Linux is starting

* spigottg.service - example systemd service unit to run tg.sh when Linux is starting

# Config variables at the start of tg.sh

* botToken - Telegram bot's token

* spigot - spigot directory absolute path with slash at the end (tg.sh will make directory "tg" for its files there)

* adminUsername - user who will be able to send commands

* messageChatID - ID of chat which will get messages from Minecraft (user ID or ID of group chat where )

* adminChatID - ID of chat which will get the entire server log (user or group chat)

# Dependencies

* [curl](https://curl.haxx.se/)

* [jq](https://stedolan.github.io/jq/)

* [screen](https://www.gnu.org/software/screen/)

To install:

    sudo apt-get install screen jq curl

# Links

* [Telegram bot API](https://core.telegram.org/bots/api)

* [how to find chat ID](https://stackoverflow.com/questions/32683992/find-out-my-own-user-id-for-sending-a-message-with-telegram-api/)
