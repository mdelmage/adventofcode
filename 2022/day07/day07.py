#!/usr/bin/env python
# -*- coding: utf-8 -*-

DISK_SPACE_TOTAL = 70000000
DISK_SPACE_REQUIRED = 30000000

class FsObject:
    def __init__(self, name):
        self.name = name

class Directory(FsObject):
    def __init__(self, parent, name):
        super().__init__(name)
        self.parent = parent
        self.contents = []

    def add(self, obj):
        self.contents.append(obj)

    def cd(self, target):
        if target == '..':
            return self.parent
        else:
            for item in self.contents:
                if item.name == target:
                    return item
        return self

    def create(self, target):
        tokens = target.split(' ')
        if tokens[0] == 'dir':
            # dir xyz means that the current directory contains a directory named xyz.
            self.contents.append(Directory(self, tokens[1]))
        else:
            # 123 abc means that the current directory contains a file named abc with size 123.
            self.contents.append(File(tokens[1], int(tokens[0])))

    def storage_size(self):
        # The total size of a directory is the sum of the sizes of the files it contains,
        # directly or indirectly. (Directories themselves do not count as having any intrinsic size.)
        size = 0
        for item in self.contents:
            size += item.storage_size()
        return size

    def subdirectory_sizes(self):
        # Start the list with our own local+subdirs size
        subdirs = [self.storage_size()]

        # Add all the subdirectory sizes to the list.
        # (As in this example, this process can count files more than once!)
        for item in self.contents:
            if isinstance(item, Directory):
                subdirs += item.subdirectory_sizes()

        return subdirs

class File(FsObject):
    def __init__(self, name, size):
        super().__init__(name)
        self.size = size

    def storage_size(self):
        return self.size

# Parse the terminal output file
with open('day07_input.txt') as f:
    log = [line.rstrip('\n') for line in f]

line = 0
root = Directory(None, '/')
current_dir = root

while line < len(log):
    # Assume that the logfile starts with a command, and that processing a command
    # consumes its output, so that the next loop iteration is ready to process
    # another command.
    tokens = log[line].split(' ')
    cmd = tokens[1]

    if cmd == 'cd':
        # Change to the requested directory
        current_dir = current_dir.cd(tokens[2])
    elif cmd == 'ls':
        # Process (and consume) the directory listing output.
        # Take care to handle an EOF condition.
        while line + 1 < len(log) and log[line + 1][0] != '$':
            line += 1
            current_dir.create(log[line])
    line += 1

# Find all of the directories with a total size of at most 100000.
# What is the sum of the total sizes of those directories?
total_100k_sizes = sum([d for d in root.subdirectory_sizes() if d <= 100000])
print('Part One: Total sizes of 100k directories is {0}.'.format(total_100k_sizes))

# The total disk space available to the filesystem is 70000000.
# To run the update, you need unused space of at least 30000000.
# You need to find a directory you can delete that will free up enough space to run the update.
#
# Find the smallest directory that, if deleted, would free up enough space
# on the filesystem to run the update. What is the total size of that directory?
storage_used = root.storage_size()
for dir_size in sorted(root.subdirectory_sizes()):
    # Simulate deleting directories by adding their size back to the disk space and see if we're good
    if DISK_SPACE_TOTAL - storage_used + dir_size >= DISK_SPACE_REQUIRED:
        print('Part Two: Total size of directory that needs to be deleted is {0}.'.format(dir_size))
        break
