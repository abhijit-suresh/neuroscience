import allensdk.brain_observatory.behavior.swdb.utilities as tools
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import platform
import seaborn as sns

from allensdk.brain_observatory.behavior.swdb import behavior_project_cache as bpc

sns.set_context("notebook", font_scale=1.5, rc={"lines.markeredgewidth": 2})
sns.set_style("white")
sns.set_palette("deep")

platstring = platform.platform()

if "Darwin" in platstring:
    # macOS
    data_root = "/Volumes/Brain2019/"
elif "Windows"  in platstring:
    # Windows (replace with the drive letter of the hard drive)
    data_root = "E:/"
elif ("amzn1" in platstring):
    # then on AWS
    data_root = "/data/"
else:
    # then linux (default here is for Ubuntu - insert your username your distribution may differ)
    data_root = "/media/$USERNAME/Brain2019"
    
cache_path = os.path.join(data_root, "dynamic-brain-workshop/visual_behavior/2019")

"""
Visual behavior
"""

# Load data.
cache = bpc.BehaviorProjectCache(cache_path)

experiments = cache.experiment_table
selected_experiments = experiments[(experiments.full_genotype=="Vip-IRES-Cre/wtAi148(TIT2L-GC6f-ICL-tTA2)/wt") & (experiments.imaging_depth==175) & (experiments.stage_name=="OPHYS_4_images_B")]
selected_experiments

# Print dataset dimensions.
print("targeted structures:", experiments.targeted_structure.unique())
print("\ncre_lines:", experiments.full_genotype.unique())
print("\nstage_types:", experiments.stage_name.unique())

# Random active behavior experiment
active_experiments = experiments[experiments.passive_session==False]
experiment_id = active_experiments.ophys_experiment_id.sample(1).values[0]

# Metadata
row = experiments[experiments["ophys_experiment_id"] == experiment_id]
print(row.targeted_structure.values[0])
print(row.imaging_depth.values[0])
print(row.full_genotype.values[0])
print(row.stage_name.values[0])

# Container ID
container_id = experiments[experiments.ophys_experiment_id==experiment_id]["container_id"].values[0]
experiments.groupby("container_id").get_group(container_id)

# Number of sessions
experiments.groupby("container_id").size()

# Get a session.
session = cache.get_session(experiment_id)

# Plot the max intensity projection and the segmentation mask.
fig, ax = plt.subplots(1, 2)
fig.set_size_inches(10, 5)
ax[0].imshow(session.max_projection)
ax[1].imshow(session.segmentation_mask_image)
plt.tight_layout()

cell_specimen_ids = list(session.roi_masks.keys())
plt.imshow(session.roi_masks[cell_specimen_ids[9]])

# Get traces and timestamps.
dff_traces = session.dff_traces
ophys_timestamps = session.ophys_timestamps

# Get shape of traces and timestamps.
print("shape of dff_traces:",session.dff_traces.shape)
print("shape of ophys_timestamps:",session.ophys_timestamps.shape)

# Shape of the trace of one cell
print("shape of one trace:",session.dff_traces.iloc[0]["dff"].shape)

# Plot the dF/F trace for one cell using ophys timestamps for x-axis values
# indexing method using row index with .iloc.
cell_index = 0 
dff_trace = session.dff_traces.iloc[cell_index]["dff"] # note that the column name is outside of the .iloc call
plt.plot(session.ophys_timestamps, dff_trace)
plt.xlabel("time (sec)")
plt.ylabel("dF/F")
plt.title("cell index: "+str(cell_index))

# Plot the dF/F trace for one cell using ophys timestamps for x-axis values
# indexing method using cell_specimen_id as index with .loc.
# Get cell_specimen_id from a list of all cell_specimen_ids.
cell_specimen_ids = session.dff_traces.index.values
cell_specimen_id = cell_specimen_ids[cell_index]
dff_trace = session.dff_traces.loc[cell_specimen_id, "dff"] # note how the column name is included in the .loc call
plt.plot(session.ophys_timestamps, dff_trace)
plt.xlabel("time (sec)")
plt.ylabel("dF/F")
plt.title("cell_specimen_id: "+str(cell_specimen_id))

# Turn dff_traces into an array of cells x timepoints.
dff_traces_array = np.vstack(session.dff_traces.dff.values)
print("shape of dff_traces_array:",dff_traces_array.shape)

# Plot a heatmap of all traces.
fig, ax = plt.subplots(figsize=(20,5))
cax = ax.pcolormesh(dff_traces_array, cmap="magma", vmin=0, vmax=np.percentile(dff_traces_array, 99))
ax.set_yticks(np.arange(0, len(dff_traces_array)), 10)
ax.set_ylabel("cells")
ax.set_xlabel("time (sec)")
ax.set_xticks(np.arange(0, len(session.ophys_timestamps), 600*31))
ax.set_xticklabels(np.arange(0, session.ophys_timestamps[-1], 600))
cb = plt.colorbar(cax, pad=0.015, label="dF/F")
