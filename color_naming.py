import colorsys
import csv
import sys
import getopt
from math import sqrt, floor
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

# ---------------------------------------------------------------- #

NUM_BINS = 10
BINS = [[] for i in range(NUM_BINS)]

# ---------------------------------------------------------------- #

# loads the 'training data' from its csv file
def load_data(filename):
    
    with open(filename, 'r') as f:
        # get lines
        reader = csv.reader(f, delimiter = ',')
        for row in reader:
            row[1] = int(row[1])
            row[2] = int(row[2])
            row[3] = int(row[3])
            # find bin number of this training color
            bno = bin_number((row[1], row[2], row[3]))
            # add to bin
            (BINS[bno]).append(((row[1], row[2], row[3]), row[0]))

# ---------------------------------------------------------------- #

# calculates the distance between x and z
def dist_calc(x, z):

    xR = x[0]
    xG = x[1]
    xB = x[2]
    
    dist = pow(xR - z[0], 2) + pow(xG - z[1], 2) + pow(xB - z[2], 2)
    return sqrt(dist)

# ---------------------------------------------------------------- #

# determines which bin z belongs to based on its hue value
def bin_number(z):

    zR = z[0]/256
    zG = z[1]/256
    zB = z[2]/256

    z_hsv = colorsys.rgb_to_hsv(zR, zG, zB)
    # Since hue values are between 0-1 and BINS are 0-0.1, 0.1-0.2, etc.,
    #  the bin number can easily be computed this way!
    binno = floor(z_hsv[0]*10)

    if binno == 10:
        # Special case when hue value == 1
        return 9
    return binno

# ---------------------------------------------------------------- #

# finds the color of the pixel z, comparing against the 'training data'.
def find_color(z):

    min_dist = pow(2, 30) # very large number to begin with
    color_name = None

    bno = bin_number(z)
    
    for cols in BINS[bno]:
        # Find color closest to z

        if dist_calc(cols[0], z) < min_dist:
            min_dist = dist_calc(cols[0], z)
            color_name = cols[1]

    return color_name

# ---------------------------------------------------------------- #

# generates the frequency of each basis color in the given image and stores the
#  raw data in imgcolors
def analyze_image(fname, imgcolors):
    # read in image into array red vals * green vals * blue vals
    img = mpimg.imread(fname)
    w = img.shape[0]
    h = img.shape[1]

    print("Analyzing colors....")
    for i in range(w):
        for j in range(h):
            # get color of this pixel
            c = find_color((img[i][j]))
            # add one more to its count
            imgcolors[c] += 1
        if (i != 0) && (i % 100 == 0):
            print(str(i) + " rows of pixels analyzed!")
    print("Done Analyzing!")

    for key, value in imgcolors.items():
        print(str(key)+ ": "+str(value))

    plt.bar(range(len(imgcolors)), list(imgcolors.values()), align='center')
    plt.xticks(range(len(imgcolors)), list(imgcolors.keys()), rotation=90)
    plt.savefig(fname.split('.')[0]+"_analysis.png")
    print("Plot saved!")

# ---------------------------------------------------------------- #

def print_usage(progname):
    print("Usage: python3 "+progname+" picname [-rgb]")
    print("Analyzes the colors of the pixels in picname")
    print("-rgb: If this option is specified, ignores picname and prompts user for RGB values to name")

# ---------------------------------------------------------------- #

def main():

    load_data("colordata.csv")
    imgcolors = {'Black' : 0, 'White' : 0, 'Red' : 0, 'Blue' : 0, 'Green' : 0,
        'Pink' : 0, 'Purple' : 0, 'Brown' : 0, 'Orange' : 0, 'Yellow' : 0,
        'Gray' : 0, 'Beige' : 0}


    argc = len(sys.argv)
    if (argc > 3) or (argc == 1):
        print_usage(sys.argv[0])
        exit(1)
    elif (argc == 3) and (sys.argv[2] != "-rgb"):
        print_usage(sys.argv[0])
        exit(1)
    elif (argc == 2 and sys.argv[1] == "-rgb") or (argc == 3):
        print("Press ctrl-C anytime to stop")
        while True:
            R = eval(input("Red: "))
            assert 0 <= R <= 255
            G = eval(input("Green: "))
            assert 0 <= G <= 255
            B = eval(input("Blue: "))
            assert 0 <= B <= 255
            print(find_color((R, G, B)))
    else:
        analyze_image(sys.argv[1], imgcolors)


if __name__ == "__main__":
    main()




