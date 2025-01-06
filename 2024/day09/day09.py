#!/usr/bin/env python
# -*- coding: utf-8 -*-

FREE_SPACE = -1

# Parse the disk map.
with open('day09_input.txt') as f:
    disk_map = [int(n) for n in [line.rstrip('\n') for line in f][0]]

    # The disk map uses a dense format to represent the layout of files and free space on the disk.
    # The digits alternate between indicating the length of a file and the length of free space.
    disk_blockwise = []
    blocks_free = []
    blocks_used = []
    file_id_to_block = {}
    block_to_contents = {}
    file_length = True

    # Each file on disk also has an ID number based on the order of the files as they appear before
    # they are rearranged, starting with ID 0.
    file_id = 0
    block = 0
    for n in disk_map:
        if file_length:
            # Make two copies of the disk so we can try our different consolidation methods.
            # One, the blockwise disk, will be a simple list of block contents.
            # The other, the filewise disk, will be a list of files/free spaces and their lengths.
            disk_blockwise += [file_id for i in range(n)]
            blocks_used += [block + i for i in range(n)]
            file_id_to_block[file_id] = block
            block_to_contents[block] = (file_id, n)
            file_id += 1
        else:
            disk_blockwise += [FREE_SPACE for i in range(n)]
            blocks_free += [block + i for i in range(n)]
            block_to_contents[block] = (FREE_SPACE, n)
        block += n
        file_length = not file_length

# The amphipod would like to move file blocks one at a time from the end of the disk to the leftmost
# free space block (until there are no gaps remaining between file blocks).
for b in range(len(blocks_free)):
    if blocks_used[-(b+1)] <= blocks_free[b]: break
    disk_blockwise[blocks_free[b]] = disk_blockwise[blocks_used[-(b+1)]]
    disk_blockwise[blocks_used[-(b+1)]] = 0


# The final step of this file-compacting process is to update the filesystem checksum.
# To calculate the checksum, add up the result of multiplying each of these blocks' position
# with the file ID number it contains. The leftmost block is in position 0.
# If a block contains free space, skip it instead.
checksum = 0
for position in range(len(disk_blockwise)):
    if disk_blockwise[position] != FREE_SPACE: checksum += (position * disk_blockwise[position])

# Compact the amphipod's hard drive using the process he requested. What is the resulting filesystem checksum?
print('Part One: The filesystem checksum when optimized by blocks is {0}.'.format(checksum))

# Maybe introducing all of that file system fragmentation was a bad idea?
#
# The eager amphipod already has a new plan: rather than move individual blocks,
# he'd like to try compacting the files on his disk by moving whole files instead.
#
# This time, attempt to move whole files to the leftmost span of free space blocks that could fit
# the file. Attempt to move each file exactly once in order of decreasing file ID number starting
# with the file with the highest file ID number. If there is no span of free space to the left of a file
# that is large enough to fit the file, the file does not move.
max_file_id = file_id - 1
for file_id in range(max_file_id, -1, -1):
    # Search front-to-back for a space large enough for our file.
    file_block = file_id_to_block[file_id]
    file_len = block_to_contents[file_block][1]

    dest_block = None
    for b in sorted(block_to_contents.keys()):
        if b >= file_block: break
        block_contents, block_len = block_to_contents[b]
        if block_contents == FREE_SPACE and block_len >= file_len:
            dest_block = b
            break

    if dest_block:
        free_len = block_to_contents[b][1]
        block_to_contents[b] = (file_id, file_len)
        file_id_to_block[file_id] = b
        if free_len > file_len:
            # More space than needed. Insert the file before the free block,
            # then reduce the size of the free block accordingly.
            block_to_contents[b + file_len] = (FREE_SPACE, free_len - file_len)

        # Remove the file at the previous location.
        block_to_contents[file_block] = (FREE_SPACE, file_len)

# The process of updating the filesystem checksum is the same.
checksum = 0
for f in file_id_to_block:
    block = file_id_to_block[f]
    block_len = block_to_contents[block][1]
    checksum += sum([f * (block + i) for i in range(block_len)])

# Start over, now compacting the amphipod's hard drive using this new method instead.
# What is the resulting filesystem checksum?
print('Part Two: The filesystem checksum when optimized by files is {0}.'.format(checksum))