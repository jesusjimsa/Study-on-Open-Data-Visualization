# -*- coding: utf-8 -*-

import re
import sys
import json

try:
	gutenberg_file = open("../../Datasets/Gutenberg/GUTINDEX.ALL.txt", "r")
	books_per_language_file = open("../../Filtering/Gutenberg/books_per_language.csv", "w+")
	books_cronological_file = open("../../Filtering/Gutenberg/books_cronological.json", "w+")
	books_per_author_file = open("../../Filtering/Gutenberg/books_per_author.csv", "w+")
	words_per_frequency_file = open("../../Filtering/Gutenberg/words_per_frequency.csv", "w+")
	biographical_vs_nonbiog_file = open("../../Filtering/Gutenberg/biographical_vs_nonbiog.json", "w+")
except IOError:
	print "Could not open file"
	sys.exit()

##### Parsing #####

first_line = True
books = list()
authors = dict()
book_code = dict()
languages = list()

re_book_author = re.compile("(.+)(, by |, por |, mennessä |, door |, di )(.+)(  *)([0-9]+)")
re_book_language = re.compile("(.*\[Language: )([a-zA-Z]+)( ?\].*)")

for line in gutenberg_file:
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

gutenberg_file.close()

##### Filtering #####

## Books per language ##
books_per_language = dict()

for elem in set(languages):
	books_per_language[elem] = 0

for elem in languages:
	books_per_language[elem] += 1

# The Language of the eBooks is English, unless otherwise noted
books_per_language["English"] = len(books) - len(languages)

books_per_language_file.write("Language,Num_books\n")

for key in books_per_language:
	books_per_language_file.write(str(key) + "," + str(books_per_language[key]) + "\n")

# json.dump(books_per_language, books_per_language_file, indent = 4)

books_per_language_file.close()

## Cronological ##
json.dump(book_code, books_cronological_file, indent = 4)

books_cronological_file.close()

## Books per author ##
books_per_author = dict()

for elem in authors:
	books_per_author[authors[elem]] = 0

for elem in authors:
	books_per_author[authors[elem]] += 1

# json.dump(books_per_author, books_per_author_file, indent = 4)
books_per_author_file.write("Author,Num_books\n")

for key in books_per_author:
	# We will ignore authors with less than ten books
	if int(books_per_author[key]) > 80 and key != "Various":
		books_per_author_file.write(str(key) + "," + str(books_per_author[key]) + "\n")

books_per_author_file.close()

## Word ordered by frequency in titles ##
words_per_frequency = dict()

for single_book in books:
	for word in single_book.split():
		if word[-1] == ',':
			word = word[0:len(word) - 1]

		words_per_frequency[word.lower()] = 0

for single_book in books:
	for word in single_book.split():
		if word[-1] == ',':
			word = word[0:len(word) - 1]

		words_per_frequency[word.lower()] += 1

# json.dump(words_per_frequency, words_per_frequency_file, indent = 4)
words_per_frequency_file.write("Word,Frequency\n")

for key in words_per_frequency:
	# We will ignore words with less than five hundred ocurrences
	if int(words_per_frequency[key]) > 500:
		words_per_frequency_file.write(str(key) + "," + str(words_per_frequency[key]) + "\n")

words_per_frequency_file.close()

## Biographical vs non-biographical ##
biographical_vs_nonbiog = dict()

biographical_vs_nonbiog["biographical"] = 0
biographical_vs_nonbiog["non_biographical"] = 0

for single_book in books:
	for word in single_book.split():
		if word.lower() == "biography" or word.lower() == "autobiography" or word.lower() == "biographical" or word.lower() == "autobiographical":
			biographical_vs_nonbiog["biographical"] += 1
		else:
			biographical_vs_nonbiog["non_biographical"] += 1

json.dump(biographical_vs_nonbiog, biographical_vs_nonbiog_file, indent = 4)

biographical_vs_nonbiog_file.close()