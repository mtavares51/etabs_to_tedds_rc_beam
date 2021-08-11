# import etabs_python connection libraries
import sys
import comtypes.client

# import data science libraries
import pandas as pd
import numpy as np

# import auxiliary functions
from get_beam_forces import get_beam_forces
from get_beam_rebar_rev1 import get_beam_rebar


# CHECKLIST BEFORE RUN:
# Ensure etabs is opened,
# Ensure analysis is run
# Ensure check/design reinforcement was run in etabs

### script inputs
framename = '6'  # frame unique name in ETABS. Ensure frame name is exactly what you want
                   # this could be developed to run over selected elements
stations = [3.75, 7.5, 11.25]  # stations to output in meters
combos = ['ULS-grav', 'SLS']  # combos to output. It should be a list: [ULS, SLS].

pref_d = 32  #  diameter for long rebar
link_d = 12  #  diameter for links
n_legs = 5  # number of link legs
l_spacing = 75  # maximum longitudinal spacing of flexural rebar
cover = 35  # side cover

### end of script inputs

# this assumes ETABS structural model is opened
AttachToInstance = True

if AttachToInstance:
    #attach to a running instance of ETABS
    try:
        #get the active ETABS object
        myETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
    except (OSError, comtypes.COMError):
        print("No running instance of the program found or failed to attach.")
        sys.exit(-1)

# Get current etabs instance and assign it to ETABSObject variable
myETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")

# Assign model to SapModel variable
SapModel = myETABSObject.SapModel

# Ensure model is locked so model edition is not possible
SapModel.SetModelIsLocked(True)

# Define units in kN_m_C
kN_m_C = 6
SapModel.SetPresentUnits(kN_m_C)

### Get forces dataframe
df_forces, e_stations = get_beam_forces(stations, framename, combos, SapModel)

### Get design reinforcement
df_rebar = get_beam_rebar(SapModel, framename, e_stations, pref_d, link_d, n_legs, l_spacing, cover)

# concatenate forces and rebar dataframes
df_forces_rebar = pd.concat([df_forces, df_rebar], axis=1)

### Get dataframe columns and set units as 1st row of tedds dataframe
batch_columns = df_forces_rebar.columns

# units_map dictionary with "map" liasing each column name start and corresponding unit
units_map = {'M_':'kNm',
             'V_':'kN',
             'b_':'mm',
             'h_':'mm',
             'N_':'',
             '\\6':'mm',
             's_':'mm',
             '_C':'',
             }

# build units dictionary
units_dict = {}
for column in batch_columns:
    key = column[:2]
    value = units_map[key]
    units_dict[column] = value

# build units dataframe
units_df = pd.DataFrame(units_dict, index=[0])

# concatenate units dataframe with forces_rebar dataframe putting units in first row
df_tedds = pd.concat([units_df, df_forces_rebar], axis=0)

# create excel to copy paste to tedds RC beam design batch analysis
df_tedds.to_excel("Beam" + framename + ".xlsx")



