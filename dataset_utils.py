import pandas as pd
import csv
import os
from config import *

def load_s11(export_file):
    '''
    Load the exported S11 curve from CST
    
    Parameters
    ----------
    export_file: str
        Path to the exported ASCII file.
    
    Returns
    -------
    pandas.DataFrame
        DataFrame containing Frequency and S11 columns
    '''

    curve = pd.read_csv(
        export_file,
        sep=r"\s+",
        engine="python",
        skiprows=2,
        names=["Frequency", "S11"]
    )
    curve = curve.iloc[::EXPORT_DOWNSAMPLE].reset_index(drop=True)
    return curve

def combine_design_with_curve(sample_id, design, curve):
    '''
    Combine one antenna design with its S11 curve
    
    Parameters
    ----------
    sample_id: int
        Unique geometry sample number.
        
    design: pandas.Series
        One row from parameter_samples.csv
    
    curve: pandas.DataFrame
        Output from load_s11()
        
    Returns
    -------
    pandas.DataFrame
        Combined dataset
    '''

    data = curve.copy()

    design_data = {
        "SampleID": sample_id,
        "L": design["L"],
        "W": design["W"],
        "H": design["H"],
        "FeedW": design["FeedW"],
        "InsetD": design["InsetD"],
        "EpsilonR": design["EpsilonR"]
    }

    combined = data.assign(**design_data)
    combined = combined[
        [
            "SampleID",
            "L",
            "W",
            "H",
            "FeedW",
            "InsetD",
            "EpsilonR",
            "Frequency",
            "S11"
        ]
    ]
    return combined

def append_dataset(data,output_file):
    '''
    Append a batch of simulation data to the master dataset.
    Parameters
    ----------
    data: pandas.DataFrame
        Combined design and S11 data
    
    output_file: str
        Path to the master dataset CSV
    '''

    file_exists = os.path.exists(output_file)

    data.to_csv(
        output_file,
        mode="a",
        header=not file_exists,
        index=False
    )

    def pop_parameter_file(parameterfile, sampleId):
        '''
        Remove entry from Parameter File upon successful 
        completion of simulation to streamline process
        of rerunning simulations for failed samples
        '''
        