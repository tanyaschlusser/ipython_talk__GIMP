# get_faces.sh
#
echo "Starting the download"
URL=http://www.cl.cam.ac.uk/research/dtg/attarchive/pub/data/att_faces.tar.Z
curl --compressed ${URL} | tar xzvf -
echo "Done!"
echo "for more information, see http://www.cl.cam.ac.uk/research/dtg/attarchive/facedatabase.html"
