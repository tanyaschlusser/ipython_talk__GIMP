"""
show_eigenfaces.py
~~~~~~~~~~~~~~~~~~

Show Eigenvectors of faces from 

Converted to Python from:
        http://docs.opencv.org/modules/contrib/doc/facerec/facerec_tutorial.html
"""
import glob
import cv2
import numpy as np

def rescale(img):
    ## the None is a pointer to the destination matrix (useful if in C).
    return cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)

att_dataset = glob.glob('orl_faces/s*/*.pgm')
train_img = []
train_label = []

for fname in att_dataset:
    img = cv2.imread(fname, cv2.IMREAD_GRAYSCALE)
    label = fname.split('/')[1].strip('s')
    train_img.append(img)
    train_label.append(label)

train_label = np.array(train_label, dtype=np.int32)
model = cv2.createEigenFaceRecognizer()
model.train(train_img, train_label)
W = model.getMat('eigenvectors')
mean = model.getMat('mean')

# Prepare a 3 x 5 array of images
height, width = img.shape
nrow, ncol = 3, 5
scale = 2  # To make it big enough for projection onscreen
imgarray = np.zeros((height * nrow, width * ncol), dtype=np.uint8)
big_img = np.zeros((height * nrow * scale, width * ncol * scale), dtype=np.uint8)

# Show eigenvectors of the face recognition model.
for i in range(nrow * ncol):
    row = (i / ncol) * height
    col = (i % ncol) * width
    eigenvector = W[:,i]
    # unflatten the vector
    eigen_img = eigenvector.reshape(img.shape)
    imgarray[row:(row+height), col:(col+width)] = rescale(eigen_img)

big_img[:,:] = np.kron(imgarray, [[1,1],[1,1]])
colorized_img = cv2.applyColorMap(big_img, cv2.COLORMAP_JET)
cv2.imshow("eigenfaces", colorized_img)
cv2.waitKey(0)
cv2.destroyWindow("eigenfaces")

# Show the array of various projections of the same face.
#components = range(10, W.shape[1], (W.shape[1] - 10) / (nrow * ncol))
components = range(25, 400, 25)
for i in range(nrow * ncol):
    row = (i / ncol) * height
    col = (i % ncol) * width
    eigenvectors = W[ :,:components[i] ]
    data = img.reshape((1, img.size))
    projections = cv2.PCAProject(data, mean, eigenvectors.transpose())
    proj_img = projections.dot(eigenvectors.transpose())
    proj_img = proj_img.reshape(img.shape)
    imgarray[row:(row+height), col:(col+width)] = rescale(proj_img)

big_img[:,:] = np.kron(imgarray, [[1,1],[1,1]])
cv2.imshow(
        "projections -- {} to {}".format(components[0], components[-1]),
        big_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
