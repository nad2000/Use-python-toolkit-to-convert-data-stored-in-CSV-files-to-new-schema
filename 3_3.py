#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import *

def conver_file(file_name):
    data = []
    headings = []
    alloys = []
    name, ext = os.path.splitext(file_name)
    output_name = name + ".p"

    chemical_formula = "CoCrCuFeNi"

    for i, row in enumerate(irows(file_name, 6)):
        if i == 0:
            table_no = row[0].lower().replace('table','').replace(' ','')
        elif i == 1:
            caption = row[0]
        elif i == 2:
            headings = [h.split('(')[0].strip() for h in row]
            units = get_units(row)
            if verbose:
                print "Units:", units
                print "Headings:", headings
        elif i in (3, 4, 5, 7, 9):  # skip "Nominal" and row descriptios
            if i > 4:  # read the phase names
                phase_names = row[0]
            continue
        elif i in (6, 8, 10):  # Actual, Dendrite and Interdendrite
            compositions = []
            for (e, a) in zip(headings, row):
                compositions.append(Composition(
                    element=e,
                    atomic_percent=a,
                    table = {'number': table_no, 'caption': caption}))
            if i != 6:
                phase = AlloyPhase(
                    names=phase_names,
                    chemical_formula=chemical_formula,
                    compositions=compositions,
                    table = {'number': table_no, 'caption': caption})

            data.append({
                'labels': [chemical_formula], 
                'value': compositions if i == 6 else phase})

    pickle.dump(data, open(output_name, 'w'))


for fn in ifiles():
    conver_file(fn)

