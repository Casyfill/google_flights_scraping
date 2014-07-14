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
	def clean(d):
		if '/' in d or '.' in d:
			return	d.replace('/','-').replace('.','-')
		else:
			return d

	d1= datetime.datetime.strptime(clean(d1), "%Y-%m-%d")
	d2= datetime.datetime.strptime(clean(d2), "%Y-%m-%d")

	dateList1 = [d1 + datetime.timedelta(days=x) for x in range(0, dom1+1)]
	dateList2 = [d2 + datetime.timedelta(days=x) for x in range(0, dom2+1)]

	trigger = False
	for date1 in dateList1:
		for date2 in dateList2:
			if date2>(date1+datetime.timedelta(days=(S+1))):
				yield (date1.strftime('%Y-%m-%d') , date2.strftime('%Y-%m-%d'))
				trigger = True
	if trigger == False:
		print 'Sorry, something bad with dates you choosed'

def cleanCost(txt):
	NC = ''
	for char in txt:
		if char in ['1','2','3','4','5','6','7','8','9','0']:
			NC+=char

	return int(NC)


def parseDuration(txt):
	from datetime import timedelta
	array = txt.replace(' мин.','').split(' ч. ')
	return timedelta(hours=int(array[0]), minutes=int(array[1]))

def parseDateTime(txt):
	from datetime import datetime
	monthdict={ 'января' :1,
				'февраля':2,
				'марта'  :3,
				'апреля' :4,
				'мая'    :5,
				'июня'   :6,
				'июля'   :7,
				'августа':8,
				'сентября':9,
				'октября':10,
				'ноября' :11,
				'декабря':12,}
	
	
	txt = txt.split(', ')[1].replace(' г. в','').split(' ')
	txt[1] = str(monthdict[txt[1]])
	return  datetime.strptime( '|'.join(txt), "%d|%m|%Y|%H:%M")
	

# print parseDateTime('среда, 6 августа 2014 г. в 09:45')
