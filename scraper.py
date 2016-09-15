#!/usr/bin/env python

import csv
import re
from urlparse import urlsplit

import requests
import scraperwiki

'''This "scraper" just changes the columns in the YourNextMP elected
candidates data from the UK 2015 general election'''

url = 'https://candidates.democracyclub.org.uk/media/candidates-elected-2015.csv'

r = requests.get(url, stream=True)

for row in csv.DictReader(r.raw):
    parlparse_person_id = re.sub(r'^.*/(\d+)$', r'\1', row['parlparse_id'])
    wikiname = ''
    if row['wikipedia_url']:
        split = urlsplit(row['wikipedia_url'])
        wikiname = split.path[len('/wiki/'):]
        wikiname = wikiname.replace('_', ' ')
    scraperwiki.sqlite.save(
        unique_keys=['id'],
        data={
            'id': parlparse_person_id,
            'name': row['name'],
            'twitter': row['twitter_username'],
            'facebook': row['facebook_page_url'],
            'wikipedia': row['wikipedia_url'],
            'wikiname': wikiname,
            'birth_date': row['birth_date'],
            'linkedin': row['linkedin_url'],
            'image': row['image_url'],
        }
    )
