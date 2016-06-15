#!/usr/bin/env python
# -*- coding: utf-8 -*-


from settings import *
import web


def create_db():
	db = web.database(dbn='mysql', db=db_name, user=db_user, pw=db_pass)

	with db.transaction():
		try:
			db.query('DROP TABLE subs;')
		except:
			pass
		db.query('CREATE TABLE subs (stamp BIGINT NOT NULL, user_id INT NOT NULL, UNIQUE INDEX(stamp, user_id));')

		try:
			db.query('DROP TABLE log;')
		except:
			pass
		db.query('CREATE TABLE log (id INT NOT NULL AUTO_INCREMENT, stamp TIMESTAMP, log TEXT, PRIMARY KEY(id));')


if __name__ == '__main__':
	create_db()
