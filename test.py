#!/usr/bin/env python
# -*- coding: utf-8 -*-


from settings import *
import web, time
from date import get_stamp


def test():
	db = web.database(dbn='mysql', db=db_name, user=db_user, pw=db_pass)

	subscribes = db.select('subs', where='stamp <= %d;' % (get_stamp(time.gmtime()) + 300000))
	for subscribe in subscribes:
		print subscribe.stamp




if __name__ == '__main__':
	test()



