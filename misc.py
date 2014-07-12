#!/usr/local/bin/python
# -*- coding: utf-8 -*-

def dateParse(text):
	from datetime import date
	y = date.today().year
	mDict = {'янв.':1,
			'фев.':2,
			'марта':3,
			'апр.':4,
			'мая':5,
			'июня':6,
			'июля':7,
			'авг.':8,
			'сен.':9,
			'окт.':10,
			'ноя.':11,
			'дек.':12,
			}

	for key in mDict.keys():
		if key in text:
			mm = mDict[key]
	day = int(text.split(' ')[1])
	return '.'.join([str(y), str(mm), str(day)])
