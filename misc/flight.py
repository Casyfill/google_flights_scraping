#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
sys.path.append("/Users/casy/Dropbox (RN&IA'N)/Projects/Kats/Afisha/2014_07_05_Flight/google_flights_scraping/misc")

from selenium import webdriver
import lxml.html
import time
# from datetime import date

# MYSCRIPTS
from Misc import dateParse

# STARTING BROWSER
ChromePath = r"/Users/casy/Dropbox (RN&IA'N)/Projects/Kats/Afisha/2014_07_05_Flight/chromedriver"
browser = webdriver.Chrome(executable_path=ChromePath)

# def TODO():
	# toDO: 
	#  * click_for_more
	# getFlightLink
	# flightDetails
	# dateList maker - сделать нормальный генератор дат, с проверкой нахлеста


# gives back a trip dictionary for any major flight combination in url
def flightInDetails(l, close=False):
	# подробности одного полета туда со всеми вариантами возвращения в указанный день
	
	global browser
	browser.get(l)
	time.sleep(3)
	htmlstring = browser.page_source
	dDom = lxml.html.fromstring(htmlstring)
	
	trip = {}

	def flightStory(flight):
		# ВОЗМОЖНО, НУЖНО ВЫВЕСТИ ДАТЫ ЗА СКОБКИ ОТДЕЛЬНЫХ ЭЛЕМЕНТОВ

		cards = flight.cssselect('div[class=GHFBRF-DKJC]')
		# print len(cards)
		story = {}
		story['moves'] = []
		for element in cards:
			# ДАТЫ
			el= {}
			if len(element.cssselect('div [class=GHFBRF-DPJC]>div'))>0:
				el['date'] = dateParse(element.cssselect('div [class=GHFBRF-DPJC]>div')[0].text.encode('utf-8'))
			# Полет
			if len(element.cssselect('div[class=GHFBRF-DLJC]'))>0:
				el['type']='flight'

				el['flightStart'] = '–'.join([x.text for x in element.cssselect('div [class=GHFBRF-DLJC]>div[class=GHFBRF-DGMC]')[0].cssselect('span')])
				el['airports']= element.cssselect('div[class=GHFBRF-DLJC]>div[class=GHFBRF-DLLC]')[0].text
				
				el['fCompany'] = element.cssselect('div[class=GHFBRF-DLJC]>div[class=GHFBRF-DKIC]')[0].text.encode('utf-8')
				if '·' in el['fCompany']:
					el['plane'] = el['fCompany'].split('·')[1].strip()
					el['fCompany'] = el['fCompany'].split('·')[0].strip()
				else: el['plane'] = 'unknown'
				# dur =[int(x) for x in element.cssselect('div [class=GHFBRF-DMJC]>div')[0].text#.encode('utf-8').replace('мин.','').strip().split(' ч. ')]
				el['duration'] = element.cssselect('div [class=GHFBRF-DMJC]>div')[0].text  #dur[0] + dur[1]/60
				
			else: # транзит
				el['type'] = 'transit'
				el['place'] = element.cssselect('div [class=GHFBRF-DNJC]')[0].text.encode('utf-8').replace('Пересадка:','').strip()
				el['duration'] = element.cssselect('div [class=GHFBRF-DGJC]')[0].text
			story['moves'].append(el)
		return story
	
	trip['flightTO'] =  flightStory(dDom.cssselect('div[class=GHFBRF-DEPC]')[0])

	flightsOutLinks = [x.get('href') for x in dDom.cssselect('div[class=GHFBRF-DFOC] a[elm="il"]:only-child')]

	trip['flightBacks'] = []
	for link in flightsOutLinks:
		browser.get(link)
		time.sleep(3)
		htmlstring = browser.page_source
		dDom = lxml.html.fromstring(htmlstring)
		flightBack = flightStory(dDom.cssselect('div[class=GHFBRF-DEPC]')[1])
		flightBack['cost'] = dDom.cssselect('span[class=GHFBRF-DKIB]')[0].text.encode('utf-8').replace('$','').replace(' ','')
		flightBack['link'] = link
		trip['flightBacks'].append(flightBack)
	
	# print 'trip scraped: 1 TO and %d OUT' % (len(trip['flightBacks']))
	return trip

	if close:
		browser.close()





