#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gimpfu import *
import os


import sys
sys.path.extend([
    '//anaconda/envs/with_opencv/lib/python27.zip',
    '//anaconda/envs/with_opencv/lib/python2.7',
    '//anaconda/envs/with_opencv/lib/python2.7/plat-darwin',
    '//anaconda/envs/with_opencv/lib/python2.7/plat-mac',
    '//anaconda/envs/with_opencv/lib/python2.7/plat-mac/lib-scriptpackages',
    '//anaconda/envs/with_opencv/lib/python2.7/lib-tk',
    '//anaconda/envs/with_opencv/lib/python2.7/lib-old',
    '//anaconda/envs/with_opencv/lib/python2.7/lib-dynload',
    '//anaconda/envs/with_opencv/lib/python2.7/site-packages',
    '//anaconda/envs/with_opencv/lib/python2.7/site-packages/setuptools-18.3.2-py2.7.egg'
])
import numpy as np
import cv2


base = '/Users/tanyaschlusser/Code/git/ipython/ipython_talk__GIMP'
haarcascades = cv2.__file__.split('lib')[0] + 'share/OpenCV/haarcascades/'
face_tree =  haarcascades + "haarcascade_frontalface_alt.xml"
mouth_tree =  haarcascades + "haarcascade_smile.xml"
face_cascade = cv2.CascadeClassifier(face_tree)
mouth_cascade = cv2.CascadeClassifier(mouth_tree)


def detect(gray, cascade, minSize=(20,20)):
    rects = cascade.detectMultiScale(
            gray,
            scaleFactor=1.05,
            minNeighbors=4,
            minSize=minSize,
            flags = cv2.CASCADE_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects


def stache(img, stachefile):
    gimp.context_push()
    img.undo_group_start()
    lyr = img.layers[0]
    if not lyr.is_rgb:
        pdb.gimp_image_convert_rgb(img)
    
    pr = lyr.get_pixel_rgn(0, 0, img.width, img.height)
    stache_lyr = pdb.gimp_file_load_layer(img, stachefile)
    pdb.gimp_image_insert_layer(img, stache_lyr, None, -1)
    pdb.plug_in_colortoalpha(img, stache_lyr, (255,255,255))
    
    shape = (pr.h, pr.w, pr.bpp)
    gray = np.reshape(np.fromstring(pr[:,:], dtype=np.uint8), shape)
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    faces = detect(gray, face_cascade)
    for x1, y1, x2, y2 in faces:
        w = int((x2 - x1) * .8)
        h = (stache_lyr.height * w) / stache_lyr.width
        face = gray[y1:y2, x1:x2]
        mouths = detect(face, mouth_cascade, minSize=(2,2))
        if len(mouths) > 0:
            mx1, mx2, my1, my2 = mouths[0]
            # assume it's the firt one
            stache_top = max(0, y1 + my1 - h/2)
            stache_left = max(0, x1 + (mx2 + mx1)/2 - w/2)
        else:
            stache_top = max(0, (y1 + y2) / 2 - .1 * h)
            stache_left = max(0, x1 + (x2 - x1) * .1)
        newstache = pdb.gimp_layer_copy(stache_lyr, False)
        pdb.gimp_image_insert_layer(img, newstache, None, -1)
        pdb.gimp_item_transform_scale(
                newstache,
                stache_left, stache_top,
                stache_left+w, stache_top + h)
        
    pdb.gimp_image_remove_layer(img, stache_lyr)
    img.undo_group_end()
    gimp.context_pop()
    

register(
    'python-fu-stache',  # name
    'Put a mustache on every person.',  # blurb
    'stache(img, stachefile) -> a mustache on every person',  # help
    'Tanya Schlusser',  # author
    'public domain',  # copyright
    '2015',  # date
    '_Stache...',  # menu_path
    '*',  # image_types
    [
     (PF_IMAGE, 'img', 'Input image', None),
     (PF_FILE, 'stachefile', 'Mustache image', None)
    ],  # type
    [],  # return values
    stache,  # function call
    menu="<Image>/Filters/Artistic/"
    )

main()
