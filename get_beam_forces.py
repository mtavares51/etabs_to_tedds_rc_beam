# import data science libraries
import pandas as pd
import numpy as np

# import auxiliary functions
from get_station_forces import get_station_forces


def get_beam_forces(sta, fn, cb, sm):
    """Returns a dataframe with internal forces for each station and etabs stations."""
    """sta - vector with stations; fn - framename; cb - vector with combos [ULS, SLS]; sm - SapModel variable"""

    # initialize vectors to be assigned each station internal force and also store etabs stations
    st_M_pos_s1 = [''] * len(sta)
    st_M_neg_s1 = [''] * len(sta)
    st_M_pos_QP_s1 = [''] * len(sta)
    st_M_neg_QP_s1 = [''] * len(sta)
    st_V2 = [''] * len(sta)
    etb_stations = [''] * len(sta)

    # get each station internal forces an assign to vectors
    for st in range(len(sta)):

        station = sta[st]
        st_M_pos_s1[st], st_M_neg_s1[st], st_M_pos_QP_s1[st], st_M_neg_QP_s1[st], st_V2[st], etb_stations[st] = get_station_forces(fn, cb, station, sm)

    # get section name of frame
    sn = sm.FrameObj.GetSection(fn, '', '')[0]

    # get depth and width of rectangular beam
    conc_rect = sm.PropFrame.GetRectangle(sn, '', '', 0, 0, 0, '', '')
    h = [conc_rect[2]*1000 for i in range(len(sta))]  # list comprehension to fill height for each station
    b = [conc_rect[3]*1000 for i in range(len(sta))]
    conc_class = [conc_rect[1] for i in range(len(sta))]

    d = {'M_{pos_s1}': st_M_pos_s1,
         'M_{neg_s1}': st_M_neg_s1,
         'M_{pos_QP_s1}': st_M_pos_QP_s1,
         'M_{neg_QP_s1}': st_M_neg_QP_s1,
         'V_{s1}': st_V2,
         'V_{Ed,max_s1}': st_V2,
         'b_{s1}': b,
         'h_{s1}': h,
         '_ConcreteClass': conc_class}

    df = pd.DataFrame(d).round(decimals=2)

    return df, etb_stations