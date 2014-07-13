#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
sys.path.append("/Users/casy/Dropbox (RN&IA'N)/Projects/Kats/Afisha/2014_07_05_Flight/google_flights_scraping/misc")

from flight import flightInDetails
# from Misc import DateCombination
import Misc
# print 'another try'
# TRIP = flightInDetails("https://www.google.com/flights/#search;f=DME,VKO,SVO;t=OKC;d=2014-07-20;r=2014-08-22;sel=SVOCDG0AF1845-CDGMSP0DL170-MSPOKC0DL4840", close=True)


# for f in TRIP['flightBacks']:
# 	print '|'.join([f['cost'], TRIP['flightTO']['moves'][0]['date'], f['moves'][0]['date']])

for x in DateCombination('2014.08.06', '2014.08.18', dom2=2, S=5):
	print x