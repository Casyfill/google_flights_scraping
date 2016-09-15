google_flights_scraping
=======================

Scraping googleFlight site for visualisation purposes only
(from https://www.google.com/flights/#search)


### UPD: 2016_09_15, version 0.2.1
- clean and expressive code, FlightCollector class
- removed shameful daterange. will write normal one, if needed
- test search


### TODO: 
 - [x] url-constructor
 - [ ] click_for_more (for now gets first N (8)) loaded by default
 - [ ] deep card Parsed, if required
 - [ ] data cleaner as a separate function
 - [ ] cronetab sketch
 - [ ] more search parameters

### Dependencies

- lxml
- selenium
- [chromedriver](http://chromedriver.storage.googleapis.com/index.html), [DOCS](http://code.google.com/p/selenium/wiki/ChromeDriver)
