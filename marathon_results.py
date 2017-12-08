#!/usr/bin/env python
from __future__ import print_function
import sys
reload(sys)
sys.setdefaultencoding('utf-8') # handle difficult character encodings

import urllib2
from bs4 import BeautifulSoup
import re

def scrape(name, year):
    races_dir = 'http://canoeracing.org.uk/marathon/results/'

    if year >= 2016:
        races_year = 'results'+str(year)+'.html'
    elif year < 2008 or year > 2017:
        print('Sorry - can\'t do years outside of 2008-2017')
        return []
    else:
        races_year = 'Results'+str(year)+'.html'

    page = urllib2.urlopen(races_dir+races_year)
    soup = BeautifulSoup(page, 'html.parser')

    # scrape the index page to get a list of links to race results
    races = []
    for atag in soup.find_all('a'):
        # skip results stored as PDF or Word documents
        if re.match(r'.*\.pdf.*', str(atag)) == None and re.match(r'.*\.doc.*', str(atag)) == None:
            races.append(atag.get('href'))
#   races = [races[1]] # 2017/Thameside1 for debug

    race_count = len(races)
    results = []

    # iterarate over all races searching for the name within a row
    rx_name = re.compile(r'.*'+name+'.*', re.I)
    for race in races:
        # progress indicator
        count_down = '{:2}...\r'.format(race_count)
        print(count_down, end='')
        race_count -= 1
        sys.stdout.flush()

        try:
            page = urllib2.urlopen(str(races_dir+race))
        except:
            print('\nIgnoring broken link: {}'.format(str(races_dir+race)))

        soup = BeautifulSoup(page, 'html.parser')
        rows = soup.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            for col in cols:
                if rx_name.match(col.text):
                    for br in row.find_all('br'): # crew boats: replace line break between crew members
                        br.replace_with('/')
                    this_row = row.find_all('td')

                    if len(this_row) >= 8: # sometimes the source data isn't perfect
                        race_position = this_row[0].text
                        race_name     = this_row[1].text
                        race_club     = this_row[2].text
                        race_class    = this_row[3].text
                        race_div      = this_row[4].text
                        race_time     = this_row[5].text
                        #race_points  = this_row[6].text
                        race_promoted = this_row[7].text

                        # strip htm[l], undersores, year etc from file name to get event name
                        race_event = re.compile(r'.htm.*').sub('', str(race))
                        race_event = re.compile(r'_').sub(' ', race_event)
                        race_event = re.compile(r'/').sub('', race_event)
                        race_event = re.compile(str(year)).sub('', race_event)
                        # use title() to capitalize each word
                        results.append((race_event.title(), race_position, race_name.title(), race_club, race_class, race_div, race_time, race_promoted))

    # get the indentation right here - return after completed loop
    print('       ') # obliterate countdown droppings
    return results

if __name__ == '__main__':

    name = sys.argv[1]
    year = int(sys.argv[2])
    results = scrape(name, year)

    # scan through all results looking for the longest strings
    event_max = 5
    name_max = 5
    division_max = 8
    for result in results:
        if len(result[0]) > event_max:
            event_max = len(result[0])
        if len(result[2]) > name_max:
            name_max = len(result[2])
        if len(result[5]) > division_max:
            division_max = len(result[5])

    result_format = '{:4} {:'+str(event_max)+'} {:5} {:'+str(name_max)+'} {:7} {:5} {:'+str(division_max)+'} {:8} {}'
    #result_format = '{:4} {:15} {:5} {:40} {:7} {:5} {:8} {:8} {}'

    if results:
        print(result_format.format('YEAR', 'RACE', 'PLACE', 'NAME', 'CLUB', 'CLASS', 'DIVISION', 'TIME', 'PROMOTED'))
    else:
        print('No results for {}'.format(year))

    for result in results:
        print(result_format.format(year, *result))
