import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
import pandas as pd

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

def get_filename(case):
    global file_list
    for f in file_list:
        if case in f:
            return(f)

if __name__ == "__main__":
    data_path = "subset0\\"
    #read all the mhd filename into a dict
    file_list = glob(data_path + r"\*.mhd")

    # read csv file
    gt_path = "D:\\LUNA16\\CSVFILES\\"
    nodules = pd.read_csv(gt_path+"annotations.csv")
    # use get_filename to pick file that avaiable
    nodules["file"] = nodules["seriesuid"].apply(get_filename)
    # drop those unavaiable filename, keep the filename with nodules
    nodules = nodules.dropna()
    # sum all the slices into this array, then divide it by the count
    array_sum = np.zeros((512,512))
    sum_count = 0

    for img_file in file_list:
        # get all nodules associate with each file(not all the file has nodule)
        nodules4perCT = nodules[nodules["file"]==img_file] 
        # some files may not have a nodule--skipping those 
        if len(nodules4perCT)>0:     
            # load the CT as a img array, the cordinator is order in z,y,x
            CT_array, origin, spacing = load_itk(img_file)
            # make a set to store the index of useful slice
            slice_with_nodule = set()
            # find out which slice contain nodules
            for idx in range(0, len(nodules4perCT)):
                node_z = nodules4perCT["coordZ"].values[idx]
                slice_z = int((node_z - origin[0]) / spacing[0] + 0.5)
                assert slice_z >= 0
                slice_with_nodule.add(slice_z)
            # sum the grey value of these slice
            for each in slice_with_nodule:
                array_sum += normalizePlanes(CT_array[each, :, :])
                sum_count += 1
    mean_grey = array_sum / sum_count
    print(sum_count)
    # save the result
    np.save('D:\\LUNA16\\annotation_mean', mean_grey)

                
                




