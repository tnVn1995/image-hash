# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 19:10:16 2019

@author: tnguy
"""

import urllib3
import threading

urllib3.disable_warnings()

def download_url(file_name, url):
    print(f'Downloading the contents of {url} into {file_name} in thread {threading.current_thread().name}')
    
    http = urllib3.PoolManager()
    
    response = http.request(method = 'GET', url=url)
    
    with open(file_name, 'wb') as f:
        f.write(response.data)
    
    print(f'Download of {url} done. \n')


test_dict = {
        'Google': 'http://www.google.com',
        'Python': 'http://www.google.com',
        'Yahoo': 'http://www.yahoo.com',
        'Bing':'http://www.google.com'
        }    


threads = []

print('Main thread starting execution ...')
for key in test_dict:
    thread = threading.Thread(target=download_url, name=key, args=(key, test_dict[key]))
    threads.append(thread)
    thread.start()
    
print('Main thread continuing execution...')
for thread in threads:
    thread.join()
    
print('Main thread exiting.')
    
    
    