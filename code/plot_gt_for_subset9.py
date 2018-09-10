#Lia想看有gt框而没被预测出的图片,
#下面是我的做法, 先保存所有有结点的原图. 再读gt文件, 找到对应的图加框

import SimpleITK as sitk
import numpy as np
from glob import glob
import pandas as pd
import os
import cv2

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
    data_path = "/home/grains2/alliance/DATA/"
    gt_path = "/home/grains2/alliance/FN_subset9/"
    bbox_path = "./gt_subset9/"

    with open(bbox_path+'bbox.txt', 'w') as f:

        # read all the mhd file into a list (with abslute path)
        file_list = []
        for i in range(9,10):
            file_list += glob(data_path + 'subset%s/*.mhd' % i)
        print("num of files:%d" % len(file_list))

        # read csv file
        nodules = pd.read_csv(gt_path+"annotations.csv")

        # sort out the file that avaible
        for each_file in file_list:
            # parse the file_list, keep the name only
            name = parse_filename(each_file)

            # check wheather csv has mark this file
            sorted_df = nodules[nodules['seriesuid'] == name]
            
            # go through this file
            slice_dict = []
            for idx in range(len(sorted_df)):
                # load the CT as a img array, the cordinator is order in z,y,x
                CT_array, origin, spacing = load_itk(each_file)

                node_x = sorted_df["coordX"].values[idx]
                node_y = sorted_df["coordY"].values[idx]
                node_z = sorted_df["coordZ"].values[idx]
                diam = sorted_df["diameter_mm"].values[idx]
                # cal the voxel coordinate
                center = np.array([node_z,node_y,node_x]) 
                nodules_center_voxel = np.rint(np.absolute(center-origin)/spacing)
                # cut the slice
                width_half = int(diam / spacing[1] / 2 + 0.999)
                i_z, i_y, i_x = nodules_center_voxel
                x1, x2, y1, y2 = int(i_x-width_half), int(i_x+width_half), int(i_y-width_half), int(i_y+width_half)
                # if it haven't been saved, save it
                if not i_z in slice_dict:
                    slice_dict.append(i_z)
                    tmp = normalizePlanes(CT_array[int(i_z),:,:])
                    tmp *= 255
                    tmp = tmp.astype(np.uint8)
                    cv2.imwrite('{}{}_{}.png'.format('./gt_subset9/', name, int(i_z), tmp)
                #del CT_array, origin, spacing
                #file_path = bbox_path + name + '_' + str(i_z)
                #f.write('{}.npy,{},{},{},{},{}\n'.format(file_path, x1, y1, x2, y2, 'positive'))


            #del sorted_df
