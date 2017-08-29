import csv

def csv_reader(newzealandsocialbakers_data):
    reader = cev.reader(newzealandsocialbakers_data)
    for row in reader:
        row = str(row).split(':')[-2].split('"edit_tags')[0].split("',")[0]
        import pdb;pdb.set_trace()
