import cmor
import numpy 
import json
import os
import shutil
import sys
from copy import deepcopy as copy

DATASET_INFO = {
    "_AXIS_ENTRY_FILE": "tables/GCModelDev_coordinate.json",
    "_FORMULA_VAR_FILE": "tables/GCModelDev_formula_terms.json",
    "_controlled_vocabulary_file": "tables/GCModelDev_CV.json",  # SEPARATE TO MIP TABLES FOR TESTING ONLY
    "activity_id": "ZMIP",
    "branch_method": "standard",
    "branch_time_in_child": 30.0,
    "branch_time_in_parent": 10800.0,
    "calendar": "360_day",
    "experiment_id": "this-expt",
    "experiment": "that",
    "forcing_index": "3",
    "grid": "N96",
    "grid_label": "gn",
    "initialization_index": "1",
    "institution_id": "MOHC",
    "license": "GCModelDev model data is licensed under the Open Government License v3 (https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/)",
    "nominal_resolution": "250 km",
    "outpath": ".",
    "physics_index": "1",
    "realization_index": "9",
    "source_id": "HadGEM3-GC31-LL",
    "source_type": "AOGCM",
    "sub_experiment_id": "none",
    "sub_experiment": "none",
    "tracking_prefix": "GCMODELDEV/",
    "mip_era": "GCModelDev",
}


def main():
    tempdir = sys.argv[1]
    if not os.path.exists(tempdir):
        os.mkdir(tempdir)
    
    dataset_info = copy(DATASET_INFO)
    dataset_info['outpath'] = tempdir
    input_json = os.path.join(tempdir,'input.json')
    with open(input_json, 'w') as fh:
        json.dump(dataset_info, fh, indent=2)

    cmor.setup(inpath="tables", netcdf_file_action=cmor.CMOR_REPLACE)

    cmor.dataset_json(input_json)

    tos = numpy.array([27, 27, 27, 27,
                        27, 27, 27, 27,
                        27, 27, 27, 27,
                        27, 27, 27, 27,
                        27, 27, 27, 27,
                        27, 27, 27, 27
                        ])
    tos.shape = (2, 3, 4)
    lat = numpy.array([10, 20, 30])
    lat_bnds = numpy.array([5, 15, 25, 35])
    lon = numpy.array([0, 90, 180, 270])
    lon_bnds = numpy.array([-45, 45,
                            135,
                            225,
                            315
                            ])
    time = numpy.array([15.5, 16.5])
    time_bnds = numpy.array([15, 16, 17])
    
    
    realm = "ocean"
    cmor.load_table(f"GCModelDev_Oday.json")
    cmorlat = cmor.axis("latitude",
                        coord_vals=lat,
                        cell_bounds=lat_bnds,
                        units="degrees_north")
    cmorlon = cmor.axis("longitude",
                        coord_vals=lon,
                        cell_bounds=lon_bnds,
                        units="degrees_east")
    cmortime = cmor.axis("time",
                        coord_vals=time,
                        cell_bounds=time_bnds,
                        units="days since 2018")
    axes = [cmortime, cmorlat, cmorlon]
    variable = "tos"
    cmortos = cmor.variable(variable, "degC", axes)

    cmor.write(cmortos, tos)
    filename = cmor.close(cmortos, file_name=True)
    print(filename)
    for root, files, directories in os.walk(tempdir):
        for f in files:
            print(os.path.join(root, f))

    input('Hit enter to delete all data created')
    
    shutil.rmtree(tempdir)


if __name__ == '__main__':
    main()
