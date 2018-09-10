import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
import pandas as pd
import os

def load_itk(filename):
    # Reads the image using SimpleITK
    itkimage = sitk.ReadImage(filename)

    # Convert the image to a  numpy array first and then shuffle the dimensions to get axis in the order z,y,x
    ct_scan = sitk.GetArrayFromImage(itkimage)

    # Read the origin of the ct_scan, will be used to convert the coordinates from world to voxel and vice versa.
    origin = np.array(list(reversed(itkimage.GetOrigin())))

    # Read the spacing along each dimension
    spacing = np.array(list(reversed(itkimage.GetSpacing())))

    return ct_scan, origin, spacing

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
    data_path = "D:\\LUNA16\\subset0\\"
    gt_path = "D:\\LUNA16\\CSVFILES\\"

    sum_count = 0
    array_sum = np.zeros((512,512))

    # read all the mhd file into a dict (with abslute path)
    file_list = glob(data_path + r"\*.mhd")

    # read csv file
    nodules = pd.read_csv(gt_path+"candidates.csv")

    # sort out the file that avaible
    for each_file in file_list:
        # parse the file_list, keep the name only
        name = parse_filename(each_file)

        # check wheather csv has mark this file
        sorted_df = nodules[nodules['seriesuid'] == name]
        # take the Z column of sorted_df as pd.Series
        sorted_s = sorted_df['coordZ']

        Zcord_set = set()
        # go through this file
        if len(sorted_df) > 0:

            # load the CT as a img array, the cordinator is order in z,y,x
            CT_array, origin, spacing = load_itk(each_file)

            z_array = sorted_s.values
            for i in range(len(z_array)):
                node_z = z_array[i].item()
                slice_z = int((node_z - origin[0]) / spacing[0] + 0.5)
                assert slice_z >= 0
                Zcord_set.add(slice_z)

            # sum the grey value of these slice
            for each in Zcord_set:
                array_sum += normalizePlanes(CT_array[each, :, :])
                sum_count += 1
            
            del CT_array, origin, spacing

        del sorted_df, sorted_s

    np.save(data_path+'_sum_%s' % sum_count, array_sum)







   
                
                




