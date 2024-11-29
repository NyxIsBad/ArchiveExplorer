import regex as re
import csv
from collections import defaultdict
from functools import reduce
from get_archive import sum_sentences

def get_category(sentence):
    match = re.match(r"([a-zA-Z\s]+)([+-]?\d+[%]?)(.*)", sentence)
    if not match:
        return None
    start, center, rest = match.groups()
    if '%' in center:
        return f"{start}x%{rest}"
    else:
        return f"{start}x{rest}"
"""
def sum_sentences(a, b):
    print("Summing", a, b)
    # Extract the common part of the sentence (e.g., "Damage of Lightning Skills")
    match_a = re.match(r"([a-zA-Z\s]+)([+-]?\d+[%]?)(.*)", a)
    match_b = re.match(r"([a-zA-Z\s]+)([+-]?\d+[%]?)(.*)", b)

    if not match_a or not match_b:
        return "Invalid input format"

    # Extract the sentence and percentage values
    start_a, value_a, rest_a = match_a.groups()
    start_b, value_b, rest_b = match_b.groups()

    # Check if the part of the sentences match
    if start_a == start_b and rest_a == rest_b:
        # Sum the percentages
        if value_a[-1] == "%":
            value_a_int = int(value_a[:-1])
            value_b_int = int(value_b[:-1])
        else:
            value_a_int = int(value_a)
            value_b_int = int(value_b)
        total = value_a_int + value_b_int
        if total < 0:
            # Return sum and category
            return f"{start_a}{total}%{rest_a}"
        else:
            return f"{start_a}+{total}%{rest_a}"
    else:
        # Return both sentences if they don't match
        print("None returned")
        return None"""

# Sort the sentences by the common part
data_cleaned = []
with open('eidolon_archive_cleaned.csv', mode='r', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter='|')
    # skip the header 
    header = next(reader)
    for row in reader:
        # replace all "," with ", " for readability
        names = ', '.join(row[0].split(','))
        data_cleaned.append([names, row[1]])
    data_cleaned = sorted(data_cleaned, key=lambda x: x[1])

# Write to new csv in order
with open('eidolon_archive_sorted.csv', mode='w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file, delimiter='|')
    writer.writerow(header)
    for row in data_cleaned:
        writer.writerow(row)
print("Data sorted successfully")

# Read the sorted data
data_sorted = []
with open('eidolon_archive_sorted.csv', mode='r', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter='|')
    header = next(reader)
    for row in reader:
        if "," in row[1]:
            attribs = row[1].split(",")
            attribs = [attrib.strip() for attrib in attribs]
        else:
            attribs = [row[1]]
        data_sorted += attribs

data_dict = defaultdict(list)
for attrib in data_sorted:
    data_dict[get_category(attrib)].append(attrib)

# Sum the sentences
data_summed = defaultdict(str)
for category, attribs in data_dict.items():
    # fold over attribs
    print(category, attribs)
    summed = reduce(sum_sentences, attribs)
    if summed:
        data_summed[category] = summed

# Write data_summed to a txt file
with open('eidolon_archive_totals.txt', mode='w', encoding='utf-8') as file:
    for category, total in data_summed.items():
        file.write(f"{category}: {total}\n")