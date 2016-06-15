#!/usr/bin/env python
# -*- coding: utf-8 -*-

from settings import *
import spaceflight
from date import get_stamp

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Bot
import web
import time
import threading


global_data = {'finish': False,
			 'last_update': 0,
			 'last_check': 0,
			 'lock': threading.Lock(),
			 'launches': [],
			 'db': web.database(dbn='mysql', db=db_name, user=db_user, pw=db_pass)}


def log(log):
	global global_data
	global_data['db'].query('INSERT INTO log (log) VALUES ("%s")' % log)

def start(bot, update):
	bot.sendMessage(update.message.chat_id, text='Hello World!')

def get_launches(flts=None, full=False):
	global global_data

	res = []
	global_data['lock'].acquire()
	for launch in global_data['launches']:
		if flts:
			cont = False
			for flt in flts:
				if flt not in launch['mission'].lower():
					cont = True
					break
			if cont:
				continue

		date = launch['date']

		tm = launch['timestr']

		tm1 = launch['tm1']
		tm2 = launch['tm2']

		if tm1:
			tm = tm1
			if tm1 != tm2:
				tm = '%s - %s' % (tm1, tm2)
		dt = '%s, %s' % (date, tm)

		sub = ''
		if launch['stamp']:
			sub = '/subscribe_%s' % launch['stamp']

		if full:
			res.append('<b>[%s]</b> %s %s\n%s\n' % (dt, launch['mission'], launch['desc'], sub))
		else:
			res.append('<b>[%s]</b> %s %s' % (dt, launch['mission'], sub))

	global_data['lock'].release()

	text = '\n'.join(res)
	return text[:4096]

def sched(args):
	flts = []
	full = False

	try:
		args.pop(0)
		if args[0] == 'desc':
			args.pop(0)
			full = True
		flts = args
	except:
		pass

	return get_launches(flts=flts, full=full)

def subscribe(args, update):
	global global_data

	user_id = update.message.from_user.id

	cmd = args[0]
	cmd = cmd.split('_')
	if len(cmd) > 1:
		args = cmd
	args.pop(0)

	try:
		stamp = int(args[0])
	except:
		return 'Arguments error'

	global_data['lock'].acquire()

	launch = None
	for l in global_data['launches']:
		if l['stamp'] == stamp:
			launch = l
			break

	#if not launch:
		#global_data['lock'].release()
		#return 'Launch not found'

	try:
		global_data['db'].query('INSERT INTO subs (stamp, user_id) VALUES ("%d", "%d")' % (stamp, user_id))
	except:
		global_data['lock'].release()
		return 'Same subscription is already added'

	global_data['lock'].release()

	return 'The subscription %d is added' % stamp

def cmd(bot, update):
	line = update.message.text.strip()

	log('CMD (%s %s, id=%d): %s' % (update.message.from_user.first_name,
									update.message.from_user.last_name,
									update.message.from_user.id,
									line))

	line = line.split()

	cmd = line[0]

	chat_id = update.message.chat_id

	if cmd.startswith('/sched'):
		text = sched(line)
	elif cmd.startswith('/subscribe'):
		text = subscribe(line, update)
	else:
		text = 'Unknown command'

	bot.sendMessage(chat_id, text=text, parse_mode='HTML')

def loop():
	global global_data

	bot = Bot(token=token)

	while True:
		global_data['lock'].acquire()
		if global_data['finish']:
			break

		t = time.time()
		if t - global_data['last_check'] > 60:
			global_data['last_check'] = t
			items = global_data['db'].select('subs', where='stamp <= %d' % (get_stamp(time.gmtime()) + 30))

			for it in items:
				bot.sendMessage(it.user_id, text='ALERT %d' % it.stamp)
				global_data['db'].delete('subs', where='stamp=%d AND user_id=%d' % (it.stamp, it.user_id))

		t = time.time()
		if t - global_data['last_update'] > 60*60:
			global_data['last_update'] = t

			data = spaceflight.get_data()
			if data:
				log('UPDATING: %d records' % len(data))

				global_data['launches'] = data
				stamps = []
				for launch in data:
					if launch['stamp']:
						stamps.append(str(launch['stamp']))

				stamps = ','.join(stamps)

				items = global_data['db'].select('subs', where='stamp NOT IN (%s)' % stamps)
				for it in items:
					bot.sendMessage(it.user_id, text='The subscription %d was changed or removed. Check schedule and resubscribe.' % it.stamp)
					global_data['db'].delete('subs', where='stamp=%d AND user_id=%d' % (it.stamp, it.user_id))


		global_data['lock'].release()

		time.sleep(5)

log('=== START ===')

thr = threading.Thread(target=loop)
thr.start()

updater = Updater(token)

updater.dispatcher.add_handler(MessageHandler([Filters.command], cmd))

updater.start_polling()
updater.idle()

global_data['lock'].acquire()
global_data['finish'] = True
global_data['lock'].release()

thr.join()

log('=== FINISH ===')

