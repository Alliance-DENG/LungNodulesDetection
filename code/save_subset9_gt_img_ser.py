import numpy as np
import pickle
from glob import glob
import SimpleITK as sitk
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

if __name__ == "__main__":
    mhd_path = "/home/grains2/alliance/DATA/subset9/"
    gt_path = "/home/grains2/alliance/DATA/CSVFILES/"
    pic_save_path = mhd_path+'gt/'
    CT_parameter_filename = '/home/grains2/alliance/keras-frcnn/parameter_for_CTs.dict'


    # read all the png file into a list (with abslute path)
    file_list = []
    file_list += glob(mhd_path + '*.mhd')
    print("num of files:%d" % len(file_list))

    # read csv file
    nodules = pd.read_csv(gt_path+"annotations.csv")

    with open(CT_parameter_filename, 'rb') as f_in:
        CT_parameter = pickle.load(f_in)

    # sort out the file that avaible
    for each_file in file_list:
        # parse the file_list, keep the name only
        # remove .mhd and 
        name = os.path.splitext(each_file)[0].split('/')[-1]

        # check wheather csv has mark this file
        sorted_df = nodules[nodules['seriesuid'] == name]
        
        origin, spacing = CT_parameter[name][0], CT_parameter[name][1]

        # 以i_z为key建一个dict
        gt_dict={}
        # 该文件下有gt
        for idx in range(len(sorted_df)):
            node_x = sorted_df["coordX"].values[idx]
            node_y = sorted_df["coordY"].values[idx]
            node_z = sorted_df["coordZ"].values[idx]
            diam = sorted_df["diameter_mm"].values[idx]
            # cal the voxel coordinate
            center = np.array([node_z,node_y,node_x]) 
            nodules_center_voxel = np.rint(np.absolute(center-origin)/spacing).astype(np.int16)
            # cut the slice
            width_half = int(diam / spacing[1] / 2 + 0.999)
            i_z, i_y, i_x = nodules_center_voxel
            x1, x2, y1, y2 = int(i_x-width_half), int(i_x+width_half), int(i_y-width_half), int(i_y+width_half)
            # 将对应的坐标保存到gt_dict里
            if i_z not in gt_dict:
                gt_dict[i_z] = []
            gt_dict[i_z].append([x1, x2, y1, y2])
        # 画出gt
        CT_array, _, _ = load_itk(each_file)
        for img_z in gt_dict:
            img = CT_array[img_z,:,:]
            img = normalizePlanes(img)
            img = (img*255).astype(np.uint8)
            img = np.stack((img,)*3, -1)
            for each_box in gt_dict[img_z]:
                cv2.rectangle(img,(each_box[0], each_box[2]), (each_box[1], each_box[3]), (0,255,0),1)
            cv2.imwrite(pic_save_path+name+'_'+str(img_z)+'_gt.png',img)

        del sorted_df, CT_array








   
                
                




