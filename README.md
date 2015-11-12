# The corresponding slides for this are here:
http://tanyaschlusser.github.io/Python-Fu-in-GIMP.slides.html#/

## You will want to use Conda

The examples are with the OpenCV source:
https://github.com/Itseez/opencv/tree/master/samples/python2
I copied facedetect.py from here and
changed the video parts to static image parts.

For the compiled binaries, use conda.
I installed Anaconda but you can use miniconda too.

```
conda create -n with_opencv python=2.7 --file=requirements.txt
source activate with_opencv
```


When done, to deactivate the environment:
```
source deactivate
```


## The math

The detection is done using a [Haar Feature-based Cascade Classifier][haar].
It's a tree -- it compares Haar features to different positions on the
image and simply stops executing if the match is bad. Otherwise it
continues to compare the 6,000 some features with the image position
to identify a face.



## Face recognition
The [face recognition][facerec] function I call is the 'eigenfaces' one --
it unwraps a grayscale image (a matrix of values from 0 to 255) into
a single row -- each picture in the dataset is a row, and
each is classified as one of the 10 people in the set.
Principal Components Analysis is performed on the entire dataset to
identify directions with the most variation.
New images will have the same transformation matrix applied and
will be compared along the selected principal components to see
which person the image most closely matches.



[haar]: http://docs.opencv.org/modules/objdetect/doc/cascade_classification.html#cascade-classification
[facerec]: http://docs.opencv.org/modules/contrib/doc/facerec
