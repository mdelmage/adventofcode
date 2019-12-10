#!/usr/bin/python

IMAGE_WIDTH = 25
IMAGE_HEIGHT = 6

# Open input file
filename = "day8.txt"
f = open(filename, "r")

fewest_zeroes = IMAGE_WIDTH * IMAGE_HEIGHT + 1
fewest_zeroes_layer = None

with open(filename, "r") as f:
    for line in f:
        layers = len(line.strip()) / IMAGE_HEIGHT / IMAGE_WIDTH
        for layer in range(layers):
            digits = [0, 0, 0]
            for i in range(IMAGE_HEIGHT * IMAGE_WIDTH):
                digit = int(line[layer * (IMAGE_HEIGHT * IMAGE_WIDTH) + i])
                digits[digit] += 1
            if digits[0] < fewest_zeroes:
                fewest_zeroes = digits[0]
                fewest_zeroes_layer = digits
        print "Layer with fewest zeroes: {0}".format(fewest_zeroes_layer)
        print "1 digits * 2 digits = {0}".format(fewest_zeroes_layer[1] * fewest_zeroes_layer[2])
    