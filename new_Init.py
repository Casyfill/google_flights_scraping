#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
sys.path.append("/Users/casy/Dropbox (RN&IA'N)/Projects/Kats/Afisha/2014_07_05_Flight/google_flights_scraping/misc")

from flight import recordFlight
from Misc import DateCombination


# TODO
# save all as a spreadsheet


From = ['DME', 'VKO', 'SVO'] #Moscow
To = ['OKC'] #Oklahoma-City
DateStart = '2014-08-06'
DateEnd = '2014-08-14'

StartDomain = 0
EndDomain = 1
S = 2

maxStops = 4



# data = (recordFlight(From, To, x[0],x[1], maxStops=1 ) for x in DateCombination(DateStart, DateEnd, dom1=StartDomain, dom2=EndDomain, S=S))
data = []
for x in DateCombination(DateStart, DateEnd, dom1=StartDomain, dom2=EndDomain, S=S):
	table=recordFlight(From,To,x[0],x[1],maxStops, back=False)
	for card in table:
		print '|'.join([ card['start'].strftime("%Y.%m.%d %H:%M"), card['airports'],str(card['FlightTime'].seconds/3600), str(card['cost'])])
	
	# .strftime("%d.%m.%Y. %H:%M")
# browser.close()


