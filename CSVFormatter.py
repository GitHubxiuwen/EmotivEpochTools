"""
    Copyright 2016 Joshua Zosky
    joshua.e.zosky@gmail.com

    This file is part of "Emotiv Epoch Tools".
    "Emotiv Epoch Tools" is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    "Emotiv Epoch Tools" is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with "Emotiv Epoch Tools".  If not, see <http://www.gnu.org/licenses/>.

    Reorganize Emotiv EEG files using their Metadata header.

    Step 1)
    Get Metadata from CSV file.

    Metadata order:
    Column 1 = File title
    Column 2 = Date of recording
    Column 3 = Sampling Rate
    Column 4 = Subject #
    Column 5 = Data Labels
    Column 6 = Number of Columns in Dataset
    Column 7 = 'units:emotiv' (unsure what this is for)

    Step 2)
    Save Metadata to separate file.

    Step 3)
    Replace CSV header with the Data Labels.

    Step 4)
    Save files to separate folders with new names based on
        Subject ID # and date/time of recording.
"""

import csv
import os
import sys

list_of_csvs = []
counter = 0
print "Opening Input Folder\n==================="
for root, subdirs, files in os.walk('Input'):
    for filename in files:
        if filename.lower().endswith('.csv'):
            list_of_csvs.append(filename)
            counter += 1
            sys.stdout.write("There are %d files \r" % counter)
            sys.stdout.flush()
    print '\n'
    print list_of_csvs

print "\nConverting Files\n==================="
completed_counter = 0
for single_file in list_of_csvs:
    sys.stdout.write("\r%s Files completed: %d/%d    " % (single_file, completed_counter, counter))
    sys.stdout.flush()
    with open('Input/%s' % single_file) as open_file:
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

    header_filename = 'Subject %s %s.csv' % (csv_dictionary['subject'], csv_dictionary['recorded'])

    with open('Output/Info/%s' % header_filename, 'w+') as out_file:
        writer = csv.DictWriter(out_file, fieldnames=field_names)
        writer.writeheader()
        writer.writerow(csv_dictionary)

    new_header = csv_dictionary['labels'].split()

    with open('Input/%s' % single_file) as in_file:
        data = csv.reader(in_file)
        data.next()

        with open('Output/Data/%s' % header_filename, 'w+') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(new_header)
            writer.writerows(data)
    completed_counter += 1

sys.stdout.write("\rCompleted converting %d files                                         \n" % counter)