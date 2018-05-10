# -*- coding: utf-8 -*-

import re
import sys

try:
	gutenberg = open("../../Datasets/Gutenberg/GUTINDEX.ALL.txt", "r")
	books_per_language_file = open("../../Filtering/Gutenberg/books_per_language.csv", "w+")
except IOError:
	print "Could not open file"
	sys.exit()

##### Parsing #####

first_line = True
by_languages = [", by", ", por", ", mennessä"]
books = list()
authors = dict()
book_code = dict()
languages = list()

re_book_author = re.compile("(.+)(, by |, por |, mennessä |, door )(.+)(  *)([0-9]+)")
re_book_language = re.compile("(.*\[Language: )([a-zA-Z]+)( ?\].*)")

for line in gutenberg:
	if first_line:
		first_line = False
	elif line[0] == "\n":
		1+1
	elif line[0] != ' ':
		if re_book_author.match(line):
			book_name = re_book_author.search(line).group(1)
			books.append(book_name)
			aux_author = re_book_author.search(line).group(3)
			
			i = len(aux_author)
			i -= 1
			
			while i > 0:
				if aux_author[i] == ' ':
					aux_author = aux_author[0:len(aux_author)-1]
					i -= 1
				else:
					i = -1

			authors[book_name] = aux_author
			book_code[book_name] = re_book_author.search(line).group(5)
	elif re_book_language.match(line):
		languages.append(re_book_language.search(line).group(2))

gutenberg.close()

##### Filtering #####

books_per_language = dict()

for elem in set(languages):
	books_per_language[elem] = 0

for elem in languages:
	books_per_language[elem] += 1

# The Language of the eBooks is English, unless otherwise noted
books_per_language["English"] = len(books) - len(languages)

books_per_language_file.write("Language, Times\n")

for elem in books_per_language:
	books_per_language_file.write(str(elem) + ", " + str(books_per_language[elem]) + "\n")

books_per_language_file.close()