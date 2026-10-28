CST Microstrip Patch Antenna Simulation Automation 

Overview

This project automates the generation and simulation of parameterised rectangular microstrip patch 
antenna designs using CST Studio Suite and Python. 

The automation workflow generates antenna geometry parameters, applies them to a CST project, runs electromagnetic
simulations, extracts the simulated reflection coefficient (S11) and combines the results into a structured 
dataset. 

The resulting dataset is intended for use in machine learning surrogate modeling experimentation.

Project objectives
- automate the generation of antenna design parameters
- reduce repetitive manual work involved in CST simulations
- Extract S11 frequency-response data from simulated antenna designs
- Build a dataset relating antenna geometry, physical properties, frequency and S11 response
- Support the development and evaluation of machine learning surrogate models

Technologies used
- Python
- CST Studio Suite
- NumPy/pandas/SciPy
- Git and Github

Repository Structure

ecs750pmsc/

-01_generate_designs.py

-02_run_simulations.py

-config.py

-cst_utils.py

-dataset_utils.py

-README.md

-.gitignore

The python files operate as such:
- 01_generate_designs.py — generates antenna parameter combinations for simulation.

- 02_run_simulations.py — coordinates the CST simulation workflow, exports S11 data, and contributes simulation results to the dataset.

- config.py — centralises configuration settings, parameter ranges, frequency settings, file paths, and sampling options. Modify parameters
            in this file to adjust for your specific project. 

- cst_utils.py — contains utilities for interacting with CST and managing simulation-related operations.

- dataset_utils.py — contains functions for loading, processing, combining, and appending simulation data.

The antenna designs are parameterized using the following parameters and ranges:
- L (Patch Length) - 26 - 34 mm
- W (Patch Width) - 30 - 40 mm
- H (Substrate thickness) - 1.0 - 2.4 mm
- FeedW (Feed-line width) - 2 - 4 mm
- InsetD (Feed inset depth) - 4 - 12 mm
- EpsilonR (Substrate relative permittivity) - 3.8 - 4.8

The simulation frequency range is configured from 1.7 GHz to 2.8 GHz. The number of designs, sampling seed, frequency step and output
downsampling factor can be adjusted in config.py. 
The ranges above describe the configured sampling bounds, the actual designs depend on the sampling method and 
any geometry-validity constraints in the scripts. 

Requirements
In order to run the automation you will need:
- Python
- A compatible installation of CST Studio Suite
- A compatible CST antenna project configured with the parameters and simulation setup
  expected by the scripts
- The defined Python libraries

Setup
1. clone the repository

  git clone https://github.com/zgon869/ecs750pmsc.git
  
  cd ecs750pmsc

2. Prepare the CST project

The CST project file itself is not included in this repository so users must supply their own compatible
.cst project. The project must contain the antenna geometry, parameter definitions, solver configuration and
S-parameter results/export setup expected by the automation scripts.

3. Configure the file paths

Open config.py and configure PROJECT_PATH to point to your CST project file. The remaining file paths are 
configured relative to the Python project directory. Ensure the scripts have permission to create and modify the required 
output files. 

4. Review configuration settings

Before running the scripts, review config.py and confirm that the parameter ranges, frequency settings, number of designs
and file paths are appropriate for your intended simulations.

5. Running the automation

Run the scripts in the intended order:

  Step 1: Generate Antenna Designs
  
  python 01_generate_designs.py

  This generates parameter combinations for the antenna designs and saves them to the configured parameter file. The sampling
  process applies the geometry-validity constraints implemented in the script. 

  Step 2: Run CST simulations and generate the dataset
  
  python 02_run_simulations.py

  This script is called on in the CST Python API through the command "run (file path)\02_run_simulations.py " . This 
  processes the generated designs, runs the CST simulations , exports the S11 response data and combines the simulation results with
  the corresponding design parameters. Simulation execution depends on the CST installation, project configuration, and the CST automation
  interface supported by the environment. 
  
  Note: The simulations may take considerable time depending on the number of designs, solver settings, available hardware and CST configuration.
  KNOWN BUG: SOME SIMULATIONS MAY OCCASIONALLY FAIL DUE TO AN ERROR WITH CERTAIN INSTALLS OF CST. IN THIS INSTANCE, SUCH SIMULATIONS WILL
  HAVE TO BE MANUALLY RERUN. IN THE EVENT SAMPLES FAIL, THE SIMULATION LOG WILL IDENTIFY THEM. 

  Dataset output:

  The generated dataset associates each antenna design with its parameter values and simulated S11 response across the configured frequency
  range. Depending on the output configuration, generated files may include:

  parameter_samples.csv — generated antenna parameter combinations.

  output_dataset.csv — intermediate or processed dataset output, if produced by the configured workflow.

  MASTER_DATASET_FILE.csv — consolidated dataset of design parameters, frequencies, and S11 values.

  simulation_log.txt — simulation execution log.

  export_file1.txt — temporary or intermediate S11 export.

Intended Application

The dataset generated by this automation is intended to support the training and evaluation of machine learning models 
to predict antenna S11 responses from design parameters an frequency. 
Such surrogate models can be evaluated against CST simulation results to investigate the prediction accuracy of a much 
more computationally efficient methodology. 

Limitations

-A compatible CST project and access to CST Studio Suite are required.
-Simulation results depend on the antenna geometry, material definitions, mesh settings, solver configuration, and frequency sweep used in the supplied project.
-Users may need to adapt the CST integration or project parameter names to their own setup.
-The generated dataset reflects the parameter ranges and simulation assumptions used to produce it; predictions outside those ranges require
additional validation.

Reproducibility

A fixed random seed is confgured to help reproduce parameter sampling. Reproducing the complete dataset also requires compatible
CST settings, matching project geometry and parameter definitions and consistent simulation configurations. 
