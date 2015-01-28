from whoosh.index import *
import whoosh.index as index
from whoosh.fields import * 
from whoosh.query import *
from whoosh.qparser import QueryParser
from whoosh import highlight
from whoosh import query
# from whoosh.span import *
from whoosh import qparser

# See what's in index
# -------------------
# from whoosh.index import open_dir
# ix = open_dir("/Users/kh/desktop/Text/Assignment5/index")
# for x in ix.searcher().documents():
# 	print(str(x))

#Open existing index
ix = index.open_dir("/Users/kh/desktop/Text/Assignment5/index")

# CapitalHTMLs that contain 'Greek' and 'Roman', but not 'Persian' using Boolean Query
#------------------------------------------------------------------------------------
searcher = ix.searcher()
parser = QueryParser("capitalsHTML", schema=ix.schema)
query = parser.parse(u"Greek AND Roman NOT Persian")

with ix.searcher() as searcher:
	results = searcher.search(query, limit=None)
	print('Result count: ' + str(len(results)))
	for result in results:
		print(str(result['capitqals']))

# Result count: 25
# ['Tripoli']
# ['Tunis']
# ['Sofia']
# ['Lisbon']
# ['Nicosia']
# ['Monaco']
# ['Skopje']
# ['Cairo']
# ['Ljubljana']
# ['Bucharest']
# ['Podgorica']
# ['Montevideo']
# ['Algiers']
# ['Bangui']
# ['Bern']
# ['Budapest']
# ['Bratislava']
# ['Berlin']
# ['Amsterdam']
# ['Madrid']
# ['Warsaw']
# ['Havana']
# ['Copenhagen']
# ['Buenos Aires']
# ['Abidjan'] 			#this is the 2nd capital listed


#Shakespeare references - Edit distance of 15 (max from class examples)
#-----------------------------------------------------------------------
searcher = ix.searcher()
parser = QueryParser("capitalsHTML", schema=ix.schema, termclass=FuzzyTerm)

with ix.searcher() as searcher:
	results = searcher.search(FuzzyTerm("capitalsHTML", "shakespeare", maxdist=4, prefixlength=2), limit=None)
	# print('Result count: ' + str(len(results)))
	# for result in results:
	# 	print(str(result['capitals']))
	# 	print(str(result.highlights("capitalsHTML")))
		
# Result count: 4
# ['London']
# ['Prague']
# ['Cairo']
# ['Washington, D.C.']


# 'located below sea level' -> Phrase Query with slop factor of 10
#------------------------------------------------------------------
searcher = ix.searcher()
# parser = qparser.QueryParser("capitalsHTML", schema=ix.schema)
# parser.remove_plugin_class(qparser.PhrasePlugin)
# parser.add_plugin(qparser.SequencePlugin())
# # myquery = parser.parse("located below sea level~10")
# myquery = Phrase("capitalHTML",["located","below","sea","level"],slop=10)

with ix.searcher() as searcher:
	results = searcher.search(Phrase("capitalsHTML",['located','below','sea','level'],slop=10),limit=None)
	print('Result count: ' + str(len(results)))
	count = 0
	for result in results:
		count += 1
		print(str(count) + '  ' + str(result['capitals']))
		# print(str(result.highlights("capitalsHTML")))

# Result count: 1
# ['Baku'] #NOT SURE ABOUT THIS ONE

