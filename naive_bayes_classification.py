from whoosh.index import *
import whoosh.index as index
from whoosh.fields import * 
from whoosh.query import *
from whoosh.qparser import QueryParser
from whoosh import highlight
from whoosh import query
# from whoosh.span import *
from whoosh import qparser
import csv
import re
import os.path
import glob, os, chardet
import sys
import nltk
from collections import Counter
from nltk.corpus import stopwords
from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests #need an http client for use with beautifulsoup, which only parses raw html text
import lxml

#Open existing index
ix = index.open_dir("/Users/kh/desktop/Text/Assignment5/index")

#Get vocab
reader = ix.reader()
searcher = ix.searcher()
too_many_words = reader.all_terms() #generator
vocab =[]
delete = re.compile('[^\w\s]+')
delete2 = re.compile('[0-9]+')
delete3 = re.compile(' [A-Za-z][A-Za-z] ')
delete4 = re.compile(' [A-Za-z] ')


for word in too_many_words:
	# print(str(word))
	if word[0] == 'capitalsHTML':
		word = str(word[1])
		word = word[2:-1] #trim off whoosh bs
		cleaned = delete.sub('', word)
		if len(cleaned) > 2:
			vocab.append(cleaned)

vocab_length = len(vocab) #83796 for all

# N (number of documents)
num_docs = searcher.doc_count_all() #195

#Classes
classes = ['Africa', 'Asia', 'Europe', 'North America', 'South America', 'Oceania']

# Break up classes (continents)
#-------------------------------

topTerms = []
topTerms_wordOnly = []
for ind_class in classes:
	searcher = ix.searcher()
	parser = QueryParser("continent", schema=ix.schema)
	query = parser.parse(ind_class)
	text = ''

	#Get all words from class
	with ix.searcher() as searcher:
		results = searcher.search(query, limit=None)
		# print('Result count: ' + str(len(results)))
		for result in results:
			text += str(result['capitalsHTML'])

	#cleanup
	text = delete.sub('', text)
	text = delete2.sub('', text)
	text = delete3.sub('', text)
	text = delete4.sub('', text)
	words = nltk.word_tokenize(text)
	words = [item.lower() for item in words]
	pattern = re.compile(r'\b(' + r'|'.join(stopwords.words('english')) + r')\b\s*')
	words = [(pattern.sub('', word)) for word in words]

	#Get word counts from class
	counts = Counter(words)
	word_count = len(counts) #24676 for Europe
	# print(str(word_count))
	# print(counts)

	# print(counts.most_common(30))
	values = {}

	for pair in counts.items():
		value = (pair[1]+1)/(word_count + vocab_length)
		values[pair[0]] = value
		# print(str(pair[0]) + '  ' + str(value))

	values = Counter(values)
	counter = 0
	for word in values.most_common(30):
		pair = []
		# print(str(counter) + '  ' + str(word[0]))
		# print(str(counter) + '  ' + str(word[0]) + "  " +str(word[1]))
		counter += 1
		if counter>1:
			pair.append(word[0])
			pair.append(ind_class)
			topTerms.append(pair)
			topTerms_wordOnly.append(word[0])

# print(str(topTerms))

uniqueTopTerms = []
for word, count in Counter(topTerms_wordOnly).most_common():
	if count == 1:
		uniqueTopTerms.append(word)
# print(str(uniqueTopTerms))
# print(str(len(uniqueTopTerms)))

uniqueWithContinent = []
for word in uniqueTopTerms:
	for lst in topTerms:
		if word == lst[0]:
			uniqueWithContinent.append((word,lst[1]))
print(str(uniqueWithContinent))
print(str(len(uniqueWithContinent)))

train = uniqueWithContinent
cl = NaiveBayesClassifier(train)

# Grab capitals, continents and HTML from index
# -------------------
capitals = []
from whoosh.index import open_dir
ix = open_dir("/Users/kh/desktop/Text/Assignment5/index")
results = ix.searcher().search(Every('capitals'), limit=None)
for result in results:
	capitals.append((str(result['capitalsHTML']),str(result['continent'])))

# y_test = []
# y_pred = []	
# for capital in capitals:
# 	y_test.append(str(capital[1]))
# 	y_pred.append(str(cl.classify(capital[0])))
# 	# print('Capital: '  + str(capital[1]))
# 	# print('Result: ' + str(cl.classify(capital[0])))

# Build confusion matrix
# -----------------------
# labels = ['North America', 'South America', 'Europe', 'Africa', 'Asia', 'Oceania']
# cm = confusion_matrix(y_test,y_pred, labels)
# print(cm)
# fig = plt.figure()
# ax = fig.add_subplot(111)
# cax = ax.matshow(cm)
# plt.title('Confusion Matrix')
# plt.colorbar(cax)
# ax.set_xticklabels([''] + labels)
# ax.set_yticklabels([''] + labels)
# plt.ylabel('True label')
# plt.xlabel('Predicted label')
# plt.show()

#FAVORITE CITY
#--------------------------------------------
#Grab only visible text
def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element)):
        return False
    return True


#Bring down HTML for Tangier
r = requests.get("http://en.wikipedia.org/wiki/Tangier")
data = r.text
soup = BeautifulSoup(data)
text = soup.findAll(text=True) #grab text from HTML
visible_text = filter(visible,text)
# print(str(cl.classify(visible_text)))

# cl.show_informative_features(7)
#Europe
# Most Informative Features
#          contains(tunis) = False          Europe : Africa =      1.1 : 1.0
#          contains(delhi) = False          Europe : Asia   =      1.1 : 1.0
#         contains(french) = False          Europe : Africa =      1.1 : 1.0
#         contains(manila) = False          Europe : Asia   =      1.1 : 1.0
#       contains(gaborone) = False          Europe : Africa =      1.1 : 1.0
#          contains(cairo) = False          Europe : Africa =      1.1 : 1.0
#          contains(sudan) = False          Europe : Africa =      1.1 : 1.0

#.24% accuracy

# prob_dist = cl.prob_classify(visible_text)
# print(str('Africa: ') + str(round(prob_dist.prob('Africa'),2)))
# print(str('Europe: ') + str(round(prob_dist.prob('Europe'),2)))
# print(str('Oceania: ') + str(round(prob_dist.prob('Oceania'),2)))
# print(str('Asia: ') + str(round(prob_dist.prob('Asia'),2)))
# print(str('North America: ') + str(round(prob_dist.prob('North America'),2)))
# print(str('South America: ') + str(round(prob_dist.prob('South America'),2)))

# Africa: 0.1
# Europe: 0.22
# Oceania: 0.22
# Asia: 0.1
# North America: 0.18
# South America: 0.18
