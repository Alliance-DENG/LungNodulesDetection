import numpy as np

def world2voxel(zyx_, origin, spacing):
    world_center = np.array(zyx_)
    z, y, x = np.rint(np.absolute(world_center-origin)/spacing)
    z, y, x = int(z), int(y), int(x)
    return (z, y, x)

def voxel2world(zyx_, origin, spacing):
    voxel = np.array(zyx_)
    world = voxel * spacing + origin
    z, y, x = world
    z, y, x = float(z), float(y), float(x)
    return (z, y, x)

import SimpleITK as sitk
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

ct_scan, origin, spacing = load_itk(r'D:\LUNA16\subset0\1.3.6.1.4.1.14519.5.2.1.6279.6001.105756658031515062000744821260.mhd')

x_real , y_real, z_real = 99.23049108, -4.882165437, -128.6913046
print((x_real, y_real, z_real))
voxel = world2voxel((x_real, y_real, z_real), origin, spacing)
print('world2voxel:',voxel)
print('voxel2world:', voxel2world(voxel, origin, spacing))
