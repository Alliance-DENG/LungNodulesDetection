import SimpleITK as sitk
import numpy as np
from glob import glob
import pickle
import os

def load_itk(filename):
    # Reads the image using SimpleITK
    itkimage = sitk.ReadImage(filename)

    # Read the origin of the ct_scan, will be used to convert the coordinates from world to voxel and vice versa.
    origin = np.array(list(reversed(itkimage.GetOrigin())))

    # Read the spacing along each dimension
    spacing = np.array(list(reversed(itkimage.GetSpacing())))

    return origin, spacing

def normalizePlanes(npzarray):
    maxHU = 400.
    minHU = -1000.
 
    npzarray = (npzarray - minHU) / (maxHU - minHU)
    npzarray[npzarray>1] = 1.
    npzarray[npzarray<0] = 0.
    return npzarray

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

if __name__ == "__main__":
    data_path = "/home/guest/alliance/LUNA16/"
    gt_path = "/home/guest/alliance/LUNA16/CSVFILES/"
    bbox_path = "/home/guest/alliance/LUNA16/bbox/"

    # read all the mhd file into a list (with abslute path)
    file_list = []
    for i in range(10):
        file_list += glob(data_path + 'subset%s/*.mhd' % i)
    print("num of files:%d" % len(file_list))

    all_param = []

    for each_file in file_list:
        # parse the file_list, keep the name only
        name = parse_filename(each_file)

        origin, spacing = load_itk(each_file)

        tmp = []
        tmp.append(name)
        tmp.append(origin)
        tmp.append(spacing)

        all_param.append(tmp)

    # save the parameter
    
with open('parameter_for_CTs.pickle', 'wb') as para_f:
	pickle.dump(all_param,para_f)


    
    









   
                
                




