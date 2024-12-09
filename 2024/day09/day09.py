#!/usr/bin/env python
# -*- coding: utf-8 -*-

FREE_SPACE = -1

# Remove all unnecessary (zero) blocks and consolidate contiguous blocks with the same ID.
def consolidate_free_space(disk):
    done = False
    while not done:
        done = True
        # If there's a zero-length block, remove it.
        for block_num in range(len(disk)):
            (block_id, block_len) = disk[block_num]
            if block_len == 0:
                disk = disk[:block_num] + disk[block_num + 1:]
                done = False
                break

        # If there are two contiguous free blocks, consolidate them.
        for block_num in range(len(disk) - 1):
            (block_id, block_len) = disk[block_num]
            (block_id_next, block_len_next) = disk[block_num + 1]
            if block_id == block_id_next:
                disk = disk[:block_num] + [(block_id, block_len + block_len_next)] + disk[block_num + 2:]
                done = False
                break

    return disk

# Parse the disk map.
with open('day09_input.txt') as f:
    disk_map = [int(n) for n in [line.rstrip('\n') for line in f][0]]

    # The disk map uses a dense format to represent the layout of files and free space on the disk.
    # The digits alternate between indicating the length of a file and the length of free space.
    disk_blockwise = []
    disk_filewise = []
    file_lengths = {}
    file_length = True

    # Each file on disk also has an ID number based on the order of the files as they appear before
    # they are rearranged, starting with ID 0.
    file_id = 0
    for n in disk_map:
        if file_length:
            # Make two copies of the disk so we can try our different consolidation methods.
            # One, the blockwise disk, will be a simple list of block contents.
            # The other, the filewise disk, will be a list of files/free spaces and their lengths.
            disk_blockwise += [file_id for i in range(n)]
            disk_filewise.append((file_id, n))
            file_lengths[file_id] = n
            file_id += 1
        else:
            disk_blockwise += [FREE_SPACE for i in range(n)]
            disk_filewise.append((FREE_SPACE, n))
        file_length = not file_length

# The amphipod would like to move file blocks one at a time from the end of the disk to the leftmost
# free space block (until there are no gaps remaining between file blocks).
disk = [n for n in disk_blockwise]
while FREE_SPACE in disk:
    block_src = disk[-1]
    disk = disk[:-1]
    block_dest = disk.index(FREE_SPACE)
    disk = disk[:block_dest] + [block_src] + disk[block_dest + 1:]

# The final step of this file-compacting process is to update the filesystem checksum.
# To calculate the checksum, add up the result of multiplying each of these blocks' position
# with the file ID number it contains. The leftmost block is in position 0.
# If a block contains free space, skip it instead.
checksum = 0
for position in range(len(disk)):
    checksum += position * int(disk[position])

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
disk = [n for n in disk_filewise]
max_file_id = disk[-1][0]
for file_id in range(max_file_id, 0, -1):
    file_len = file_lengths[file_id]
    file_index = disk.index((file_id, file_len))
    for b in range(file_index):
        (block_id, block_len) = disk[b]
        if block_id == FREE_SPACE and block_len >= file_lengths[file_id]:
            disk[file_index] = (FREE_SPACE, file_len)
            disk = disk[:b] + [(file_id, file_len)] + [(FREE_SPACE, block_len - file_len)] + disk[b + 1:]
            disk = consolidate_free_space(disk)
            break

# The process of updating the filesystem checksum is the same.
checksum = 0
raw_block = 0
for (block_id, block_len) in disk:
    if block_id != FREE_SPACE:
        for i in range(block_len):
            checksum += block_id * (raw_block + i)
    raw_block += block_len

# Compact the amphipod's hard drive using the process he requested.
# What is the resulting filesystem checksum?
print('Part Two: The filesystem checksum when optimized by files is {0}.'.format(checksum))