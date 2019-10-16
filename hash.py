# from imutils import paths
import argparse
import time
import sys
import cv2
import os
import shutil
import numpy as np
import distance

ap = argparse.ArgumentParser()
ap.add_argument("-a", "--imgpath", required=True,
                help="dataset of images to create hash")
ap.add_argument("-c", "--copypath", required=True,
                help = "path to copy images to")
args = vars(ap.parse_args())
if os.path.exists(args['copypath']) == False:
    os.mkdir(args['copypath'])
print(args['imgpath'], args['copypath'])
def get_key(dictionary,val):
    return list(dictionary.keys())[list(dictionary.values()).index(val)]

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
# Get the list of images from imgpath
list_imgs = os.listdir(args['imgpath'])
# Create a dictionary to store image name with its corresponding hash value
img_w_has = {}
# Store the first img has in img_w_has
st_hash = dhash(os.path.join(args['imgpath'],list_imgs[0]))
print(st_hash)
img_w_has[list_imgs[0]] = st_hash
# Create an ampty array to store hash value
hashes = []
hashes.append(st_hash)
# Copy first image in a copypath directory
print(f'[INFO] copy 1st image in to {args["copypath"]}...')
print(hashes)
copy_path = args['copypath']
shutil.copy(os.path.join(args['imgpath'], list_imgs[0]), copy_path)
#Create a duplicate dictionary
duplicate = {}
# Itereate over the list of images in imgpath
for p in list_imgs[1:]:
    img_path = os.path.join(args['imgpath'],p)
    print(f'[INFO] Calculate hash value for {img_path}...')
    im_hash = dhash(img_path)
    print(f'[INFO] check for duplicates...')
    for hash in hashes:
        try:
            if hammingDistance(im_hash, hash) <= 10:
                key = get_key(img_w_has,hash)
                print(f'[INFO] found one duplicate for {key}...')
                print('[INFO] Leave the duplicate in the old directory...')
                print('[INFO] store duplicates')
                duplicates[key] = []
                duplicates[key].append(p)
            else:
                print(f'[INFO] moving image to new directory...')
                print(f'[INFO] store hash values in database')
                shutil.copy(img_path, copy_path)
                img_w_has[p] = im_hash
                np.append(hashes, im_hash)
        except Exception as e:
            print(e)
