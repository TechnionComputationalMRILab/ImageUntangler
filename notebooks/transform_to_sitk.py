# %%
import SimpleITK as sitk
import json
import numpy as np
from glob import glob
from pathlib import Path
import matplotlib.pyplot as plt

# %%
CASE_PATH = r'C:\Users\ang.a\OneDrive - Technion\Documents\MRI_Data\cases_for_rotem\99'
ANNOTATION_DATA = r'C:\Users\ang.a\OneDrive - Technion\Documents\MRI_Data\cases_for_rotem\99\data\24.11.2021__13_53..annotation.json'

# %%
# open and read the annotation data
with open(ANNOTATION_DATA, 'r') as f: 
    annotation_points = json.load(f)
    data = annotation_points['MPR points']

data = np.array(data)
data[-1] 

# %%
# transform the DICOM folder to a numpy array
reader = sitk.ImageSeriesReader()
dicom_names = reader.GetGDCMSeriesFileNames(CASE_PATH)
reader.SetFileNames(dicom_names)
image = reader.Execute()
nda = sitk.GetArrayFromImage(image)

nda = np.flipud(nda)
nda = np.reshape(nda, nda.shape, order='F')

# %%
x_num = image.GetSize()[0]
xi = image.TransformIndexToPhysicalPoint([0,0,0])[0]
xf = image.TransformIndexToPhysicalPoint([x_num-1,x_num-1,0])[0]

y_num = image.GetSize()[1]
yi = image.TransformIndexToPhysicalPoint([0,0,0])[1]
yf = image.TransformIndexToPhysicalPoint([y_num-1,y_num-1,0])[1]

x_translate = ((np.abs(xi)+np.abs(xf))/2) - np.abs(image.GetOrigin()[0])
y_translate = ((np.abs(yi)+np.abs(yf))/2) - np.abs(image.GetOrigin()[1])

# %%
# get the slice indices that have annotations...
indices = [image.TransformPhysicalPointToIndex((0,0,z))[2] for z in np.unique(data[:,2])]
print(indices)

indices = list(range(indices[0], indices[-1]+1))
print(indices)

# %%
# convert the last coordinate to the slice index
data_copy = np.copy(data)

for i in data_copy:
    i[2] = image.TransformPhysicalPointToIndex((0,0,i[2]))[2]

# %%
i = 47
pt = (data[0])
size = image.GetSize()

plt.figure(figsize=(15,15))
plt.imshow(nda[i,:,:], extent=[xi,xf,yi,yf])
plt.plot(pt[0]+x_translate, pt[1]+y_translate, 'ro')

# %%
# show all slices
fig, axs = plt.subplots(ncols=4, nrows=4, figsize=(50,50))

axs = np.ravel(axs)

for idx, i in enumerate(indices):
    axs[idx].set_title(f'SliceIdx: {i}')
    axs[idx].imshow(nda[i,:,:], extent=[xi,xf,yi,yf])

    for pt in data_copy:
        if pt[2] == i:
            axs[idx].plot(pt[0]+x_translate, pt[1]+y_translate, 'ro')
plt.tight_layout()



