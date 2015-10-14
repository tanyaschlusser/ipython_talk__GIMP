###
## Converted to Python from:
##    http://docs.opencv.org/modules/contrib/doc/facerec/facerec_tutorial.html
##
import glob
import random

import cv2
import numpy as np

att_dataset = glob.glob('orl_faces/s*/*.pgm')
is_color = False
pairs = []

for fname in att_dataset:
    img = cv2.imread(fname, is_color)
    label = fname.split('/')[1].strip('s')
    pairs.append([img, label])


principal_components = 8
ntest = 10
random.shuffle(pairs)
train_img, train_label = zip(*pairs[:-ntest])
train_label = np.array(train_label, dtype=np.int32)

model = cv2.createEigenFaceRecognizer(principal_components)
model.train(train_img, train_label)

for img, label in pairs[-ntest:]:
    # Need to make the image one big long row
    flattened_img = img.reshape(img.size)
    prediction, confidence = model.predict(flattened_img)
    print "Predicted:", prediction, "actual:", label,
    print "distance:", round(confidence)
