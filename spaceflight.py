# -*- coding: utf-8 -*-


from date import parse_date, parse_time, get_stamp
import time
import lxml.html as html


url = 'http://spaceflightnow.com/launch-schedule/'


def rm_pref(s):
	s = s.split(':')
	if len(s) > 1:
		s.pop(0)
	res = ':'.join(s)
	return res.strip()


def get_data():
	page = html.parse(url)
	root = page.getroot()

	datenames = root.find_class('datename')
	missiondatas = root.find_class('missiondata')
	missdescrips = root.find_class('missdescrip')

	launches = zip(datenames, missiondatas, missdescrips)

	res = []

	curtime = time.gmtime()
	year = curyear = curtime.tm_year
	curmon = curtime.tm_mon
	prev_mon = -1

	for name, data, desc in launches:
		datestr = name.find_class('launchdate')[0].text.strip()
		mission = name.find_class('mission')[0].text.strip()
		desc = desc.text_content().strip()

		timestr, site = data.text_content().strip().split('\n')

		site = rm_pref(site)
		timestr = rm_pref(timestr)

		mon, day = parse_date(datestr)
		tm1, tm2 = parse_time(timestr)

		if mon > 0:
			if mon < prev_mon:
				year += 1
			elif mon < curmon - 2 and curyear == year:
				year = curyear + 1

			prev_mon = mon

		stamp = None
		if mon > 0 and day > 0:
			date = '%02d-%02d-%04d' % (day, mon, year)
			if tm1:
				dt = '%s %s' % (date, tm1)
				stamp = get_stamp(time.strptime(dt, '%d-%m-%Y %H:%M'))
		else:
			date = '%s %s' % (datestr, year)

		res.append({'tm1': tm1,
					'tm2': tm2,
					'timestr': timestr,
					'date': date,
					'stamp': stamp,
					'mission': mission,
					'site': site,
					'desc': desc})
	return res
