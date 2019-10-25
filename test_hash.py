# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 13:42:22 2019

@author: ngu09790
"""

import time

import cv2
import os
import shutil

#import matplotlib.pyplot as plt
from collections import defaultdict
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('-src', '--source', required=True,
                help='Directory to get images from')
ap.add_argument('-dest', '--destination', required=True,
                help='Directory to copy non-duplicated images to')
args = vars(ap.parse_args())
def hammingDistance(x, y):
    """
    :type x: int
    :type y: int
    :rtype: int
    """
    biX = bin(x)[2:]
    biY = bin(y)[2:]
    ll = max(len(biX),len(biY))
    sl = min(len(biX),len(biY))
    if len(biX)<=len(biY):
        biX = '0'*(ll-sl) + biX
    else:
        biY = '0'*(ll-sl) + biY
    n = 0
    for i in range(ll):
        if biX[i] != biY[i]:
            n += 1
    return n


def dhash(image, hashSize=8):
    image = cv2.imread(image)
    # Skip image if None
    if image is None:
        pass
    # resize the input image, adding a single column (width) so we
    # can compute the horizontal gradient
    try:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(image, (hashSize + 1, hashSize))
        # compute the (relative) horizontal gradient between adjacent
        # column pixels
        diff = resized[:, 1:] > resized[:, :-1]

        # convert the difference image to a hash
        return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])
    except Exception as e:
        print(e)


def get_key(dictionary,val):
    return list(dictionary.keys())[list(dictionary.values()).index(val)]
#%%

if __name__ == '__main__':
    start = time.time()
    file_path2 = args['source']
    copy_path = args['destination']
    print(file_path2, copy_path)
    if os.path.isdir(copy_path) == False:
        os.mkdir(copy_path)
    list_imgs1 = os.listdir(file_path2)
    img_w_has = {}
    # Store the first img has in img_w_has
    st_hash = dhash(os.path.join(file_path2,list_imgs1[0]))
    print('1st hash value is:',st_hash)
    img_w_has[list_imgs1[0]] = st_hash
    print('dict of hash values and corresponding picture:',img_w_has)
    # Create an ampty array to store hash value
    hashes = []
    hashes.append(st_hash)
    #im = cv2.imread(os.path.join(file_path2,list_imgs[0]))
    #plt.imshow(im)
    shutil.copy(os.path.join(file_path2,list_imgs1[0]), copy_path)
    assert list_imgs1[0] in os.listdir(copy_path), "Error! not in there"
    """Let's test moving images"""
    count = 0
    duplicate = defaultdict(list)
    for p in list_imgs1[1:]:
        im_path = os.path.join(file_path2, p)
        im_hash = dhash(im_path)
        print(f'{p}\'s hash value is:', im_hash)
        for hash in hashes:
            if hammingDistance(im_hash, hash) <= 10:
                key = get_key(img_w_has, hash)
                duplicate[key].append(p)
            else:
                print('No Duplicates')
                print(f'[INFO] store hash values in database')
                print(f'INFO] move {im_path} to {copy_path}')
                img_w_has[p] = im_hash
#                print(f'[INFO] the dict hash value now is {img_w_has}')
                if im_hash not in hashes:
                    hashes.append(im_hash)
#                print('List of hash value is',hashes)
        for key, val in duplicate.items():
            shutil.copy(os.path.join(file_path2, val[0]), copy_path)
            if len(val) >= 2:
                print('[INFO] duplicates are:', val)
    end = time.time()
    print(f'[INFO] it takes {(end-start)/60} minutes to complete exxecution' )
