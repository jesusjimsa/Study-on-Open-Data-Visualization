# -*- coding: utf-8 -*-
#
# COLUMN pl_discmethod:  Discovery Method
# COLUMN pl_pnum:        Number of Planets in System
# COLUMN pl_orbper:      Orbital Period [days]
# COLUMN st_dist:        Distance [pc]
# COLUMN pl_name:        Planet Name
# COLUMN pl_facility:    Discovery Facility
#

# 9999999999999 means the field is empty in the file

import re
import sys
import json

try:
	exoplanets_file = open("../../Datasets/Exoplanets/planets.tsv", "r")
	method_per_frequency_file = open("../../Filtering/Exoplanets/method_per_frequency.json", "w+")
	system_size_file = open("../../Filtering/Exoplanets/system_size.json", "w+")
	discover_facility_file = open("../../Filtering/Exoplanets/discover_facility.json", "w+")
	ordered_distance_file = open("../../Filtering/Exoplanets/ordered_distance.json", "w+")
	orbital_period_file = open("../../Filtering/Exoplanets/orbital_period.json", "w+")
except IOError as e:
	print "Could not open file -> ", e
	sys.exit()

#### Parsing ####
first_line = True
pl_name = list()
pl_discmethod = dict()
pl_pnum = dict()
pl_orbper = dict()
st_dist = dict()
pl_facility = dict()

discmethods = set()
facilities = set()

re_line = re.compile("(.*)\t(.*)\t(.*)\t(.*)\t(.*)\t(.*)\t(.*)")

for line in exoplanets_file:
	if first_line:
		first_line = False
	elif re_line.match(line):
		name = re_line.search(line).group(6)
		discmethod = re_line.search(line).group(2)
		pnum = re_line.search(line).group(3)
		orbper = re_line.search(line).group(4)
		dist = re_line.search(line).group(5)
		facility = re_line.search(line).group(7)

		pl_name.append(name)
		discmethods.add(discmethod)
		facilities.add(facility)
		
		pl_discmethod[name] = discmethod
		pl_pnum[name] = pnum
		if orbper != "":
			pl_orbper[name] = float(orbper)
		else:
			pl_orbper[name] = 9999999999999
		st_dist[name] = dist
		pl_facility[name] = facility

exoplanets_file.close()

#### Filtering ####
## Discovery method per frequency ##
method_per_frequency = dict()

for elem in discmethods:
	method_per_frequency[elem] = 0

for elem in pl_discmethod:
	method_per_frequency[pl_discmethod[elem]] += 1

json.dump(method_per_frequency, method_per_frequency_file, indent = 4)

method_per_frequency_file.close()

## Number of planets frequency ##
system_size = dict()

for elem in pl_pnum:
	system_size[pl_pnum[elem]] = 0

for elem in pl_pnum:
	system_size[pl_pnum[elem]] += 1

json.dump(system_size, system_size_file, indent = 4)

system_size_file.close()

## Discover facility ##
discover_facility = dict()

for elem in pl_facility:
	discover_facility[elem] = pl_facility[elem]

json.dump(discover_facility, discover_facility_file, indent = 4)

discover_facility_file.close()

## Distance ##
ordered_distance = dict()
transition = list()

for elem in st_dist:
	if st_dist[elem] != "":
		transition.append([elem, float(st_dist[elem])])
	else:
		transition.append([elem, 9999999999999])

transition.sort(lambda x, y: cmp(y[1], x[1]))

for i in range(0, len(transition)):
	ordered_distance[transition[i][0]] = i + 1

json.dump(ordered_distance, ordered_distance_file, indent = 4)

ordered_distance_file.close()

## Orbital period ##
json.dump(pl_orbper, orbital_period_file, indent = 4)

orbital_period_file.close()