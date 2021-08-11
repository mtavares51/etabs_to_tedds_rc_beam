# import auxiliary functions
from find_nearest import find_nearest
from get_ix import get_ix


def get_station_forces(framename, combos, station, sm):
    """Function to get internal forces for combinations at one station"""
    """combos parameter should be a list with two strings: ['ULS combo', 'SLS combo']"""
    for i in range(len(combos)):

        # Deselect All Load Combinations
        sm.Results.Setup.DeselectAllCasesAndCombosForOutput

        # Select load combo
        ComboName = combos[i]
        sm.Results.Setup.SetComboSelectedForOutput(ComboName)

        # Get results for a frame object
        # Initialize dummy variables
        ObjectElm = 0  # equal to zero to retrieve by name of the frame
        NumberResults = 0  # The total number of results returned by the program
        Obj = []  # line object name associated with each result, if any
        ObjSta = []  # distance measured from the I-end of the line object to the result location
        Elm = []  # line element name associated with each result
        ElmSta = []  # distance measured from the I-end of the line element to the result location
        LoadCase = []  # name of the analysis case or load combination
        StepType = []  # step type, if any, for each result
        StepNum = []  # step number, if any, for each result
        P = []  # axial force for each result
        V2 = []
        V3 = []
        T = []
        M2 = []
        M3 = []

        # Get results for frame
        FrameName = framename  # name of the frame
        [NumberResults, Obj, ObjSta, Elm, ElmSta, LoadCase, StepType, StepNum, P, V2, V3, T, M2, M3,
         ret] = sm.Results.FrameForce(
            FrameName,
            ObjectElm,
            NumberResults,  # The total number of results returned by the program
            Obj,  # line object name associated with each result, if any
            ObjSta,
            # distance measured from the I-end of the line object to the result location
            Elm,  # line element name associated with each result
            ElmSta,
            # distance measured from the I-end of the line element to the result location
            LoadCase,  # name of the analysis case or load combination
            StepType,  # step type, if any, for each result
            StepNum,  # step number, if any, for each result
            P,  # axial force for each result
            V2,
            V3,
            T,
            M2,
            M3,
        )
        lcs = len(set(LoadCase))  # number of different load cases selected for output
        # for some reason etabs selects more than 1 case except on the first run

        # get nearest station value
        station = find_nearest(ObjSta, station)

        # get index for that station
        ObjSta_ix_uls, ObjSta_ix_sls = get_ix(ObjSta, lcs, station, NumberResults)

        if i == 0:  # this means if combo is ULS
            Med = M3[ObjSta_ix_uls]  # get bending moment at station
            Ved = abs(V2[ObjSta_ix_uls])  # get shear at station
            if Med > 0:
                M_pos_s1 = Med
                M_neg_s1 = 0
            else:
                M_pos_s1 = 0
                M_neg_s1 = abs(Med)


        else:  # this means if combo is SLS
            M = M3[ObjSta_ix_sls]
            if M > 0:
                M_pos_QP_s1 = M
                M_neg_QP_s1 = 0
            else:
                M_pos_QP_s1 = 0
                M_neg_QP_s1 = abs(M)

    return M_pos_s1, M_neg_s1, M_pos_QP_s1, M_neg_QP_s1, Ved, station


