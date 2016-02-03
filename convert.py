#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import *
from collections import defaultdict

def conver_file(file_name):
    data = []
    headings = []
    phases = []
    name, ext = os.path.splitext(file_name)
    output_name = name + ".p"
    output_json = name + ".json"
    affiliations = []
    processes = defaultdict(lambda: [])

    rows = list(irows(file_name))
    all_ids = []
    # Replace IDs value with the list of IDs 
    # and collect the full list of all IDs in the doc
    for row in rows[1:]:
        # list IDs:
        ids = [id_.strip() for id_ in row[0].split(',')]
        row[0] = ids
        all_ids.extend([id_ for id_ in ids if id_.lower() != "all"])
    all_ids = set(all_ids)

    if verbose:
        print "*** IDs in the file:",  all_ids

    for i, row in enumerate(rows):
        if i == 0:
            header = row
            if not (header[:5] == ["ID", "Type", "Name", "Value", "Units"]):
                print "*** Unexpeced header:", header
            
        else:
            ids, obj_type, name, value, units = row[:5]
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
                    obj = Alloy()
                    if name.lower() == "chemical formula":
                        obj.chemical_formula = value

                elif obj_type == "processing":
                    step = ProcessStep(
                            details=Value(
                                scalars = [Value(
                                    name='Processing',
                                    scalars=value)]
                                    + properties))
                    if id_.lower() == "all":
                        for id__ in ids:
                            processes[id__].append(step)
                    else:
                        processes[id_].append(step)

                elif obj_type == "property":
                    obj = Property(
                        name = name,
                        scalars = value,
                        units = units,
                        conditions = properties)

                elif obj_type == "reference":
                    if name.lower() == "doi":
                        obj = Reference(
                            doi = value)
                    elif name.lower() == "affiliation" or "institution":
                        affiliations.append(value)
                        continue

                elif obj_type == "phase":
                    obj = AlloyPhase(
                            names = value,
                            chemical_formula = value,
                            properties = properties)

                if obj_type in ["alloy", "phase"]:
                    obj.properties = properties

                # "Processing" gets added at the end:
                if obj_type != "processing":
                    data.append({'labels':[id_], 'value': obj})

    # Add "Processing":
    for id_, steps in processes.items():
        data.append({'labels':[id_], 'value': steps})

    data.append({'labels':['all'], 'value': Reference(affiliation=affiliations)})
    pickle.dump(data, open(output_name, 'w'))
    pif.dump(data, open(output_json, 'w'),indent=4)


for fn in ifiles(files="*.xlsx"):
    conver_file(fn)

