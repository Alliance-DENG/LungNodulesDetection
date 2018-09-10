import numpy as np
from glob import glob
import cv2
import os

if __name__ == "__main__":
    data_path = "/home/guest/alliance/LUNA16/bbox/"
    #read all the mhd filename into a dict
    file_list = glob(data_path + r"*.npy")
    print("num of array:{}".format(len(file_list)))
    for each in file_list:
        img_grey = np.load(each)
        img_grey = img_grey * 255
        #img_grey = img_grey.astype(np.uint8)
        img_rgb = np.stack((img_grey,)*3, -1)

        filename = os.path.splitext(each)[0]
        cv2.imwrite(filename+'.png', img_rgb)


