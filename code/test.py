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


    mean_grey = np.zeros((512,512))
    np.save('D:\\mean_pixel', mean_grey)

                
                




