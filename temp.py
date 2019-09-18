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
search.raise_for_status()


results = search.json()


totalHits = results['totalHits']

photos = results['hits']

print(f'total results for {term} are {totalHits}')

total = 0

for i in range(1,totalHits/len(photos)):
    print(f'[INFO] making request for {i}th page from the search query ...')
    params = {'key': API_KEY, 'q': term, 'per_page': 200, 'image_type': 'photo', 'page': i}
    search = requests.get(URL, params = params)
    search.raise_for_status()
    
    results = search.json()
    print(f'Saving images for the {i}th page')
    
    for im in results['hits']:
        try:
            print(f"Fetching {im['webformatURL']}")
            r = requests.get(im['webformatURL'], timeout=30)
            
            ext = im['webformatURL']im['webformatURL'].rfind("."):]
            p = 
        
