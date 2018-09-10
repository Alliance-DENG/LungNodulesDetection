import csv

#annotations is a Dict in Dict, with string
def load_annotation(path):
	csv_file = csv.reader(open(path, 'r'))
	annotations = []
	for line in csv_file:
		annotations.append(line)
	return annotations	
