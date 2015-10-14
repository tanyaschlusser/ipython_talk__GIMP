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
face_cascade = cv2.CascadeClassifier(face_tree)


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


def hat(img, hatfile):
    gimp.context_push()
    img.undo_group_start()
    lyr = img.layers[0]
    if not lyr.is_rgb:
        pdb.gimp_image_convert_rgb(img)
    
    pr = lyr.get_pixel_rgn(0, 0, img.width, img.height)
    hat_lyr = pdb.gimp_file_load_layer(img, hatfile)
    pdb.gimp_image_insert_layer(img, hat_lyr, None, -1)
    pdb.plug_in_colortoalpha(img, hat_lyr, (255,255,255))
    
    shape = (pr.h, pr.w, pr.bpp)
    gray = np.reshape(np.fromstring(pr[:,:], dtype=np.uint8), shape)
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    faces = detect(gray, face_cascade)
    
    for x1, y1, x2, y2 in faces:
        face_ht = y2-y1
        brow_ht = face_ht / 4
        w = x2 - x1
        h = (hat_lyr.height * w) / hat_lyr.width
        newhat = pdb.gimp_layer_copy(hat_lyr, False)
        pdb.gimp_image_insert_layer(img, newhat, None, -1)
        pdb.gimp_item_transform_scale(newhat, x1, max(y1+brow_ht-h,0), x1+w, y1+brow_ht)
        #pdb.gimp_layer_scale(newhat, x1, h-y1, x1+w, y1)
        #pdb.gimp_layer_resize(newhat, w, h, -x1, h-y1)
        
    pdb.gimp_image_remove_layer(img, hat_lyr)
    img.undo_group_end()
    gimp.context_pop()
    

register(
    'python-fu-hat',  # name
    'Put a hat on every person.',  # blurb
    'hat(img, hatfile) -> a hat on every person',  # help
    'Tanya Schlusser',  # author
    'public domain',  # copyright
    '2015',  # date
    '_Hat...',  # menu_path
    '*',  # image_types
    [
     (PF_IMAGE, 'img', 'Input image', None),
     (PF_FILE, 'hatfile', 'Hat image', None)
    ],  # type
    [],  # params
    hat,  # ret_vals
    menu="<Image>/Filters/Artistic/"
    )


main()
