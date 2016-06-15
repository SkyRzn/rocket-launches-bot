# -*- coding: utf-8 -*-


import sys


sec_dir = '/home/sky/rocket-bot/sensitive_data'


if sec_dir not in sys.path:
	sys.path.append(sec_dir)


import priv


db_name = priv.db_name
db_user = priv.db_user
db_pass = priv.db_pass
token = priv.token

