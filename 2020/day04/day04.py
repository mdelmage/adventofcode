#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

# Parse the passport list and save each line
with open('day04_input.txt') as f:
    passport_list = [''] + [line.rstrip('\n') for line in f]

# The automatic passport scanners are slow because they're having trouble
# detecting which passports have all required fields. The expected fields
# are as follows:
#
# byr (Birth Year)
# iyr (Issue Year)
# eyr (Expiration Year)
# hgt (Height)
# hcl (Hair Color)
# ecl (Eye Color)
# pid (Passport ID)
# cid (Country ID)
all_fields = set(['byr',
                  'iyr',
                  'eyr',
                  'hgt',
                  'hcl',
                  'ecl',
                  'pid',
                  'cid'])


# The third passport is interesting; the only missing field is cid,
# so it looks like data from North Pole Credentials, not a passport
# at all! Surely, nobody would mind if you made the system temporarily
# ignore missing cid fields. Treat this "passport" as valid.
optional_field = set(['cid'])

passports = []
for line in passport_list:
    if line == '':
        passports.append({})
    else:
        tokens = line.replace(':', ' ').split()
        for i in range(len(tokens)):
            if (i % 2) == 0: passports[len(passports) - 1][tokens[i]] = tokens[i + 1]

part_one_valid_passports = 0
part_two_valid_passports = 0
for p in passports:
    fields = set()
    for f in p:
        fields.add(f)
    if fields | optional_field == all_fields:
        part_one_valid_passports += 1
        
        # The line is moving more quickly now, but you overhear airport security
        # talking about how passports with invalid data are getting through.
        # Better add some data validation, quick!
        #
        # You can continue to ignore the cid field, but each other field has
        # strict rules about what values are valid for automatic validation:
        #
        # byr (Birth Year) - four digits; at least 1920 and at most 2002.
        # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
        # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
        # hgt (Height) - a number followed by either cm or in:
        # If cm, the number must be at least 150 and at most 193.
        # If in, the number must be at least 59 and at most 76.
        # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
        # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
        # pid (Passport ID) - a nine-digit number, including leading zeroes.
        # cid (Country ID) - ignored, missing or not.
        v = True
        v = v and int(p['byr']) >= 1920 and int(p['byr']) <= 2002
        v = v and int(p['iyr']) >= 2010 and int(p['iyr']) <= 2020
        v = v and int(p['eyr']) >= 2020 and int(p['eyr']) <= 2030
        v = v and (p['hgt'][-2:] == 'in' or p['hgt'][-2:] == 'cm')
        v = v and (((int(p['hgt'][:-2]) >= 150) and (int(p['hgt'][:-2]) <= 193)) or (p['hgt'][-2:] == 'in'))
        v = v and (((int(p['hgt'][:-2]) >= 59) and (int(p['hgt'][:-2]) <= 76)) or (p['hgt'][-2:] == 'cm'))
        v = v and re.match('#[0-9a-f]{6}', p['hcl'])
        v = v and (p['ecl'] in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'])
        v = v and re.match('^[\d]{9}$', p['pid'])
        if v: part_two_valid_passports += 1
        
print 'Part One: {0} valid passports out of {1}.'.format(part_one_valid_passports, len(passports))
print 'Part Two: {0} valid passports out of {1}.'.format(part_two_valid_passports, len(passports))