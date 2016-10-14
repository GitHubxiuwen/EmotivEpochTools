"""
Get Metadata from CSV file

Metadata order:
Column 1 = File title
Column 2 = Date of recording
Column 3 = Sampling Rate
Column 4 = Subject #
Column 5 = Data Labels
Column 6 = Number of Columns in Dataset
Column 7 = 'units:emotiv' (unsure what this is for)

"""

import csv

single_file1 = 'SampleCSV.csv'
single_file2 = 'SampleCSV2.csv'

with open(single_file1) as open_file:
    csv_object = csv.reader(open_file, delimiter=',')
    csv_metadata = csv_object.next()

csv_metadata = [item.strip(' ') for item in csv_metadata]
csv_dictionary = {}
for item in csv_metadata:
    if ':' in item:
        item_split = item.split(':')
        item_key = item_split[0]
        item_value = item_split[1]
        csv_dictionary[item_key] = item_value

field_names = [
    'title',
    'recorded',
    'sampling',
    'subject',
    'labels',
    'chan',
    'units'
]

header_filename = 'Subject %s %s - header.csv' % (csv_dictionary['subject'], csv_dictionary['recorded'])

with open(header_filename, 'w') as out_file:
    writer = csv.DictWriter(out_file, fieldnames=field_names)
    writer.writeheader()
    writer.writerow(csv_dictionary)

new_header = csv_dictionary['labels'].split()

with open(single_file1) as in_file:
    #in_file.next()
    data = csv.reader(in_file)
    data.next()

    with open(single_file2, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(new_header)
        writer.writerows(data)