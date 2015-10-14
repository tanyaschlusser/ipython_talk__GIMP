###
## Copied from:
##    https://github.com/Itseez/opencv/tree/master/samples/python2/facedetect.py
##   ... with the video capture functions replaced by still image functions,
##       just like in:
##    https://realpython.com/blog/python/face-recognition-with-python
##

#import numpy as np
import cv2
haarcascades = cv2.__file__.split('lib')[0] + 'share/OpenCV/haarcascades/'

help_message = '''
USAGE: facedetect.py [--cascade <cascade_fn>] [--nested-cascade <cascade_fn>] [<image_source>]
'''

def detect(img, cascade, minSize=(20,20)):
    rects = cascade.detectMultiScale(
            img,
            scaleFactor=1.05,
            minNeighbors=4,
            minSize=minSize,
            flags = cv2.CASCADE_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects

def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

if __name__ == '__main__':
    import sys, getopt

    args, img_src = getopt.getopt(sys.argv[1:], '', ['cascade=', 'nested-cascade='])
    try:
        img_src = img_src[0]
    except:
        img_src = 0
        print help_message

    args = dict(args)
    if args.get('--help', None):
        print help_message
        sys.exit()
    cascade_fn = args.get('--cascade', haarcascades + "haarcascade_frontalface_alt.xml")
    nested_fn  = args.get('--nested-cascade', haarcascades + "haarcascade_eye.xml")

    cascade = cv2.CascadeClassifier(cascade_fn)
    nested = cv2.CascadeClassifier(nested_fn)

    img = cv2.imread (img_src)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    rects = detect(gray, cascade)
    vis = img.copy()
    draw_rects(vis, rects, (0, 255, 0))
    if not nested.empty():
        for x1, y1, x2, y2 in rects:
            roi = gray[y1:y2, x1:x2]
            vis_roi = vis[y1:y2, x1:x2]
            subrects = detect(roi.copy(), nested, minSize=(8,8))
            draw_rects(vis_roi, subrects, (255, 0, 0))


    cv2.imshow("facedetect", vis)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
