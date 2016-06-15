#!/usr/bin/env python
# -*- coding: utf-8 -*-


from settings import *
import web



def show_log():
	db = web.database(dbn='mysql', db=db_name, user=db_user, pw=db_pass)

	with db.transaction():
		logs = db.query('SELECT * FROM log')

	for log in logs:
		stamp = log['stamp'].strftime('%Y-%m-%d %H:%M:%S')
		log = log['log']
		print '[%s] %s' % (stamp, log)



if __name__ == '__main__':
	show_log()



