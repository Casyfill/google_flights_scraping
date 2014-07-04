from selenium import webdriver
import time
import lxml.html
# Scraping googleFlight site

# toDO: 
#  * url-constructor
#  * click_for_more


def flightRequest():
	
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

	# Making Url

	baseUrl = "https://www.google.com/flights/#search"
	home = "DME,VKO,SVO"
	to = "OKC"
	Departure = "2014-08-12"
	Return = "2014-09-23"
	maxStops = 1
	return ';'.join([baseUrl, 'f='+home, 't='+to, 'd='+ ','.join(list(Departure)), 'r=' + ','.join(list(Return)), 's=' +str(maxStops)])
	# url = 'https://www.google.com/flights/#search;f=DME,VKO,SVO;t=VVO;d=2014-07-20;r=2014-07-24'



ChromePath = r"/Users/casy/Dropbox (RN&IA'N)/Projects/Kats/Afisha/2014_07_05_Flight/chromedriver"
browser = webdriver.Chrome(executable_path=ChromePath)
url = 'https://www.google.com/flights/#search;f=DME,VKO,SVO;t=OKC;d=2014-07-20;r=2014-07-24'

browser.get(url)
time.sleep(2.5)
html = browser.page_source
browser.quit()

# PARSING
dom = lxml.html.fromstring(html)
flights = dom.cssselect('a[elm="il"]:only-child')
print len(flights)

def parseCard (f):
	# first (cost and type)
	card =  f.cssselect('a > div')
	first = card[0].cssselect('div[elm="p"]>div')
	cost = first[0].text
	Type = first[1].text
	
	# second (dates, company)
	second = card[1]
	dates = second.cssselect('div>span')
	start = dates[0].get('tooltip')
	end = dates[1].get('tooltip')
	company = second.cssselect('div')[-1].text
	
	# third (airports, time)
	third = card[2]
	fTime = third.cssselect('div>div')[0].text
	airports = third.cssselect('div>div')[1].text

	# fourth (stops)
	fourth = card[3]
	stops = fourth.cssselect('div>div')[0].text

	return { 'cost':cost, 'type':Type, 'start':start, 'end':end, 'company':company,'FlightTime':fTime, 'airports':airports, 'stops':stops}

for f in flights:
	print parseCard(f)

