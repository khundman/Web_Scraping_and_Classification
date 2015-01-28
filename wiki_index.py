from whoosh.index import create_in
from whoosh.fields import * 
from whoosh.query import *
from whoosh.qparser import QueryParser
from whoosh import highlight
import csv
import re
import os.path
import glob, os, chardet
import sys

csv.field_size_limit(sys.maxsize) #extend field limit for csv (html was too long)

#initialize schema
schema = Schema(capitals=TEXT(stored=True), country= TEXT(stored=True), continent=TEXT(stored=True), capitalsHTML=TEXT(stored=True), countriesHTML=TEXT(stored=True))

#create index directory
if not os.path.exists("/Users/kh/desktop/Text/Assignment5/index"):
    os.mkdir("/Users/kh/desktop/Text/Assignment5/index")
ix = create_in("/Users/kh/desktop/Text/Assignment5/index", schema)

# Open file and write indices

with open("/Users/kh/desktop/Text/Assignment5/scrape_results.csv", newline='') as csvfile:
	scrape_reader = csv.reader(csvfile, delimiter= ',')
	writer = ix.writer()
	for a in scrape_reader:
		# print('Country: ' + str(a[1]))
		# print('Capitals: ' + str(a[2]))
		# print('Continent: ' + str(a[3]))
		# print('CapitalsHTML: ' + str(a[4]))
		writer.add_document(country = str(a[1]), capitals = str(a[2]), continent = str(a[3]), capitalsHTML = str(a[4]), countriesHTML = str(a[5]))
	writer.commit()

print(str(ix.doc_count()))


