from glob import glob
import os

# parse the file_list, keep the name only
def parse_filename(filename):
    # remove .mhd
    filename = os.path.splitext(filename)[0]
    # remove path
    i = len(filename) - 1
    while i >= 0:
        if filename[i] == '\\' or filename[i] == '/':
            break
        i -= 1
    return filename[int(i+1) :]


gt_path = '/home/guest/alliance/LUNA16/CSVFILES/'
data_path = '/home/guest/alliance/LUNA16/'

file_list = glob(data_path + 'subset9/*.mhd')

ff = open(gt_path+'annotations_val.csv', 'w')
ff.write('seriesuid,coordX,coordY,coordZ,diameter_mm\n')

filenames = []
for each in file_list:
    filename = parse_filename(each)
    filenames.append(filename)

with open(gt_path+'annotations.csv', 'r') as f:
    print('Parsing annotation files')

    print(file_list[0])
    print(filenames[0])

    for line in f:
        line_split = line.strip().split(',')
        (filename,x,y,z,d) = line_split
        #print(filename_)
        if filename in filenames:
            print(line)
            ff.write(line)

ff.close()