# minecraft-tg

Bash script which links chats in Telegram messenger with in-game chat on Spigot Minecraft server and allows sending commands to Spigot remotely. 

Every chat message on the Minecraft server is sent to the selected Telegram chat and every message from that chat is sent to the Minecraft server. Another selected chat gets the entire server log sent to it live.

If selected user (admin) starts his message on Telegram with slash, it's sent to the server as a command. Effects of that command can be seen in the chat which gets server log.

Script in action: https://imgur.com/a/yRjor

# Usage

At minimum, you must put chat IDs other configuration variables in the tg.sh and run it. Spigot must be run with [GNU screen](https://www.gnu.org/software/screen/manual/screen.html). Screen session must be named spigot for tg.sh to work correctly.

# Files

* tg.sh - main file,  which starts sending messages between Telegram and Spigot when executed

* spigot.service - example systemd service unit to run spigot with [GNU screen](https://www.gnu.org/software/screen/manual/screen.html) when Linux is starting

* spigottg.service - example systemd service unit to run tg.sh when Linux is starting

# Config variables at the start of tg.sh

* botToken - Telegram bot's token

* spigot - spigot directory absolute path with slash at the end (tg.sh will make directory "tg" for its files there)

* adminUsername - user who will be able to send commands

* messageChatID - ID of chat which will get messages from Minecraft (user or group chat)

* adminChatID - ID of chat which will get the entire server log (user or group chat)

# Links

* [Telegram bot API](https://core.telegram.org/bots/api)

* [how to find chat ID](https://stackoverflow.com/questions/32683992/find-out-my-own-user-id-for-sending-a-message-with-telegram-api/)
