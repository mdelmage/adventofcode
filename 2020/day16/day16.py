#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This function identifies an index in the tickets data that can only be valid
# for a single field name, and returns the mapping of ticket index --> field name.
def find_an_exclusive_field():
    for idx in values_by_field_number:
        matched_fields = 0
        for field_name in fields:
            # Do all data for this ticket index meet the rules for this field name?
            if values_by_field_number[idx].issubset(fields[field_name]):
                matched_fields += 1
                match_idx = idx
                match_name = field_name

        # Found an exclusive match! Bail out.
        if matched_fields == 1:
            return (match_idx, match_name)

    print 'Error! Could not find an exclusive field.'
    return (None, None)

# Parse the tickets info and save each line
with open('day16_input.txt') as f:
    ticket_document = [line.rstrip('\n').strip(':') for line in f]

line_num = 0
fields = {}
valid_values = set()
nearby_parsing = False
nearby_tickets = []
while line_num < len(ticket_document):
    line = ticket_document[line_num]
    if ':' in line:
        # A bit of nasty parsing, to extract data of the format 'field_name: min1-max1 or min2-max2'.
        tokens = line.split(': ')
        field_name = tokens[0]
        field_range = tokens[1]
        range_tokens = field_range.split(' or ')
        fields[field_name] = set()

        for token in range_tokens:
            range_low_high = [int(x) for x in token.split('-')]
            low = range_low_high[0]
            high = range_low_high[1]
    
            # We're doing a lot of subset-type checks, so use the set() primitive.
            fields[field_name] |= set(range(low, high + 1))
            valid_values |= set(range(low, high + 1))
    elif 'your ticket' in line:
        line_num += 1
        your_ticket = [int(x) for x in ticket_document[line_num].split(',')]
    elif 'nearby tickets' in line:
        nearby_parsing = True
    elif nearby_parsing:
        nearby_tickets.append([int(x) for x in line.split(',')])
    line_num += 1

# Start by determining which tickets are completely invalid; these are tickets that contain values
# which aren't valid for any field. Ignore your ticket for now.
error_rate = 0
valid_tickets = []
for ticket in nearby_tickets:
    valid = True
    for value in ticket:
        # It doesn't matter which position corresponds to which field; you can identify invalid nearby tickets
        # by considering only whether tickets contain values that are not valid for any field.
        if value not in valid_values:
            valid = False
            error_rate += value

    # Now that you've identified which tickets contain invalid values, discard those tickets entirely.
    # Use the remaining valid tickets to determine which field is which.
    if valid: valid_tickets.append(ticket)

print 'Part One: ticket scanning error rate is {0}.'.format(error_rate)

# Generate a lookup of all values for a given field index.
values_by_field_number = {}
for idx in range(len(fields)):
    values = set()
    for ticket in valid_tickets:
        values.add(ticket[idx])
    values_by_field_number[idx] = values

# Once you work out which field is which, look for the six fields on your ticket
# that start with the word departure. What do you get if you multiply those six values together?
product = 1
while len(fields) > 0:
    (idx, field_name) = find_an_exclusive_field()
    if 'departure' in field_name:
        product *= your_ticket[idx]
    del fields[field_name]

print 'Part Two: product of all departure-related fields is {0}.'.format(product)