'''
Defines functions which interface with the CST Python API
'''

import pandas as pd
import csv
import cst.interface
import logging
import os
import sys
import inspect
import time

from cst.interface import DesignEnvironment

def connect_to_project(project_path):
    '''
    Connect to CST Studio and open the project. 
    Returns the DesignEnvironment and project objects.
    '''

    de = DesignEnvironment.connect_to_any_or_new()
    project = de.open_project(project_path)

    return de, project

def apply_design(project, design):
    '''
    Apply one antenna geometry from a pandas row.
    '''

    model = project.model3d

    model.StoreParameter("L", float(design["L"]))
    model.StoreParameter("W", float(design["W"]))
    model.StoreParameter("H", float(design["H"]))
    model.StoreParameter("FeedW", float(design["FeedW"]))
    model.StoreParameter("InsetD", float(design["InsetD"]))
    model.StoreParameter("EpsilonR", float(design["EpsilonR"]))

    model.Rebuild()

def run_solver(project):
    '''
    Run the CST solver and wait until it is completed.
    '''
    start = time.time()
    project.model3d.RunSolver()
    elapsed = time.time() - start

    return elapsed

def export_s11(project, export_path):
    '''
    Export the selected S11 curve

    Retries the tree selection several times because CST
    occasionally leaves the current view on "Components"
    immediately after solver finishes instead of "1D Results\S-Parameters\S1,1".
    '''

    model = project.model3d
    expected = r"1D Results\S-Parameters\S1,1"

    '''
    This for loop was constructed in trying to understand and fix the problem of some simulations
    failing. It appeared that CST would sometimes select the incorrect tree item after completing 
    a simulation, so this loop was an attempt to force it to reselect the correct tree item in order
    to finish the simulation. This did not solve the problem, however  a decision was made to just 
    rerun the failed simulations rather than trying to fix the CST error. This code was left here in 
    the event the debugging process is continued.
    '''
    for attempt in range(10):
        print("\nChecking available tree methods...")
        for name in dir(model):
            if "Tree" in name or "tree" in name or "Exist" in name or "exist" in name:
                print(name)

        model.SelectTreeItem(expected)
        selected = model.GetSelectedTreeItem()
        if selected == expected:
            break
        print(
            f"Selection attempt {attempt + 1}/10 failed"
            f"(current = '{selected}')"
        )
        model.GetSolverRunInfo()
        while model.IsSolverRunning():
            time.sleep(0.5)
    else:
        raise RuntimeError(
            f"Failed to select S11 after 10 attempts."
            f"Current selection: {selected}"
            print("Solver running:",
                  model.IsSolverRunning())
        )

    #Existing export code
    ascii_export = model.ASCIIExport
    ascii_export.Reset()
    ascii_export.FileName(export_path)
    ascii_export.Execute()

def close_project(project):
    '''
    Close the CST project.
    '''

    project.close()