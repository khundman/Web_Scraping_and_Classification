from bs4 import BeautifulSoup
import requests #need an http client for use with beautifulsoup, which only parses raw html text
import lxml
import whoosh
import pandas
import re

#Grab only visible text
def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element)):
        return False
    return True

#Bring down HTML
r = requests.get("http://en.wikipedia.org/wiki/List_of_countries_and_capitals_with_currency_and_language")
data = r.text
soup = BeautifulSoup(data)

# find this HTML tag pattern for COUNTRIES - tr,td,b,a 
# Not grabbing bold and/or italic countries (not really countries)
# Continent is equal to 'Caption' tag (only 7 of these)
# --------------------------------------------
count = 0
countries = []
continents = []
countryHTML = []

for table in soup.find_all('table'):
	for caption in table.find_all('caption'):
		continent = caption.string
	for tr in table.find_all('tr'):
		for td in tr.find_all('td', recursive = False):
			for b in td.find_all('b', recursive = False): 
				# print(b)
				for a in b.find_all('a', recursive = False):
					countries.append(str(a.string))
					continents.append(str(continent))
					# print(a.string)
					count += 1
					#grab country's page
					r = requests.get('http://en.wikipedia.org' + a['href'])
					data = r.text
					soupHTML = BeautifulSoup(data)
					texts = soupHTML.findAll(text=True) #grab text from HTML
					visible_texts = filter(visible,texts) #grab only text that is visible on page
					content = ""
					for text in visible_texts: #filter returns iterator object
						content = content + text #just make one long string
					clean = ' '.join(content.split()) #remove extra whitespace
					countryHTML.append(clean)
# print('COUNT: ' + str(count))

# find this pattern for CAPITAL CITIES - tr,td,a - where the country is in the countries list
# Only grab the first capital listed
# -------------------------------------------------------
count = 0
all_capitals = []
all_cityHTML = []
for tr in soup.find_all('tr'):
	capitals = []
	cityHTML = []
	counter = 0
	for td in tr.find_all('td', recursive = False):
		for b in td.find_all('b', recursive = False):
			for a in b.find_all('a', recursive = False):
				if a.string in countries:
					get_capital = True #only get capital(s) if you grabbed the country
				else:
					get_capital = False
				if get_capital == True:
					for td in tr.find_all('td', recursive = False):
						counter += 1
						only_first = 0 
						no_doubles = 0
						if counter == 3:
							for a in td.find_all('a', recursive = False):
								if only_first < 1:	
									only_first += 1	
									count += 1
									capitals.append(a.string)
									# grab the city's page
									r = requests.get('http://en.wikipedia.org' + a['href'])
									data = r.text
									soupHTML = BeautifulSoup(data)
									texts = soupHTML.findAll(text=True) #grab text from HTML
									visible_texts = filter(visible,texts) #grab only text that is visible on page
									content = ""
									for text in visible_texts: #filter returns iterator object
										content = content + text #just make one long string
									clean = ' '.join(content.split()) #remove extra whitespace
									cityHTML.append(clean)
								elif no_doubles == 0:
									for br in td.find_all('br', recursive = True):
										other = br.nextSibling
										other2 = other.nextSibling #second sibling is next capital
										print('Other Capital: ' + other2.string)
										capitals.append(other2.string)
										no_doubles += 1
										r = requests.get('http://en.wikipedia.org' + other2['href'])
										data = r.text
										soupHTML = BeautifulSoup(data)
										texts = soupHTML.findAll(text=True) #grab text from HTML
										visible_texts = filter(visible,texts) #grab only text that is visible on page
										content = ""
										for text in visible_texts: #filter returns iterator object
											content = content + text #just make one long string
										clean = ' '.join(content.split()) #remove extra whitespace
										cityHTML.append(clean)
							all_capitals.append(capitals)
							all_cityHTML.append(cityHTML)
							# print('Capitals: ' + str(capitals))
# print('COUNT: ' + str(count))

# Results
# j = 0
# while j < 194:
# 	print('Country: ' + str(countries[j]) + '   Capital: ' + str(all_capitals[j]) + '   Continent: ' + str(continents[j]))
# 	print('')
# 	# print('')
# 	# print(str(cityHTML[j]))
# 	j+=1

# print('Length Cap: ' + str(len(all_capitals)))
# print('Length Country: ' + str(len(countries)))
# print('Length Continents: ' + str(len(continents)))
# print('Length cityHTML: ' + str(len(all_cityHTML)))
# print('Length countryHTML: ' + str(len(countryHTML)))

docs = pandas.DataFrame()
docs['country'] = countries
docs['capital'] = all_capitals
docs['continent'] = continents
docs['cityHTML'] = all_cityHTML
docs['countryHTML'] = countryHTML

docs.to_csv('/Users/kh/desktop/text/assignment5/scrape_results.csv')

# Look into handling multiple capitals


