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
r = requests.get("http://http://en.wikipedia.org/wiki/Tangier")
data = r.text
soup = BeautifulSoup(data)
text = soup.findAll(text=True) #grab text from HTML
visible_texts = filter(visible,text)
