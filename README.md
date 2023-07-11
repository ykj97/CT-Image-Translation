# CT-Image-Translation
The aim of this project is to perform CT translation from diagnostic CT to planning CT for prostate cancer, specifically for clinical research.

## Data processing

  1.`clean_MRN.m` : This code is responsible for cleaning the DICOM private data by utilizing patient numbers.
  #
  2. The anonymized DICOM data is then processed into nii.gz format using Med-ImageTools.
  3. `patien_info.py` : Each patient have none, single, multiple CT scans. This code if for getting dataset information.
  4. `registration.py` : The code performs registration using simpelitk library. It facilitates the registration of multimodal CT images.
  5. `check_registration_result.py` : The code for checking the regstration result and calculating the accuracy. 
