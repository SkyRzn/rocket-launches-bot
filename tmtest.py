#!/usr/bin/env python
# -*- coding: utf-8 -*-


from settings import *
import web, telegram


def time2str(time):
	h, m = str(time).split(':')[:2]
	return '%02d:%02d' % (int(h), int(m))

def sched_data(db):
	launches = db.select('launches')

	res = []
	res_full = []
	for launch in launches:
		date = '%s %s' % (launch.datestr, launch.date.strftime('%Y'))
		if launch.precdate:
			date = launch.date.strftime('%d %b %Y')

		time = launch.timestr

		if launch.time1:
			time = time2str(launch.time1)
			if launch.time2 and launch.time1 != launch.time2:
				time = '%s - %s' % (time, time2str(launch.time2))
		dt = '%s, %s' % (date, time)
		res.append('*** %s ***\n%s' % (dt, launch.mission))
		res_full.append('*** %s ***\n%s\n%s' % (dt, launch.mission, launch.descr))

	return '\n'.join(res),


def tm():
	bot = telegram.Bot(token=token)

	db = web.database(dbn='mysql', db=db_name, user=db_user, pw=db_pass)
	data = sched_data(db)
	#bot.sendMessage(883104, text=data)


	bot.sendMessage(883104, text='aaa /subscribe?1234', parse_mode='HTML')

if __name__ == '__main__':
	tm()
	#test()



