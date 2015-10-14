#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gimpfu import *
import os

def red_to_magenta(img):
    gimp.Display(img)  # Create a new image window
    gimp.displays_flush()  # Show the new image window
    gimp.context_push()
    img.undo_group_start()
    red = pdb.gimp_channel_new_from_component(img, RED_CHANNEL, 'red')
    img.add_channel(red)
    pdb.gimp_edit_copy(red)

    pdb.gimp_image_set_component_active(img, RED_CHANNEL, False)
    pdb.gimp_image_set_component_active(img, GREEN_CHANNEL, False)
    pdb.gimp_image_set_component_active(img, BLUE_CHANNEL, True)

    lyr = pdb.gimp_edit_paste(img.layers[0], True)
    pdb.gimp_floating_sel_anchor(lyr)
    img.remove_channel(red)
    img.undo_group_end()
    gimp.context_pop()
    

register(
    'python-fu-red-to-magenta',  # name
    'Change red to magenta for colorblind people.',  # blurb
    'red_to_magenta(img) -> add the red channel to the blue one',  # help
    'Tanya Schlusser',  # author
    'public domain',  # copyright
    '2015',  # date
    '_Red to magenta...',  # menu_path
    'RGB*',  # image_types
    [
     (PF_IMAGE, 'img', 'Input image', None)
    ],  # type
    [],  # params
    red_to_magenta,  # ret_vals
    menu="<Image>/Filters/Artistic/"
    )


main()
