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
EndDomain = 6
S = 7

maxStops = 4



# data = (recordFlight(From, To, x[0],x[1], maxStops=1 ) for x in DateCombination(DateStart, DateEnd, dom1=StartDomain, dom2=EndDomain, S=S))
data = []
for x in DateCombination(DateStart, DateEnd, dom1=StartDomain, dom2=EndDomain, S=S):
	data.append(recordFlight(From,To,x[0],x[1],maxStops))
	

