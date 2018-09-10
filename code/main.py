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

def get_filename(case):
    global file_list
    for f in file_list:
        if case in f:
            return(f)

if __name__ == "__main__":
    data_path = "D:\\LUNA16\\subset0\\"
    #read all the mhd filename into a dict
    file_list = glob(data_path + r"\*.mhd")

    # read csv file
    gt_path = "D:\\LUNA16\\CSVFILES\\"
    nodules = pd.read_csv(gt_path+"annotations.csv")
    # use get_filename to pick file that avaiable
    nodules["file"] = nodules["seriesuid"].apply(get_filename)
    # drop those unavaiable filename, keep the filename with nodules
    nodules = nodules.dropna()
    
    for img_file in file_list:
        print("Iterating the image file %s" % img_file.replace(data_path,""))
        # get all nodules associate with each file(not all the file has nodule)
        nodules4perCT = nodules[nodules["file"]==img_file] 
        # some files may not have a nodule--skipping those 
        if len(nodules4perCT)>0:     
            # load the CT as a img array, the cordinator is order in z,y,x
            CT_array, origin, spacing = load_itk(img_file)
            # plot each nodule per CT
            for idx in range(0, len(nodules4perCT)):
                node_x = nodules4perCT["coordX"].values[idx]
                node_y = nodules4perCT["coordY"].values[idx]
                node_z = nodules4perCT["coordZ"].values[idx]
                diam = nodules4perCT["diameter_mm"].values[idx]
                # assume the origin order in mhd file is z-y-x
                center = np.array([node_z,node_y,node_x]) 
                # get the nearest integer as the center cordinator, 
                # nodules_center_voxel[0] indicate the slice of the img_array
                nodules_center_voxel = np.rint(np.absolute(center-origin)/spacing)
                # cut the slice
                width_half = int(diam / spacing[1] / 2 + 0.999)
                i_z, i_y, i_x = nodules_center_voxel
                y1, y2, x1, x2 = int(i_y-width_half), int(i_y+width_half), int(i_x-width_half), int(i_x+width_half)
                nodule_patch = CT_array[int(i_z), y1:y2:1, x1:x2:1]
                # plot the slice
                plt.imshow(nodule_patch, cmap='Greys')
                plt.show()
                # save the image
                




