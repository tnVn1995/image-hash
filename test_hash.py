# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 13:42:22 2019

@author: ngu09790
"""

import time
import sys
import cv2
import os
import shutil
import numpy as np
import distance

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
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(image, (hashSize + 1, hashSize))

    # compute the (relative) horizontal gradient between adjacent
    # column pixels
    diff = resized[:, 1:] > resized[:, :-1]

    # convert the difference image to a hash
    return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])

def get_key(dictionary,val):
    return list(dictionary.keys())[list(dictionary.values()).index(val)]

list_imgs = os.listdir('C:\Users\ngu09790\OneDrive - Texas Tech University\Dimitri_class\dataset\dataset\anger')

img_w_has = {}