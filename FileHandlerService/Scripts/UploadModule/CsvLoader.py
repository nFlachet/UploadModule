import csv
import json


def loadAsJson(csvFile):
    json_data = {"type": "FeatureCollection"}
    feature_list = []

    lines = csvFile.splitlines()
    csv_rows = csv.reader(lines, delimiter=';')

    # case id parameter
    caseid_row = next(csv_rows)
    if caseid_row[0] != 'Case_ID':
        print 'WARNING check if case id is correctly set'
    json_data['caseId'] = caseid_row[1]

    # variant id parameter
    variantid_row = next(csv_rows)
    if variantid_row[0] !='Variant_ID':
        print 'WARNING check if variant id is correctly set'
    json_data['variantId'] = variantid_row[1]

    # type id parameter
    typeid_row = next(csv_rows)
    if typeid_row[0] != 'Type':
        print 'WARNING check if type id is correctly set'
    json_data['gml_type'] = typeid_row[1]

    keys_values = next(csv_rows)

    for row in csv_rows:
        feature_dict = {"type": "Feature"}
        properties_dict = {}
        for key, val in zip(keys_values, row):
            if key == 'geometry':
                feature_dict["geometry"] = val
            else:
                properties_dict[key] = val

        feature_dict["properties"] = properties_dict
        feature_list.append(feature_dict)

    json_data['features'] = feature_list
    return json_data
