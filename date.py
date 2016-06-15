# -*- coding: utf-8 -*-


import time, re


months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']


def parse_date(date):
	date = date.strip().lower()
	mon = day = None
	try:
		mon = months.index(date[:3]) + 1
		day = int(re.search('([0-9]+)', date).group())
		return mon, day
	except:
		pass
	return None, None

def mh(s):
	s = s.strip()
	if len(s) != 4:
		return None
	if not s.isdigit():
		return None
	return '%02d:%02d' % (int(s[:2]), int(s[2:]))

def parse_time(timestr):
	tm = timestr.strip().split()
	tm1 = None
	if 'GMT' in tm:
		ind = tm.index('GMT')
		if ind > 0:
			tm = tm[ind - 1]
			tm = tm.split('-')

			tm1 = tm2 = mh(tm[0])

			if len(tm) == 2:
				tm2 = mh(tm[1])
			return tm1, tm2

	return None, None

def get_stamp(stamp):
	return int(time.strftime('%Y%m%d%H%M', stamp))




