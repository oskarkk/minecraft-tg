from datetime import datetime
import logging as log

import telegram as tg
import config as cfg


def from_tg():
	data = tg.getUpdates(timeout=cfg.timeout)
	updatesNum = len(data['result'])
	commands = []

	# tg gives max 100 updates
	# get more updates till there are none
	while updatesNum > 0 :
		log.debug(f"updates from tg: {data['result']}")
		for update in data['result']:
			try:
				if update['channel_post']['chat']['username'] == cfg.channelID[1:]:
					newtitle = update['channel_post']['new_chat_title']
					log.info(f"new chat title found: {newtitle}")
					postID = update['channel_post']['message_id']
					tg.delete(cfg.channelID, postID)
					continue
			except KeyError:
				pass

			try:
				# get content of the message
				message = update['message']['text']
			except KeyError:
				# if key doesn't exist, discard update and go to the next update
				continue

			chatID = update['message']['chat']['id']
			# try block added 2021-01
			# after user without username caused endless spam on the server
			try:
				username = update['message']['from']['username']
				displayname = '§3@§l' + username
				if username == cfg.tgAdminUsername:
					displayname = '§6[Prezes] ' + displayname
			except KeyError:
				username = None
				displayname = '§3§l'+update['message']['from']['first_name']
				if lastname := update['message']['from'].get('last_name'):
					displayname += ' ' + lastname

			# discard message if it isn't from "console" or "chat" chat
			if chatID not in [cfg.consoleID, cfg.chatID]: continue
			# discard messages from linked channel
			if displayname == 'Telegram': continue

			for line in message.splitlines():
				# if the message was sent by the admin and it's a command
				if username == cfg.tgAdminUsername and line[0] == '/' :
					# remove slash and bot's name
					commands.append(line[1:].replace('@OskarkBot', ''))
				else:
					line = line.replace('^','\^')  # without this you can stop server by sending just ^C
					line = line.replace('"','')
					line = line.replace('\\','')
					# add username, hour and Minecraft command "tellraw"
					time = datetime.now().strftime('%H:%M')
					minecraft = f'tellraw @a "{time} {displayname}§r §l>§r {line}"'
					# add broadcast to Discord
					discord = f'discord broadcast [TG] {displayname} » {line}'
					commands += [minecraft, discord]

		# get the next updates
		lastID = data['result'][-1]['update_id']
		data = tg.getUpdates(timeout=0, offset=(lastID + 1))
		updatesNum = len(data['result'])
	
	for command in commands:
		log.info(f'command: {command}')

	# return messages (which are passed to gnu screen)
	return '\n'.join(commands)
