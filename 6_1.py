#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import *

def conver_file(file_name):
    data = []
    headings = []
    alloys = []
    name, ext = os.path.splitext(file_name)
    output_name = name + ".p"

    for i, row in enumerate(irows(file_name, 2)):
        if i == 0:
            table_no = row[0].lower().replace('table','').strip()
        elif i == 1:
            caption = row[0]
        elif i == 2:
            headings = [h.split('(')[0].strip() for h in row]
            units = get_units(row)
            if verbose:
                print "Units:", units
                print "Headings:", headings
        else:
            if row[0] <> '':
                chemical_formula = row[0]
            else:  # skip empty lines
                continue

            properties = []
            prop = Property(name=headings[1])
            prop.scalars = row[1]
            prop.units = units[1]
            prop.table = {'number': table_no, 'caption': caption}
            properties.append(prop)

            data.append({'labels': [chemical_formula], 'value': properties})

    pickle.dump(data, open(output_name, 'w'))


for fn in ifiles():
    conver_file(fn)

