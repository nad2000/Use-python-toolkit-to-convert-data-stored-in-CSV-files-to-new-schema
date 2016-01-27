#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import *

def conver_file(file_name):
    data = []
    headings = []
    alloys = []
    name, ext = os.path.splitext(file_name)
    output_name = name + ".p"

    for i, row in enumerate(irows(file_name)):
        if i == 0:
            table_no = row[0].lower().replace('table','').replace(' ','')
        elif i == 1:
            caption = row[0]
        elif i == 2:
            headings = [h.split('(')[0].strip() for h in row]
            if verbose:
                print "Headings:", headings
        elif i == 3:
            units = [u.strip(" ()") for u in row]
            if verbose:
                print "Units:", units
            if row[1] != '':
                headings[1] += ' ' + row[1]
        else:
            if row[0] <> '':
                chemical_formula = row[0]


            alloy = Alloy(
                ids = chemical_formula, 
                chemical_formula = chemical_formula) 

            properties = []
            method = Method(name=row[1])
            for k in range(2,4):
                prop = Property(name=headings[k])
                prop.scalars = row[k]
                prop.method = method
                properties.append(prop)

            alloy.properties = properties
            alloy.table = {'number':table_no, 'caption':caption}

            data.append({'labels':[chemical_formula], 'value':alloy})

    pickle.dump(data, open(output_name, 'w'))


for fn in ifiles():
    conver_file(fn)

