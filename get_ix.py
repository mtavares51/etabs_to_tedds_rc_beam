def get_ix(objsta, lcs, station, nr):
    """Function to get index depending on number of load cases"""
    if lcs != 1:  # if it is picking 2 load cases
        ObjSta_ix_sls = objsta.index(station)  # get station index for sls
        ObjSta_ix_uls = objsta.index(station) + int(nr / 2)  # get station index for uls
    else:  # if it is picking 1 load case
        ObjSta_ix_sls = objsta.index(station)
        ObjSta_ix_uls = objsta.index(station)

    return ObjSta_ix_uls, ObjSta_ix_sls