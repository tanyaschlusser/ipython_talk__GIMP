#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gimpfu import *
import os

#def red_to_magenta(img, save_path, filename):
def red_to_magenta_batch(infile, save_path, filename):
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
    if filename == '':
        filename = os.path.basename(infile)
    outfile = os.path.join(save_path, filename)
    pdb.gimp_file_save(img, img.layers[0], outfile, outfile)


register(
    'python-fu-red-to-magenta-batch',  # name
    'Change red to magenta for colorblind people.',  # blurb
    'red_to_magenta(infile, save_path, filename) -> to file',  # help
    'Tanya Schlusser',  # author
    'public domain',  # copyright
    '2015',  # date
    '_Red to magenta...',  # menu_path
    '',  # image_types
    [
     (PF_FILE, "infile", "Path for input file", ''),
     (PF_DIRNAME, "save-path", "Path for output filename", os.getcwd()),
     (PF_STRING, "filename",  "Filename for export",  "fixed.png")
    ],  # type
    [],  # params
    red_to_magenta_batch,  # ret_vals
    menu="<Toolbox>/My-Python-Fu/"
    )


main()
