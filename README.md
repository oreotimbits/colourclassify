# Image Colour Classification Based on Pixel Intensity Values

This project aims to map an image's pixel intensity values to the twelve basic English color names (pink, purple, red, orange, yellow, green, cyan, blue, brown, white, grey, and black) to determine the amount of each colour in the picture.
While colour classification has a variety of uses in fields like image retrieval and colourblind assistance, 
I personally use this project to analyze a digitally created artwork for the approximate amount of paint/ink I'd need to recreate it on a traditional physical medium (e.g. canvas, wood panels, linoleum, etc).

## Usage

To analyze image.jpeg: python3 color_naming.py imgname.jpeg (this creates a png file imgname_analysis.png with the bar graph)
To get the colour of input RGB values: python3 color_naming.py -rgb 
Note that colordata.csv must be in the same directory as color_naming.py
Possible dependencies to install: python3.7 or higher, matplotlib (python3 -m pip install matplotlib).


## Implementation

The underlying algorithm used in this project was initially developed by Sainui and Pattanasatean in *Color Classification based on Pixel Intensity Values (2018)* for the 
19th IEEE/ACIS International Conference on Software Engineering, Artificial Intelligence, Networking and Parallel/Distributed Computing.

Summary: We initialize a ‘training data’ set of approximately 1000 RGB tuples with human-generated labels indicating their colours, which is one of the twelve basic colour names. 
We then sort them all into 10 bins based on their hue value in HSV colour format. 
Given an input RGB triple z, we first determine which bin it belongs to (to increase accuracy and to reduce the number of comparisons performed) and then find the training colour that is closest to it. 
To determine this, we treat each RGB triple like a coordinate in the Cartesian plane and simply find the 3D distance between the two points. The input triple is then named the same colour as the point closest to it.

## Areas for Improvement

*	Speed: The above computations can get extremely expensive when analyzing a larger image, since there are more pixels to analyze. One way to speed this up is by comparing fewer pixels in the image, since we currently analyze all of them. 
Skipping a fixed number of pixels at each iteration, however, will result in a subset of columns of pixels not being looked at.
A possible workaround to increase accuracy would be to randomly choose a (small) number of pixels to skip before determining the next pixel to analyze. This increases the randomness of the ignored pixels, 
increasing the probability that our selected pixels will form an accurate representation of the distribution of colours in the image.
*	Accuracy: The accuracy of the returned results directly depends on the accuracy of the human labels of the training data. Having many humans vote on the perceived colour of the RGB triples and averaging out their responses results in a more accurate label.
*	Increasing training data size: The more training data available, the higher the chance that there’s a training triple exactly the same/extremely close to the colour we’re observing. This does result in a speed-tradeoff, however.
*	Increasing colour identification capability: Could make this more useful for artists by adding the option to select which colours to detect. 
This would be especially helpful with detecting common paint colours like burnt sienna, crimson red, ochre yelllow, etc. for traditional paintings.

