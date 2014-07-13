#!/usr/local/bin/python
# -*- coding: utf-8 -*-

def dateParse(text):
	# designed for "Воскресение, 13 авг." format
	text = str(text)
	from datetime import date
	y = date.today().year
	day = int(text.split(' ')[1])
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
			break
	
	return '.'.join([str(y), str(mm), str(day)])



def DateCombination(d1, d2, dom1=0, dom2=0, S=0):
	# ГЕНЕРАТОР КОРРЕКТНЫХ КОМБИНАЦИЙ ДАТ ДЛЯ ЗАПРОСА
	# d1, d2 - стартовые даты прилета и улета
	# dom1, dom2 - максимальный интервал соотв. дат вперед
	# S - минимальное количество дней в точке прилета (минимальная разница между полетом туда и обратно в днях)

	import datetime
	
	# cleaning
	def parsing(d):
		if '/' in d1 or '.' in d1:
			d.replace('/','-').replace('.','-')

		return datetime.datetime.strptime(d, "%Y-%m-%d")

	d1= datetime.datetime.strptime(d1, "%Y.%m.%d")
	d2= datetime.datetime.strptime(d2, "%Y.%m.%d")

	dateList1 = [d1 + datetime.timedelta(days=x) for x in range(0, dom1+1)]
	dateList2 = [d2 + datetime.timedelta(days=x) for x in range(0, dom2+1)]

	trigger = False
	for date1 in dateList1:
		for date2 in dateList2:
			if date2>(date1+datetime.timedelta(days=(S+1))):
				yield (date1.strftime('%Y-%m-%d') , date2.strftime('%Y-%m-%d'))
				trigger = True
	if trigger = False:
		print 'Sorry, something bad with dates you choosed'


for x in DateCombination('2014.08.06','2014.08.09', dom1=2,dom2=4,S=2):
	print x