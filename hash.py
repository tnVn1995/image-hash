from imutils import paths
import argparse
import time
import sys
import cv2
import os
import shutil
import numpy
import distance

ag = argparse.ArgumentParser()
ap.add_argument("-a", "--imgpath", required=True,
                help="dataset of images to create hash")
ap.add_argument("-c", "--copypath", required=True,
                help = "path to copy images to")
args = vars(ap.parse_args())

def dhash(image, hashSize=8):
    image = cv2.imread(image)
    # Skip image if None
    if image is None:
        continue
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
1st_hash = dhash(os.path.join(args['imgpath'],list_imgs[0]))
img_w_has[list_imgs[0]] = 1st_hash
# Create an ampty array to store hash value
hash = np.array([])
np.append(hash, 1st_hash)
# Copy first image in a copypath directory
print(f'[INFO] copy 1st image in to {args['copypath']}...')
copy_path = args['copypath']
shutil.copy(os.path.join(args['imgpath'], list_imgs[0]), copy_path)
# Itereate over the list of images in imgpath
for p in list_imgs[1:]:
    img_path = os.path.join(args['imgpath'],p)
    print(f'[INFO] Calculate hash value for {img_path}...')
    im_hash = dhash(img_path)
    print(f'[INFO] check for duplicates...')
    
