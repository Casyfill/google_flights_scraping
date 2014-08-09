

JsonDict = {}

for row in csv:
	a = {'region':, 'ICAO':, 'IATA':, 'name': }
	if location in JsonDict.keys():
		JsonDict[location].append(a)
	else:
		JsonDict[location]= [a]


