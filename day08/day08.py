#!/usr/bin/python

IMAGE_WIDTH = 25
IMAGE_HEIGHT = 6

PIXEL_MISSING     = -1
PIXEL_BLACK       = 0
PIXEL_WHITE       = 1
PIXEL_TRANSPARENT = 2

# Open input file
filename = "day08.txt"
f = open(filename, "r")

fewest_zeroes = IMAGE_WIDTH * IMAGE_HEIGHT + 1
fewest_zeroes_layer = None

layers = []

with open(filename, "r") as f:
    for line in f:
        layer_count = len(line.strip()) / IMAGE_HEIGHT / IMAGE_WIDTH
        for layer in range(layer_count):
            digits = [0, 0, 0]
            layers.append([])
            for i in range(IMAGE_HEIGHT * IMAGE_WIDTH):
                digit = int(line[layer * (IMAGE_HEIGHT * IMAGE_WIDTH) + i])
                digits[digit] += 1
                layers[layer].append(digit)
            if digits[0] < fewest_zeroes:
                fewest_zeroes = digits[0]
                fewest_zeroes_layer = digits
        print "Layer with fewest zeroes: {0}".format(fewest_zeroes_layer)
        print "1 digits * 2 digits = {0}".format(fewest_zeroes_layer[1] * fewest_zeroes_layer[2])

        # Render the image based on the topmost non-transparent pixel
        rendered_layer = [PIXEL_MISSING] * IMAGE_WIDTH * IMAGE_HEIGHT
        for layer in layers:
            for digit in range(len(layer)):
                if PIXEL_MISSING == rendered_layer[digit] and PIXEL_TRANSPARENT != layer[digit]:
                    rendered_layer[digit] = layer[digit]

        for pixel in range(len(rendered_layer)):
            if PIXEL_BLACK == rendered_layer[pixel]:
                print " ",
            else:
                print "*",
            if IMAGE_WIDTH - 1 == pixel % IMAGE_WIDTH:
                print ""
