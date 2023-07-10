
# %% Check fixed, moving, registered img
#  Coronal, axial, sagittal overlay
import nibabel as nib
import matplotlib.pyplot as plt
import cv2
import numpy as np


def plot_img(img, i):
    rotated_img = cv2.rotate(img[:,:,i], cv2.ROTATE_90_CLOCKWISE)
    plt.imshow(rotated_img, cmap='gray')
    plt.axis('off')



rows = 1; cols = 3
axes=[]; fig = plt.figure(figsize=(15, 6))

def add_img(img, title, index):
    axes.append(fig.add_subplot(rows, cols, index))
    axes[-1].set_title(title)
    axes[-1].axis('off')
    if index!=3: plt.imshow(img, cmap='gray')
    else: plt.imshow(img, cmap='Blues')



def overlap_imgs(fixed_img, registered_img, slice_num):

    fixed = cv2.rotate(fixed_img[:,:,slice_num], cv2.ROTATE_90_CLOCKWISE)
    registered = cv2.rotate(registered_img[:,:,slice_num], cv2.ROTATE_90_CLOCKWISE)
 
    overlap_img = cv2.addWeighted(fixed,1,registered,1,0)

    plt.imshow(overlap_img, cmap='Blues')
    plt.axis('off')

    return

ref_rows = 2; ref_cols = 3
ref_axes=[]; ref_fig = plt.figure(figsize=(15, 10))

def add_ref_img(img, title, index):
    img = cv2.resize(img, dsize=(499, 499), interpolation=cv2.INTER_CUBIC)
    ref_axes.append(ref_fig.add_subplot(ref_rows, ref_cols, index))
    ref_axes[-1].set_title(title)
    ref_axes[-1].axis('off')
		
		# Image Flip (Vertical)
    plt.imshow(np.flip(img, 0), cmap='gray')

def resize_coronal(img):
    img = cv2.resize(img, dsize=(466, 466), interpolation=cv2.INTER_CUBIC)
    img = cv2.rotate(img, cv2.ROTATE_180)
    return img

def resize_sagittal(img):
    img = cv2.resize(img, dsize=(466, 466), interpolation=cv2.INTER_CUBIC)
    img = cv2.flip(img, 0)
    return img

def resize_axial(img):
    img = cv2.resize(img, dsize=(466, 466), interpolation=cv2.INTER_CUBIC)
    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    return img

def nii_to_arr(path):
    nii_img = nib.load(path)
    arr_img = np.array(nii.img.dataobj)
    return arr_img



fixed_path = '/cluster/home/t122378uhn/map/263_2958605722_fixed_image.nii.gz'
registered_path = '/cluster/home/t122378uhn/map/263_2958605722_out_image.nii.gz'
moving_path = '/cluster/home/t122378uhn/map/263_2958605722_moving_image.nii.gz'



fixed = nii_to_arr(fixed_path)
registered = nii_to_arr(registered_path)
moving = nii_to_arr(moving_path)

slice_sagittal = 251
slice_coronal = 260
slice_axial = 90

axial_f  = fixed[:, :, slice_axial]
axial_f = resize_axial(axial_f)
axial_r  = registered[:, :, slice_axial]
axial_r = resize_axial(axial_r)

plt.subplot(1,3,1)
plt.title("axial", fontsize=20)
plt.imshow(axial_f, cmap='Blues')
plt.imshow(axial_r, cmap='RdPu', alpha=0.4)
plt.axis('off')


sagittal_f  = fixed[slice_sagittal, :, :].T
sagittal_f = resize_sagittal(sagittal_f)
sagittal_r  = registered[slice_sagittal, :, :].T
sagittal_r = resize_sagittal(sagittal_r)

plt.subplot(1,3,2)
plt.title("sagittal", fontsize=20)
plt.imshow(sagittal_f, cmap='Blues')
plt.imshow(sagittal_r, cmap='RdPu', alpha=0.4)
plt.axis('off')


coronal_f = fixed[:, slice_coronal, :].T
coronal_f = resize_coronal(coronal_f)
coronal_r = registered[:, slice_coronal, :].T
coronal_r = resize_coronal(coronal_r)

plt.subplot(1,3,3)
plt.title("coronal", fontsize=20)
plt.imshow(coronal_f, cmap='Blues')
plt.imshow(coronal_r, cmap='RdPu', alpha=0.4)
plt.axis('off')
plt.tight_layout()

