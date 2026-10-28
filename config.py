#config.py
'''
Configuration for Microstrip Patch Antenna Surrogate Modeling project

Adjust file path for your patch antenna cst file

Adjust number of desired antenna geometries, frequency ranges
and parameter ranges to desired figures

Export downsample reduces the exported frequency ranges points, if the 
full frequency range sweep from simulations is desired, remove this 
line.
'''

from pathlib import Path

# Folder containing this python configuration file
BASE_DIR = Path(__file__).resolve().parent

# CST project file

# Change this to the name and location of your own CST project file
PROJECT_PATH = BASE_DIR/"Patch_Antenna_Automation.cst"

#Output and data files
OUTPUT_DATASET = BASE_DIR/"output_dataset.csv"

PARAMETER_FILE = BASE_DIR/"parameter_samples.txt"

LOG_FILE = BASE_DIR/"simulation_log.txt"

EXPORT_FILE = BASE_DIR/"export_file1.txt"

MASTER_DATASET_FILE = BASE_DIR/"MASTER_DATASET_FILE.csv"

EXPORT_DOWNSAMPLE = 7  #Reduce the amount of frequencies per single geometry written to output dataset

#Number of Antenna geometries
N_DESIGNS = 500

#Frequency Range
FREQ_START = 1.7
FREQ_STOP = 2.8
FREQ_STEP = 0.01

#Random seed for reproducibility 
RANDOM_SEED = 42

#Parameter ranges 
PARAMETER_RANGES = {
    "L": (26.0, 34.0),
    "W": (30.0, 40.0),
    "H": (1.0,2.4),
    "FeedW": (2.0, 4.0),
    "InsetD": (4.0, 12.0),
    "EpsilonR": (3.8, 4.8)
}

#Output file for generated parameter samples
OUTPUT_FILE = BASE_DIR/"parameter_samples.csv"