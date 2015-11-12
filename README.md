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

## Pumpkin
https://www.flickr.com/photos/robbyt/283346018/in/photolist-r3dUb-r3dU9

## The math

The detection is done using a [Haar Feature-based Cascade Classifier][haar].
That's



## Face recognition
[Face recognition][facerec]

[haar]: http://docs.opencv.org/modules/objdetect/doc/cascade_classification.html#cascade-classification
[facerec]: http://docs.opencv.org/modules/contrib/doc/facerec
