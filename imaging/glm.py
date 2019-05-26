import numpy as np
import matplotlib.pyplot as plt
import os
import requests
import zipfile
import pandas as pd
import nibabel

"""
Generalized linear model (GLM general) for fMRI.
"""

# Define the URL of the data and download it using the Requests libary
url = "http://www.fil.ion.ucl.ac.uk/spm/download/data/MoAEpilot/MoAEpilot.zip"
data = requests.get(url)

# Check if the targed folder for storing the data already exists. If not create it and save the zip file.
if os.path.exists("./fMRI_data") == False:
    os.mkdir("fMRI_data")
    
open("./fMRI_data/data.zip", "wb").write(data.content)

# Unzip the file
zip_ref = zipfile.ZipFile("./fMRI_data/data.zip", "r")
zip_ref.extractall("./fMRI_data/")
zip_ref.close()

# Find all files in the structural data folder
data_path = "./fMRI_data/sM00223/"
files = os.listdir(data_path)

# Read in the data
data_all = []
for data_file in files:
    if data_file[-3:] == "hdr":
        data = nibabel.load(data_path + data_file).get_data()

data = np.rot90(data.squeeze(), 1)

# Plot
fig, ax = plt.subplots(1, 6, figsize=[18, 3])

n = 0
slice = 0
for _ in range(6):
    ax[n].imshow(data[:, :, slice], 'gray')
    ax[n].set_xticks([])
    ax[n].set_yticks([])
    ax[n].set_title('Slice number: {}'.format(slice), color='r')
    n += 1
    slice += 10
    
fig.subplots_adjust(wspace=0, hspace=0)
plt.show()

# Basic information about the data acquisition
x_size = 64
y_size = 64
n_slice = 64
n_volumes = 96

# Find all files in the data folder
data_path = "./fMRI_data/fM00223/"
files = os.listdir(data_path)

# Read in the data and organize it with respect to the acquisition parameters
data_all = []
for data_file in files:
    if data_file[-3:] == "hdr":
        data = nibabel.load(data_path + data_file).get_data()        
        data_all.append(data.reshape(x_size, y_size, n_slice))

# Create a 3x6 subplot 
fig, ax = plt.subplots(3, 6, figsize=[18, 11])

# Organize the data for visualisation in the coronal plane
coronal = np.transpose(data_all, [1, 3, 2, 0])
coronal = np.rot90(coronal, 1)

# Organize the data for visualisation in the transversal plane
transversal = np.transpose(data_all, [2, 1, 3, 0])
transversal = np.rot90(transversal, 2)

# Organize the data for visualisation in the sagittal plane
sagittal = np.transpose(data_all, [2, 3, 1, 0])
sagittal = np.rot90(sagittal, 1)

# Plot some of the images in different planes
n = 10
for i in range(6):
    ax[0][i].imshow(coronal[:, :, n, 0], cmap="gray")
    ax[0][i].set_xticks([])
    ax[0][i].set_yticks([])
    if i == 0:
        ax[0][i].set_ylabel("coronal", fontsize=25, color="r")
    n += 10
    
n = 5
for i in range(6):
    ax[1][i].imshow(transversal[:, :, n, 0], cmap="gray")
    ax[1][i].set_xticks([])
    ax[1][i].set_yticks([])
    if i == 0:
        ax[1][i].set_ylabel("transversal", fontsize=25, color="r")
    n += 10
    
n = 5
for i in range(6):
    ax[2][i].imshow(sagittal[:, :, n, 0], cmap="gray")
    ax[2][i].set_xticks([])
    ax[2][i].set_yticks([])
    if i == 0:
        ax[2][i].set_ylabel("sagittal", fontsize=25, color="r')
    n += 10

fig.subplots_adjust(wspace=0, hspace=0)
plt.show()

# Create an empty plot with defined aspect ratio
fig, ax = plt.subplots(1, 1, figsize=[18, 5])

# Plot the timecourse of a random voxel
ax.plot(transversal[30, 30, 35, :], lw=3)
ax.set_xlim([0, transversal.shape[3]-1])
ax.set_xlabel("time [s]", fontsize=20)
ax.set_ylabel("signal strength", fontsize=20)
ax.set_title("voxel time course", fontsize=25)
ax.tick_params(labelsize=12)

plt.show()

# Rearrange and reshape data for export
data_all = np.transpose(data_all, [3, 2, 1, 0])
data_all = np.reshape(data_all, [n_slice, y_size*x_size, n_volumes])

# Check if output path exists, if not create it.
if os.path.exists(".fMRI_data/csv_data") == False:
    os.mkdir("./fMRI_data/csv_data")

# Export each slice as a .csv file 
n = 0
for export in data_all:
    save_file = "slice_{}.csv".format(n)
    save_path = "./fMRI_data/csv_data/{}".format(save_file)
    pd.DataFrame(export).to_csv(save_path, header=False, index=False)
    n += 1

# Main parameters of the fMRI scan and experimental desgin
block_design = ["rest", "stim"]
block_size = 6
block_RT = 7
block_total = 16
block_length = block_size*block_RT
acq_num = block_size*block_total
data_time = block_length*block_total
data_time_vol = np.arange(acq_num)*block_RT
x_size = 64
y_size = 64

