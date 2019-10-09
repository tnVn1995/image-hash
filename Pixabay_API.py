# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 16:12:33 2019

@author: tnguy
"""

# -*- coding: utf-8 -*-
"""
This script searches images using API from Pixabay 
with the query input
"""

from requests import exceptions
import argparse
import requests
import cv2
import os
import math

"""
Construct argument parser and parse the arguments
"""

ap = argparse.ArgumentParser()
ap.add_argument("-q", "--query", required=True,
	help="search query to search Bing Image API for")
ap.add_argument("-o", "--output", required=True,
	help="path to output directory of images")
args = vars(ap.parse_args())


"""
Define key words
"""
API_KEY = '13570746-6c4abd4d2437c7d64baac7be0'
term = args['query']
URL = 'https://pixabay.com/api/'

params = {'key': API_KEY, 'q': term, 'per_page': 200, 'image_type': 'photo'}

search = requests.get(URL, params = params)
search.raise_for_status()


results = search.json()


totalHits = results['totalHits']

photos = results['hits']

print(f"total results for {args['query']} are {totalHits}")

total = 0

for i in range(1,math.ceil(totalHits/len(photos))+1):
    print(f'[INFO] making request for {i}th page from the search query ...')
    params = {'key': API_KEY, 'q': args['query'], 'per_page': 200, 'image_type': 'photo', 'page': i}
    search = requests.get(URL, params = params)
    search.raise_for_status()
    
    results = search.json()
    print(f'Saving images for the {i}th page')
    
    for im in results['hits']:
        try:
            print(f"Fetching {im['webformatURL']}")
            r = requests.get(im['webformatURL'], timeout=30)
            
            ext = im['webformatURL'][im['webformatURL'].rfind("."):]
            p = os.path.join(args['output'], f'{str(total).zfill(8)}{ext}')
            
            with open(p, 'wb')  as f:
                f.write(r.content)
                f.close()
                
        except Exception as e:
            print('Error', e)
            continue
        
        
        image = cv2.imread(p)
        
        
        if image is None:
            print(f'[INFO] deleting: {p}')
            os.remove(p)
            continue
        
        total +=1
print('The number of images downlaoded is:', total)          
            
        
