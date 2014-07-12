from selenium import webdriver
import time
import lxml.html

ChromePath = r"/Users/casy/Dropbox (RN&IA'N)/Projects/Kats/Afisha/2014_07_05_Flight/chromedriver"
browser = webdriver.Chrome(executable_path=ChromePath)


# Scraping googleFlight site

# def TODO():
	# toDO: 
	#  * click_for_more
	# getFlightLink
	# flightDetails
	# dateList maker - сделать нормальный генератор дат, с проверкой нахлеста


From = ['DME', 'VKO', 'SVO'] #Moscow
To = ['OKC'] #Oklahoma-City
DateStart = '2014-08-06'
DateEnd = '2014-08-15'

StartDomain = 1
EndDomain = 1




def recordFlight(From, To, departure, Return, maxStops=1 ):

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

	def parseCard (f):

		
		# first (cost and type)
		link = f.get('href')
		flightDetails(link)
		# print link
		card =  f.cssselect('a > div')
		# first = card[0].cssselect('div[elm="p"]>div')
		# cost = first[0].text #.replace(' $','').replace(' ','')
		# # print cost
		# # cost= int(cost)
		# Type = first[1].text
	
		# # second (dates, company)
		# second = card[1]
		# dates = second.cssselect('div>span')
		# start = dates[0].get('tooltip')
		# end = dates[1].get('tooltip')
		# company = second.cssselect('div')[-1].text
		
		# # third (airports, time)
		# third = card[2]
		# fTime = third.cssselect('div>div')[0].text
		# airports = third.cssselect('div>div')[1].text

		# # fourth (stops)
		# fourth = card[3]
		# stops = fourth.cssselect('div>div')[0].text

		


		# return { 'link':link, 'cost':cost, 'type':Type, 'start':start, 'end':end, 'company':company,'FlightTime':fTime, 'airports':airports, 'stops':stops}

	# STARTING BROUSER EMULATIONG
	ChromePath = r"/Users/casy/Dropbox (RN&IA'N)/Projects/Kats/Afisha/2014_07_05_Flight/chromedriver"
	browser = webdriver.Chrome(executable_path=ChromePath)
	url = 'https://www.google.com/flights/#search;f=DME,VKO,SVO;t=OKC;d=2014-07-20;r=2014-07-24'
	# url = flightRequest(From,To,departure,Return, maxStops)

	browser.get(url)
	time.sleep(3)
	html = browser.page_source
	

	# PARSING
	dom = lxml.html.fromstring(html)
	flights = dom.cssselect('a[elm="il"]:only-child')
	browser.close()
	return [parseCard(f) for f in flights]







# ПЕРЕБОР ДАТ
# FIXME - сделать нормальный перебор дат
def DataList(DateStart, StartDomain, DateEnd, EndDomain):
	dates = {}
	for sd in xrange(StartDomain):
 
		st = str(int(DateStart.split('-')[2])+sd)
		if len(st)<2:
			st = '0'+st
		start = '-'.join(DateStart.split('-')[:2]  +[st])
		dates[start]=[]

		for ed in xrange(EndDomain):
			zeroEnd = int(DateEnd.split('-')[2])
			et = str(int(DateEnd.split('-')[2])+ed)
			if len(st)<2:
				et = '0'+et
			dates[start].append('-'.join(DateEnd.split('-')[:2] +[et]))

	return dates

print 'start parsing ', StartDomain*EndDomain, ' urls!'
	


# globalTable = []
dates = DataList(DateStart, StartDomain, DateEnd, EndDomain)


# PRINTIN TABLE
for start in dates:
	for end in dates[start]:
		print start, '--->', end, ' scraping'
		table = recordFlight(From, To, start, end, maxStops =3)
# 		for card in table:
# 			print '|'.join([start, end] + [card[key] for key in card.keys()])
# 		time.sleep(5)

		# globalTable+=table

# for card in globalTable:
# 	print '|'.join([card[key] for key in card.keys()])