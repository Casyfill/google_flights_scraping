#!/usr/bin/env python
#-*- coding: utf-8 -*-

from selenium import webdriver
import lxml.html
import time

import sys
sys.path.append("/Users/casy/Dropbox (RN&IA'N)/Projects/Kats/Afisha/2014_07_05_Flight/google_flights_scraping/misc")
from Misc import dateParse, cleanCost,parseDuration, parseDateTime

# STARTING BROUSER EMULATIONG
ChromePath = r"/Users/casy/Dropbox (RN&IA'N)/Projects/Kats/Afisha/2014_07_05_Flight/chromedriver"
browser = webdriver.Chrome(executable_path=ChromePath)



# gives back a trip dictionary for any major flight combination in url
def recordFlight(From, To, departure, Return, maxStops=1, back=False ):

	

	def flightRequest(From, To, departure, Return, maxStops=1):
			
		# documentation
		# http://www.google.com/flights/#search | The website URL
		# f=ORD,MDW,MKE | Origin Airport(s) (from)
		# t=WAS | Destination Airport(s) (to)
		# d=2011-11-14 | Departure Date (depart)
		# r=2011-11-17 | Return Date (return)
		# a=AA,CO,WN,UA | Air Carrier(s)(airline)
		# c=DFW,IAH | Connection Cities (connect)
		# s=1 | Maximum Stops (stops)
		# olt=0,900 | Outbound Landing Time Range – Min-Max in minutes from 0:00 (outbound landing – arrival time range)
		# itt=840,1440 | Inbound Takeoff Time Range – Min-Max in minutes from 0:00 (inbound takeoff – departure time range)
		# tt=o/m   |one-way/multyway
		
		# Making Url
		baseUrl = "https://www.google.com/flights/#search"
		home = 'f=' + ','.join(From) # "DME,VKO,SVO"
		to = 't=' + ','.join(To)
		# print ';'.join([baseUrl, home, to, 'd='+ departure, 'r=' + Return, 's=' +str(maxStops)])
		return ';'.join([baseUrl, home, to, 'd='+ departure, 'r=' + Return, 's=' +str(maxStops)])
		# url = 'https://www.google.com/flights/#search;f=DME,VKO,SVO;t=VVO;d=2014-07-20;r=2014-07-24'

	
	def parseCard (f, back=False):

		
		def flightInDetails(l, back=False):
			# подробности одного полета туда со всеми вариантами возвращения в указанный день
			

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
						el['airports']= element.cssselect('div[class=GHFBRF-DLJC]>div[class=GHFBRF-DLLC]')[0].text.encode('utf-8')
						
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
			if back:
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

		# PARSE FLIGHT CARD
		# first (cost and type)
		link = f.get('href')
		
		detailtree = True
		if detailtree:
			trip = flightInDetails(link)
		else:
			trip = None


		# print link
		card =  f.cssselect('a > div')
		first = card[0].cssselect('div[elm="p"]>div')
		cost = cleanCost(first[0].text) #.replace(' $','').replace(' ','')
		# print cost
		Type = first[1].text
		
		# second (dates, company)
		second = card[1]
		dates = second.cssselect('div>span')
		start = parseDateTime(dates[0].get('tooltip').encode('utf-8'))
		end = parseDateTime(dates[1].get('tooltip').encode('utf-8'))
		company = second.cssselect('div')[-1].text.encode('utf-8')
		
		# third (airports, time)
		third = card[2]
		fTime = parseDuration(third.cssselect('div>div')[0].text.encode('utf-8'))
		
		# AEROPORTS
		def parseAirports(List):
			return [ x  for x in list(set(' – '.join(List).split(' – ')))]

		if detailtree:
			airportsTotal = []
			for el in trip['flightTO']['moves']:
				if el['type']=='flight':
					airportsTotal.append(el['airports'])

			airports = '-'.join(parseAirports(airportsTotal))
		else:
			airports = third.cssselect('div>div')[1].text

		# fourth (stops)
		fourth = card[3]
		stops = fourth.cssselect('div>div')[0].text

		return { 'link':link, 'trip':trip, 'cost':cost, 'type':Type, 'start':start, 'end':end, 'company':company,'FlightTime':fTime, 'airports':airports, 'stops':stops}

	
	url = flightRequest(From,To,departure,Return, maxStops)

	browser.get(url)
	time.sleep(3)
	html = browser.page_source
	
	# PARSING
	dom = lxml.html.fromstring(html)
	flights = dom.cssselect('a[elm="il"]:only-child')
	# browser.close()

	print departure, '|', Return, '|', len(flights)
	return [parseCard(f,back) for f in flights]






