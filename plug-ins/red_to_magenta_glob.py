#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gimpfu import *
import glob
import os

def red_to_magenta(infile, save_path):
    img = pdb.gimp_file_load(infile, '')
    red = pdb.gimp_channel_new_from_component(img, RED_CHANNEL, 'red')
    img.add_channel(red)
    pdb.gimp_edit_copy(red)

    pdb.gimp_image_set_component_active(img, RED_CHANNEL, False)
    pdb.gimp_image_set_component_active(img, GREEN_CHANNEL, False)
    pdb.gimp_image_set_component_active(img, BLUE_CHANNEL, True)

    lyr = pdb.gimp_edit_paste(img.layers[0], True)
    pdb.gimp_floating_sel_anchor(lyr)
    img.remove_channel(red)
    filename = os.path.basename(infile)
    outfile = os.path.join(save_path, filename)
    pdb.gimp_file_save(img, img.layers[0], outfile, outfile)

def red_to_magenta_glob(in_path, save_path):
    print 'Reading from:', in_path, 'and writing to:', save_path
    for infile in glob.glob(in_path):
        red_to_magenta(infile, save_path)
        print 'converted {}...'.format(infile)
    

register(
    'python-fu-red-to-magenta-glob',  # name
    'Change red to magenta for colorblind people.',  # blurb
    'red_to_magenta(in_path, save_path) -> in_path should be a glob directive',  # help
    'Tanya Schlusser',  # author
    'public domain',  # copyright
    '2015',  # date
    '_Red to magenta glob...',  # menu_path
    '',
    [
     (PF_STRING, "in-path", "Path for input file", ''),
     (PF_DIRNAME, "save-path", "Path for output filename", os.getcwd()),
    ],  # type
    [],  # params
    red_to_magenta_glob,  # ret_vals
    menu="<Toolbox>/My-Python-Fu/"
    )


main()
