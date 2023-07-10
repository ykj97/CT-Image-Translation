#  Patient number - planning wise
import os
import sys
from tabulate import tabulate

base_path = './'

one_matched = []
multiple = []
no_matched = []
patients = {"Patient num":[], "Match":[], "Diag_path":[]}

for num in range(0,309):
    plan_path = os.path.join(base_path, 'planning')
    return_plan = os.path.join(plan_path, os.listdir(plan_path)[num])
    patient_num = return_plan.split('_')[-1]

    patients["Patient num"].append(patient_num)

    diag_path = os.path.join(base_path, 'diagnostic')
    return_diag = list(filter(lambda x: patient_num in x, os.listdir(diag_path)))
    
    if(len(return_diag) > 1): 
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



print("One matched : %d | Multiple matched : %d | No Matched : %d " 
      %(len(one_matched),len(multiple), len(no_matched)))

print(tabulate(patients, headers="keys"))
