#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import *

def conver_file(file_name):
    data = []
    headings = []
    phases = []
    name, ext = os.path.splitext(file_name)
    output_name = name + ".p"
    affiliations = []

    rows = list(irows(file_name))
    for i, row in enumerate(rows):
        if i == 0:
            header = row
            if not (header[:5] == ["ID", "Type", "Name", "Value", "Units"]):
                print "*** Unexpeced header:", header
            
        else:
            ids, obj_type, name, value, units = row[:5]
            ids = [id_.strip() for id_ in row[0].split(',')]
            obj_type = obj_type.lower()

            properties = []
            for i in xrange(5, len(row), 3):
                if row[i] == '':
                    break
                properties.append(Property(
                    name = row[i],
                    scalars = row[i+1],
                    units = row[i+2]))

            for id_ in ids:
                if obj_type == "alloy":
                    obj = Alloy(
                            names = value,
                            chemical_formula = value,
                            properties = properties)

                elif obj_type == "processing":
                    obj = ProcessStep(
                            details=Value(
                                name = value,
                                scalars = properties))

                elif obj_type == "propery":
                    obj = Property(
                        name = name,
                        scalars = value,
                        units = units)

                elif obj_type == "reference":
                    if name.lower() == "doi":
                        obj = Reference()
                        obj.doi = value
                    elif name.lower() == "affiliation":
                        affiliations.append(value)
                        continue  ## TODO

                elif obj_type == "phase":
                    obj = AlloyPhase(
                            names = value,
                            chemical_formula = value,
                            properties = properties)

                if obj_type in ["alloy", "phase"]:
                    obj.properties = properties

                data.append({'labels':[id_], 'value': obj})

    pickle.dump(data, open(output_name, 'w'))

for fn in ifiles(files="*.xlsx"):
    conver_file(fn)

