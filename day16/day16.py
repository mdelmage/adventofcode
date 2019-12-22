#!/usr/bin/python
# coding: utf-8

import datetime

PATTERN_BASE = [0, 1, 0, -1]

INPUT_REPEAT_COUNT = 10000
FFT_PHASE_COUNT    = 100
MESSAGE_LENGTH     = 8

patterns = {}

def timestamp(phase):
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print "Starting Phase {0}. Current time is {1}".format(phase, current_time)


def fft(number, phases, offset):
    print "FFTing {0}... for {1} phases with offset {2}!".format(number[:16], phases, offset)

    # Turn the input into a list
    signal = [int(x) for x in number] * INPUT_REPEAT_COUNT
    original_signal_length = len(signal)
    signal = signal[offset:]

    # Loop for each FFT phase
    for phase in range(phases):
        timestamp(phase + 1)
        new_signal = [0] * (original_signal_length - offset)

        # Loop for each digit we're computing
        digit = offset + 1
        while digit <= original_signal_length:
            subdigit = digit - offset - 1
            subsignal = signal[subdigit:]

            # Loop for each digit we're sourcing for the digit compute.
            # By inspection, for offsets deep (~90%) into the input, the pattern will
            # just be all 1's. Therefore, sum the remaining digits.
            # To optimize, don't re-sum for every digit; take the last computed sum
            # and remove one term.
            if 0 == subdigit:
                new_signal[subdigit] = sum(subsignal)
            else:
                new_signal[subdigit] = new_signal[subdigit - 1] - signal[subdigit - 1]
            digit += 1

        digit = offset + 1
        while digit <= original_signal_length:
            subdigit = digit - offset - 1
            new_signal[subdigit] = abs(new_signal[subdigit]) % 10
            digit += 1

        signal = new_signal
    print signal[:MESSAGE_LENGTH]

# Open input file
filename = "day16.txt"
with open(filename, "r") as f:
    for line in f:
        offset = int(line[:7])
        fft(line.strip(), FFT_PHASE_COUNT, offset)