# -*- coding: utf-8 -*-

import re
import sys
import json

try:
	titles_basics_file = open("../../Datasets/IMDB/title.basics.tsv", "r")
	titles_per_length_file = open("../../Filtering/IMDB/title_length.csv", "w+")
	types_per_frequency_file = open("../../Filtering/IMDB/types_per_frequency.csv", "w+")
	words_per_frequency_file = open("../../Filtering/IMDB/words_per_frequency.csv", "w+")
	genres_per_frequency_file = open("../../Filtering/IMDB/genres_per_frequency.csv", "w+")
	titles_per_year_file = open("../../Filtering/IMDB/titles_per_year.csv", "w+")
except IOError as e:
	print "Could not open file -> ", e
	sys.exit()

#### Parsing ####
print "Parsing...\n"

first_line = True
titles = list()
types = set()
years = set()
genres = set()
title_type = dict()
title_year = dict()
title_length = dict()
title_genres = dict()

re_line = re.compile("(.*)\t(.+)\t(.+)\t(.*)\t(.*)\t(.+)\t(.*)\t(.+)\t(.+)")

for line in titles_basics_file:
	if first_line:
		first_line = False
	elif re_line.match(line):
		if re_line.search(line).group(2) != "tvEpisode":
			type = re_line.search(line).group(2)
			title = re_line.search(line).group(3)
			year = re_line.search(line).group(6)
			length = re_line.search(line).group(8)
			genre = re_line.search(line).group(9)

			titles.append(title)
			types.add(type)
			years.add(year)
			
			if genre != "\\N":
				for elem in genre.split(","):
					genres.add(elem)
			else:
				genres.add("unknown")

			title_type[title] = type
			
			if year != "\\N":
				title_year[title] = year
			else:
				title_year[title] = "unknown"

			if length != "\\N":
				title_length[title] = length
			else:
				title_length[title] = ""
			
			if genre != "\\N":	
				title_genres[title] = genre.split(",")
			else:
				title_genres[title] = ["unknown"]

titles_basics_file.close()

#### Filtering ####
print "Filtering\n"

## Titles length ##
print "Titles length\n"

# json.dump(title_length, titles_per_length_file, indent = 4)

titles_per_length_file.write("Title,Length (in minutes)\n")

for key in title_length:
	if title_length[key] != "":
		titles_per_length_file.write(str(key) + "," + str(title_length[key]) + "\n")

titles_per_length_file.close()

## Types per frequency ##
print "Types per frequency\n"

types_per_frequency = dict()

for elem in types:
	types_per_frequency[elem] = 0

for elem in title_type:
	types_per_frequency[title_type[elem]] += 1

# json.dump(types_per_frequency, types_per_frequency_file, indent = 4)

types_per_frequency_file.write("Genre,Num_films\n")

for key in types_per_frequency:
	types_per_frequency_file.write(str(key) + "," + str(types_per_frequency[key]) + "\n")

types_per_frequency_file.close()

## Words per frequency ##
print "Words per frequency\n"

words_per_frequency = dict()

for single_title in titles:
	for word in single_title.split():
		words_per_frequency[word.lower()] = 0

for single_title in titles:
	for word in single_title.split():
		words_per_frequency[word.lower()] += 1

# json.dump(words_per_frequency, words_per_frequency_file, indent = 4)

words_per_frequency_file.write("Word,Num_ocurrences\n")

for key in words_per_frequency:
	if words_per_frequency[key] > 4000:
		words_per_frequency_file.write(str(key) + "," + str(words_per_frequency[key]) + "\n")

words_per_frequency_file.close()

## Genres per frequency ##
print "Genres per frequency\n"

genres_per_frequency = dict()

for elem in genres:
	genres_per_frequency[elem] = 0

for elem in title_genres:
	for genre in title_genres[elem]:
		genres_per_frequency[genre] += 1

# json.dump(genres_per_frequency, genres_per_frequency_file, indent = 4)

genres_per_frequency_file.write("Genre,Num_films\n")

for key in genres_per_frequency:
	genres_per_frequency_file.write(str(key) + "," + str(genres_per_frequency[key]) + "\n")

genres_per_frequency_file.close()

## Titles year ##
print "Titles year\n"

titles_per_year = dict()

for elem in years:
	if elem != "\\N":
		titles_per_year[elem] = 0

titles_per_year["unknown"] = 0

for elem in title_year:
	if elem != "\\N":
		titles_per_year[title_year[elem]] += 1

# json.dump(titles_per_year, titles_per_year_file, indent = 4)

titles_per_year_file.write("Year,Num_films\n")

for key in titles_per_year:
	titles_per_year_file.write(str(key) + "," + str(titles_per_year[key]) + "\n")

titles_per_year_file.close()