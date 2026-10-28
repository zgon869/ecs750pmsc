"""
Generate Latin Hypercube antenna geometries for input file
for CST Studio Suite for experimentation with Rectangular 
Microstrip Patch Antennas

"""
import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
from scipy.stats import qmc

from config import *

def scale_samples(lhs_samples):
    """
    Convert Latin Hypercube samples from [0,1]
    into real antenna dimensions
    """
    scaled = np.zeros_like(lhs_samples)
    parameter_names = list(PARAMETER_RANGES.keys())

    for i, parameter in enumerate(parameter_names):
        lower, upper = PARAMETER_RANGES[parameter]
        scaled[:, i] = lower + lhs_samples[:,i] * (upper - lower)

    return scaled

def is_valid(sample):
    """
    Returns True is the antenna geometry is physically
    valid

    Take a generated antenna, extract patch length, and inset 
    depth, and geometry will be considered valid only if the inset
    depth is no more than 45% of the patch length.
    """
    L = sample[list(PARAMETER_RANGES.keys()).index("L")]
    inset = sample[list(PARAMETER_RANGES.keys()).index("InsetD")]

    return inset <= 0.45*L

#generate latin hypercube
sampler = qmc.LatinHypercube(
    d = len(PARAMETER_RANGES),
    seed = RANDOM_SEED
)

    #Aiming to have 500 unique geometries, so we need to ensure
    #we have enough which pass the validation test
valid_samples = []
rejected = 0
batch_size = 100

while len(valid_samples) < N_DESIGNS:
    raw_samples = sampler.random(n=batch_size)
    scaled_samples = scale_samples(raw_samples)
    for sample in scaled_samples:
        if is_valid(sample):
            valid_samples.append(sample)
        else:
            rejected += 1
        if len(valid_samples) >= N_DESIGNS:
            break


#Convert to dataframe
columns = list(PARAMETER_RANGES.keys())

df = pd.DataFrame(
    valid_samples,
    columns = columns
)

#Insert an id column
df.insert(0, "SampleID", np.arange(1,len(df)+1))

#Save
df.to_csv(
    OUTPUT_FILE,
    index = False,
    float_format="%.4f"
)

print(f"{len(df)} antenna geometries generated.")
print(f"Rejected {rejected} invalid designs.")

print ("\nParameter Statistics\n")
print(df.describe())

#Generate histogram of sampled parameters
df.hist(figsize=(12,8))
plt.tight_layout()
plt.show()