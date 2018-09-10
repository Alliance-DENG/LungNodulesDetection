import numpy as np
import pickle
from glob import glob
import pandas as pd
import os
import cv2

if __name__ == "__main__":
    img_path = "C:\\Users\\Alliance\\Desktop\\results-imgs\\"
    gt_path = "D:\\LUNA16\\CSVFILES\\"
    pic_save_path = img_path+'gt\\'
    CT_parameter_filename = 'D:\\LUNA16\\parameter_for_CTs.dict'


    # read all the png file into a list (with abslute path)
    file_list = []
    file_list += glob(img_path + '*.png')
    print("num of files:%d" % len(file_list))

    # read csv file
    nodules = pd.read_csv(gt_path+"annotations.csv")

    with open(CT_parameter_filename, 'rb') as f_in:
        CT_parameter = pickle.load(f_in)

    # sort out the file that avaible
    for each_file in file_list:
        # parse the file_list, keep the name only
        name = each_file.split('\\')[-1].split('_')[0]
        img_z = int(each_file.split('\\')[-1].split('_')[1].split('.')[0])

        # check wheather csv has mark this file
        sorted_df = nodules[nodules['seriesuid'] == name]
        
        img = cv2.imread(each_file)
        origin, spacing = CT_parameter[name][0], CT_parameter[name][1]

        Plot_gt = False

        for idx in range(len(sorted_df)):
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

            if(abs(i_z-img_z)<1):
                cv2.rectangle(img,(x1, y1), (x2, y2), (0,255,0),1)
                Plot_gt = True
        if(Plot_gt):
            cv2.imwrite(pic_save_path+name+'_'+str(img_z)+'_gt.png',img)

            
        del sorted_df








   
                
                




