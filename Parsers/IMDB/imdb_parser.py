# -*- coding: utf-8 -*-

import re
import sys
import json

try:
	titles_basics_file = open("../../Datasets/IMDB/title.basics.tsv", "r")
	titles_per_length = open("../../Filtering/IMDB/title_length.json", "w+")
	types_per_frequency_file = open("../../Filtering/IMDB/types_per_frequency.json", "w+")
	words_per_frequency_file = open("../../Filtering/IMDB/words_per_frequency.json", "w+")
	genres_per_frequency_file = open("../../Filtering/IMDB/genres_per_frequency.json", "w+")
	titles_per_year_file = open("../../Filtering/IMDB/titles_per_year.json", "w+")
except IOError as e:
	print "Could not open file -> ", e
	sys.exit()

#### Parsing ####
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
				title_genres[title] = "unknown"

titles_basics_file.close()

#### Filtering ####
## Titles length ##
json.dump(title_length, titles_per_length, indent = 4)

titles_per_length.close()

## Types per frequency ##
types_per_frequency = dict()

for elem in types:
	types_per_frequency[elem] = 0

for elem in title_type:
	types_per_frequency[title_type[elem]] += 1

json.dump(types_per_frequency, types_per_frequency_file, indent = 4)

types_per_frequency_file.close()

## Words per frequency ##
words_per_frequency = dict()

for single_title in titles:
	for word in single_title.split():
		words_per_frequency[word] = 0

for single_title in titles:
	for word in single_title.split():
		words_per_frequency[word] += 1

json.dump(words_per_frequency, words_per_frequency_file, indent = 4)

words_per_frequency_file.close()

## Genres per frequency ##
genres_per_frequency = dict()

for elem in genres:
	genres_per_frequency[elem] = 0

for elem in title_genres:
	for genre in title_genres[elem]:
		genres_per_frequency[genre] += 1

json.dump(genres_per_frequency, genres_per_frequency_file, indent = 4)

genres_per_frequency_file.close()

## Title year ##
titles_per_year = dict()

for elem in years:
	titles_per_year[elem] = 0

for elem in title_year:
	titles_per_year[title_year[elem]] += 1

json.dump(titles_per_year, titles_per_year_file, indent = 4)

titles_per_year_file.close()