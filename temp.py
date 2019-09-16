# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests 
API_KEY = '13570746-6c4abd4d2437c7d64baac7be0'
term = 'sad+face'
URL = 'https://pixabay.com/api/'

params = {'key': API_KEY, 'q': term, 'per_page': 200, 'image_type': 'photo'}

search = requests.get(URL, params = params)

results = search.json()

results.keys()

totalHits = results['totalHits']

photos = results['hits']

print(f'total results for {term} are {totalHits}')

total = 0

