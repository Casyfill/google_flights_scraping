from selenium import webdriver
# from datetime import date
from Misc import dateParse
# import misc
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


# def dateParse(text):
# 	y = date.today().year
# 	mDict = {'янв.':1,
# 			'фев.':2,
# 			'марта':3,
# 			'апр.':4,
# 			'мая':5,
# 			'июня':6,
# 			'июля':7,
# 			'авг.':8,
# 			'сен.':9,
# 			'окт.':10,
# 			'ноя.':11,
# 			'дек.':12,
# 			}

	# for key in mDict.keys():
	# 	if key in text:
	# 		mm = mDict[key]
	# day = int(text.split(' ')[1])
	# return '.'.join([str(y), str(mm), str(day)])


# gives back a trip dictionary for any major flight combination in url
def flightInDetails(l):
	
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
		trip['flightBacks'].append(flightBack)
	
	print 'trip scraped: 1 TO and %d OUT' % (len(trip['flightBacks']))
	return trip



print 'another try'
TRIP = flightInDetails("https://www.google.com/flights/#search;f=DME,VKO,SVO;t=OKC;d=2014-07-20;r=2014-08-22;sel=SVOCDG0AF1845-CDGMSP0DL170-MSPOKC0DL4840")
browser.close()

for f in TRIP['flightBacks']:
	print '|'.join([f['cost'], TRIP['flightTO']['moves'][0]['date'], f['moves'][0]['date']])




