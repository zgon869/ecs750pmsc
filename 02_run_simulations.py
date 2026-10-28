"""
Runs CST simulations for all generated antenna geometries

project directory must be defined

Requires
--------
config.py
cst_utils.py
dataset_utils.py

Workflow
--------
Load parameter from csv ->
Connect to CST studio ->
For each antenna ->
Apply geometry ->
Run simulation ->
Export S11 ->
Read S11 ->
Combine geometry + s11 ->
Append to dataset
"""

import sys
import pandas as pd
from pathlib import Path

PROJECT_DIR = str(Path(__file__).resolve().parent)

if PROJECT_DIR not in sys.path:
    sys.path.insert(0,PROJECT_DIR)

from config import *
from cst_utils import *
from dataset_utils import *

designs = pd.read_csv(PARAMETER_FILE)

print (f"{len(designs)} antenna designs loaded.")

de, project = connect_to_project(PROJECT_PATH)

print("Connected to CST Studio.")

for _, design in designs.iterrows():   
    sample_id = int(design["SampleID"])
    print(f"\nRunning Sample {sample_id}")
    try:
        apply_design(project, design)
        elapsed = run_solver(project)
        export_s11(project, EXPORT_FILE)
        curve = load_s11(EXPORT_FILE)
        combined = combine_design_with_curve(
            sample_id,
            design,
            curve
        )
    
        append_dataset(
            combined,
            MASTER_DATASET_FILE
        )
        print(f"✓ Sample {sample_id} Completed in {elapsed:.1f} seconds.")
        with open(LOG_FILE, "a") as log:
            log.write(
                f"Sample {sample_id} completed."
                f"({elapsed:.1f} s)\n"
            )
    
    except Exception as e:
        print(f"✗ Sample {sample_id} failed")
        print(project.model3d.GetSelectedTreeItem())
        print(e)
        with open(LOG_FILE, "a") as log:
            log.write(f"Sample {sample_id} FAILED\n")
            log.write(f"{str(e)}\n\n")