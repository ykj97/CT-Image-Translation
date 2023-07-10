import sys
import os
import SimpleITK as sitk
import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np
import cv2
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import mean_squared_error as mse
from skimage.metrics import normalized_root_mse as nrmse
import csv
import pandas as pd

def command_iteration(method):
    if method.GetOptimizerIteration() == 0:
        print("Estimated Scales: ", method.GetOptimizerScales())
    print(
        f"{method.GetOptimizerIteration():3} "
        + f"= {method.GetMetricValue():7.5f} "
        + f": {method.GetOptimizerPosition()}"
    )


def calculate_accuracy(fixed_arr, moving_arr, out_arr):
    ssim_val = ssim(fixed_arr, out_arr, data_range=fixed_arr.max() - fixed_arr.min())
    nrmse_val = nrmse(fixed_arr, out_arr)
    return ssim_val, nrmse_val


def multi_scan(base_path, num):
    diag_list = []

    plan_path = os.path.join(base_path, 'planning')
    patient_num = str(num)

    return_plan = list(filter(lambda x: patient_num in x, os.listdir(plan_path)))
    return_plan = os.path.join(plan_path, str(return_plan[0]))
    return_plan = os.path.join(return_plan, 'CT', 'CT.nii.gz')

    diag_path = os.path.join(base_path, 'diagnostic')
    return_diag = list(filter(lambda x: patient_num in x, os.listdir(diag_path)))

    for i in range(len(return_diag)):
        diag = os.path.join(diag_path, return_diag[i], 'CT', 'CT.nii.gz')
        diag_list.append(diag)

    return return_plan, diag_list, patient_num


def remove_background(img):
    return sitk.Clamp(img, lowerBound=-1000)


base_path = './'
csv_file_path = './map'

one_matched = []
multiple = []
no_matched = []
patients = {"Patient num": [], "Match": [], "Diag_path": []}

delete_file_list = []
delete_file_path = os.path.join(csv_file_path, 'delete_file.csv')

for num in range(0, 309):
    plan_path = os.path.join(base_path, 'planning')
    return_plan = os.path.join(plan_path, os.listdir(plan_path)[num])
    patient_num = return_plan.split('_')[-1]

    patients['Patient num'].append(patient_num)

    diag_path = os.path.join(base_path, 'diagnostic')
    return_diag = list(filter(lambda x: patient_num in x, os.listdir(diag_path)))

    if len(return_diag) > 1:
        multiple.append(patient_num)
        patients["Match"].append("Multiple Patients")
        patients["Diag_path"].append(return_diag)
    elif len(return_diag) == 0:
        no_matched.append(patient_num)
        patients["Match"].append("No Matched Patients")
        patients["Diag_path"].append("none")
    else:
        one_matched.append(patient_num)
        patients["Match"].append("One Matched Patients")
        patients["Diag_path"].append(return_diag)

num_list = multiple

for itr in range(0, len(num_list)):
    num_itr = num_list[itr]
    plan_path, diag_path, patient_num = multi_scan(base_path, num_itr)

    for i, scans in enumerate(diag_path):
        main_path = './'

        print("Patient # : %s" % patient_num, end='\n')
        print("Diagnostic path : %s" % scans)

        if len(plan_path) < 1: continue

        fixed = sitk.ReadImage(plan_path, sitk.sitkFloat32)
        moving = sitk.ReadImage(scans, sitk.sitkFloat32)

        fixed = remove_background(fixed)
        moving = remove_background(moving)

        R = sitk.ImageRegistrationMethod()

        R.SetMetricAsCorrelation()

        R.SetOptimizerAsRegularStepGradientDescent(
            learningRate=2.0,
            minStep=1e-4,
            numberOfIterations=1000,
            gradientMagnitudeTolerance=1e-8,
        )
        R.SetOptimizerScalesFromIndexShift()

        tx = sitk.CenteredTransformInitializer(
            fixed, moving, sitk.Similarity3DTransform()
        )
        R.SetInitialTransform(tx)

        R.SetInterpolator(sitk.sitkLinear)

        R.AddCommand(sitk.sitkIterationEvent, lambda: command_iteration(R))

        print("Execution start")
        outTx = R.Execute(fixed, moving)

        print("-------")
        print(outTx)
        print(f"Optimizer stop condition: {R.GetOptimizerStopConditionDescription()}")
        print(f" Iteration: {R.GetOptimizerIteration()}")
        print(f" Metric value: {R.GetMetricValue()}")

        resampler = sitk.ResampleImageFilter()
        resampler.SetReferenceImage(fixed)
        resampler.SetInterpolator(sitk.sitkLinear)
        resampler.SetDefaultPixelValue(-1000) 
        resampler.SetTransform(outTx)

        out = resampler.Execute(moving)
        
        fixed_arr = sitk.GetArrayFromImage(fixed)
        moving_arr = sitk.GetArrayFromImage(moving)
        out_arr = sitk.GetArrayFromImage(out)

        ssim_val, nrmse_val = calculate_accuracy(fixed_arr, moving_arr, out_arr)
        
        print(f"SSIM: {ssim_val:.4f}")
        print(f"NRMSE: {nrmse_val:.4f}")
        
        if nrmse_val <= 0.5:
            writer = sitk.ImageFileWriter()
            writer.SetFileName('/cluster/home/t122378uhn/map/' + diag_path[i].split('/')[7] + '_fixed_image.nii.gz')
            writer.Execute(fixed)

            writer_2 = sitk.ImageFileWriter()
            writer_2.SetFileName('/cluster/home/t122378uhn/map/' + diag_path[i].split('/')[7] + '_moving_image.nii.gz')
            writer_2.Execute(moving)

            writer_3 = sitk.ImageFileWriter()
            writer_3.SetFileName('/cluster/home/t122378uhn/map/' + diag_path[i].split('/')[7] + '_out_image.nii.gz')
            writer_3.Execute(out)
                

        else:
            print("Delete this file! | path : %s" %scans)
            delete_file_list.append(scans)

print(delete_file_list)

with open(delete_file_path, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows(delete_file_list)

df = pd.DataFrame(delete_file_list)
df.to_csv("./map/delete_file_path_1.csv")