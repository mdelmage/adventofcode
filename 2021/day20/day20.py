#!/usr/bin/env python
# -*- coding: utf-8 -*-

PIXEL_ON  = '#'
PIXEL_OFF = '.'

GROWTH_PER_ITERATION = 3

ITERATIONS_PART_ONE = 2
ITERATIONS_PART_TWO = 50

def filter_to_integer(image, x, y, default_value):
	# The image enhancement algorithm describes how to enhance an image by simultaneously
	# converting all pixels in the input image into an output image. Each pixel of the
	# output image is determined by looking at a 3x3 square of pixels centered on the
	# corresponding input image pixel.
	integer = 0
	for y_local in range(y - 1, y + 2):
		for x_local in range(x - 1, x + 2):
			# These nine input pixels are combined into a single binary number
			# that is used as an index in the image enhancement algorithm string.
			integer <<= 1
			if image.get((x_local, y_local), default_value) == PIXEL_ON:
				integer += 1
	return integer

def run_filter(i, default_value):
	# Scan a 3x3 area for each pixel in the image we're going to generate.
	# Because our filter is sneaky and lights up infinite pixels sometimes,
	# we'll provide a default value for what we expect in the image if we
	# don't get a hit.
	new_image = {}
	for x in range(0 - (GROWTH_PER_ITERATION * iteration), image_size_x + (GROWTH_PER_ITERATION * iteration) + 1):
		for y in range(0 - (GROWTH_PER_ITERATION * iteration), image_size_y + (GROWTH_PER_ITERATION * iteration) + 1):
			filter_index = filter_to_integer(i, x, y, default_value)
			new_image[(x, y)] = enhancement_algo[filter_index]
	return new_image

def lit_pixels(image):
	pixel_count = 0
	for pixel in image:
		if image[pixel] == PIXEL_ON: pixel_count += 1
	return pixel_count

# Parse the ocean trench map file
with open('day20_input.txt') as f:
	lines = [line.rstrip('\n') for line in f]

# The first section is the image enhancement algorithm. It is normally given on a single line,
# but it has been wrapped to multiple lines in this example for legibility.
enhancement_algo = lines[0]

# The second section is the input image, a two-dimensional grid of light pixels (#) and dark pixels (.).
input_image = lines[2:]
image = {}
for y in range(len(input_image)):
	for x in range(len(input_image[y])):
		if input_image[y][x] == PIXEL_ON: image[(x, y)] = input_image[y][x]

image_size_x = x
image_size_y = y

iteration = 1
while iteration <= ITERATIONS_PART_TWO:
	# The puzzle input very subtly deviates from the example given in the puzzle description:
	# Any 3x3 region with no lit pixels will be lit in the next iteration, meaning an infinite
	# number will be lit on odd ticks, and then be unlit on the subsequent (even) tick.
	#
	# To handle this, the filter only examines an area 3 pixels larger in every dimension
	# than the existing image. We then know on the next tick that every pixel should default
	# to "lit" if it's not in the given image.
	image_with_infinite_pixels_lit = run_filter(image, default_value=PIXEL_OFF)
	iteration += 1

	# Run the same filter, but now defaulting to "lit" out to infinity.
	image = run_filter(image_with_infinite_pixels_lit, default_value=PIXEL_ON)
	iteration += 1

	# Start with the original input image and apply the image enhancement algorithm twice, being careful to account
	# for the infinite size of the images. How many pixels are lit in the resulting image?
	if iteration - 1 == ITERATIONS_PART_ONE:
		print('Part One: {0} pixels are lit after {1} image enhancement algorithms.'.format(lit_pixels(image), ITERATIONS_PART_ONE))

# Start again with the original input image and apply the image enhancement algorithm 50 times.
# How many pixels are lit in the resulting image?
print('Part Two: {0} pixels are lit after {1} image enhancement algorithms.'.format(lit_pixels(image), ITERATIONS_PART_TWO))