#!/usr/bin/env python

"""
    Author : Mridul Ahuja (original author)
    Author : Alexander Willner (updates, refactoring)
    Github : https://github.com/AlexanderWillner/csv2vcf
    Description : A small command line tool to convert CSV files to VCard files

"""

import os
import sys
import csv
import json
import argparse
import copy

def make_n(fields):
    if 'n' in fields:
        return fields['n']
    else:
        return fields.get('given', '') + ' ' + fields.get('surname', '')

VCARD_FIELDS = [
    ('FN', 'fn'),
    ('N', make_n),
    ('NICKNAME', 'nickname'),
    ('TEL;HOME;VOICE', 'tel'),
    ('EMAIL', 'email'),
    ('BDAY', 'bday'),
    ('ORG', 'org'),
    ('ROLE', 'role'),
    ('URL', 'url'),
]

class FieldMapper:
    def __init__(self, mapping):
        self._mapping = mapping

    def map_row(self, row):
        return {key: row[value]
                for (key, value) in self._mapping.items()}

def read_csv(csv, mapper):
    return [mapper.map_row(row) for row in csv]

def parse_mapping(s):
    tag, value = maybe_tagged(s)
    return (tag, FieldMapper(json.loads(value)))

def maybe_tagged(s):
    idx = s.find(':')
    if idx is None or not s[:idx].isalnum():
        return (None, s)
    else:
        return (s[:idx], s[idx + 1:])

def parse_join_keys(s):
    return s.split(':')

def build_index(rows, key):
    idx = {}
    for i, row in enumerate(rows):
        idx[row[key]] = i
    return idx

def join_tables(tables, keys):
    result = copy.copy(tables[0])
    result_idx = [(key, build_index(result, key)) for key in keys]
    for (key, idx), table in zip(result_idx, tables[1:]):
        for row in table:
            key_value = row[key]
            result[idx[key_value]].update(row)
    return result

def format_vcf(rows):
    for row in rows:
        print('BEGIN:VCARD')
        print('VERSION:3.0')
        for (key, getter) in VCARD_FIELDS:
            if callable(getter):
                value = getter(row)
            else:
                value = row.get(getter, '')
            print('{}:{}'.format(key, value))
        print('END:VCARD')

def main(args):
    parser = argparse.ArgumentParser(description='Convert CSV to VCF')
    parser.add_argument('--map', metavar='MAPPING',
                        action='append', dest='mappings',
                        type=parse_mapping)
    parser.add_argument('--join', metavar='KEYS', type=parse_join_keys, default=[])
    parser.add_argument('input_specs', metavar='INPUT-SPECS', nargs='*', type=maybe_tagged)
    options = parser.parse_args(args)

    inputs = []
    mappings = dict(options.mappings)
    for (tag, filename) in options.input_specs:
        mapping = mappings[tag]
        with open(filename) as f:
            reader = csv.DictReader(f)
            inputs.append(read_csv(reader, mapping))
    combined = join_tables(inputs, options.join)
    format_vcf(combined)

if __name__ == '__main__':
    main(sys.argv[1:])
