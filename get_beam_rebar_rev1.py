# import data science libraries
import numpy as np
import pandas as pd

# import auxiliary functions
from get_rebar import get_rebar
from PlaceRebarRev1 import *





def get_beam_rebar(sm, fn, sta, d, link_d, n_legs, l_spacing, cover):
    """Uses etabs API function GetSummaryResultsBeam to return vectors of reinforcement for each station"""
    """sm - SapModel; fn - frame name; sta - etabs stations returned from get_beam_forces"""
    """d - longitudinal rebar diameter; link_d - link diameter"""
    """n_legs - number of link legs; l_spacing - minimum longitudinal bar spacing; cover - side cover"""

    [NumberResults, FrameName, Location, TopCombo, TopArea, BotCombo, BotArea, VMajorCombo, VMajorArea, TLCombo, TLArea,
     TTCombo, TTArea, ErrorSummary, WarningSummary, ret] = sm.DesignConcrete.GetSummaryResultsBeam(
        fn,  # frame name
        0,  # NumberItems,
        [],  # FrameName,
        [],  # Location,
        [],  # TopCombo,
        [],  # TopArea,
        [],  # BotCombo,
        [],  # BotArea,
        [],  # VMajorCombo,
        [],  # VMajorArea,
        [],  # TLCombo,
        [],  # TLArea,
        [],  # TTCombo,
        [],  # TTArea,
        [],  # ErrorSummary,
        [],  # WarningSummary,
    )

    # need to find indices for each location and get rebar for that station. Note that there are locations with 2 indices
    # (2 stations) and this can result in different rebar amount for each index.
    indices = []
    for station in sta:  # loop to get a list with all station indices that match our locations
        indices.append([i for i, x in enumerate(Location) if x == station])

    as_l_top = np.round_(np.array(get_rebar(indices, TopArea)) * 1000000, 0)
    as_l_bot = np.round_(np.array(get_rebar(indices, BotArea)) * 1000000, 0)
    as_v = np.round_(np.array(get_rebar(indices, VMajorArea)) * 1000000, 0)
    asT_l = np.round_(np.array(get_rebar(indices, TLArea)) * 1000000, 0)
    asT_v = np.round_(np.array(get_rebar(indices, TTArea)) * 1000000, 0)

    # get section name of frame
    sn = sm.FrameObj.GetSection(fn, '', '')[0]

    # get depth and width of rectangular beam
    conc_rect = sm.PropFrame.GetRectangle(sn, '', '', 0, 0, 0, '', '')
    b = [conc_rect[3] * 1000 for i in range(len(sta))]

    # initialize lists to get rebar data
    bars_l_top = []
    bars_l_bot = []
    links_v = []
    bars_l_torsion = []
    links_v_torsion = []

    #  place rebar for each station
    for i in range(len(indices)):
        bars_l_top.append(place_rebar_long_flex(as_l_top[i], b[i], cover, link_d, d, l_spacing))
        bars_l_bot.append(place_rebar_long_flex(as_l_bot[i], b[i], cover, link_d, d, l_spacing))
        links_v.append(place_rebar_trans_v(as_v[i], link_d, n_legs))
        bars_l_torsion.append(place_rebar_long_torsion(asT_l[i], d))
        links_v_torsion.append(place_rebar_trans_v(asT_v[i], link_d, n_legs))

    #  re-arrange rebar data to be read in Tedds batch analysis
    n_bars_top, diams_top, max_layers_top = group_l_bars(bars_l_top)
    n_bars_bot, diams_bot, max_layers_bot = group_l_bars(bars_l_bot)

    #  create keys for dictionaries that will store rebar data
    n_top_keys = ['N_{s1_t_L' + str(layer) + '}' for layer in range(1, max_layers_top + 1)]
    n_bot_keys = ['N_{s1_b_L' + str(layer) + '}' for layer in range(1, max_layers_bot + 1)]
    d_top_keys = ['\\66_{s1_t_L' + str(layer) + '}' for layer in range(1, max_layers_top + 1)]
    d_bot_keys = ['\\66_{s1_b_L' + str(layer) + '}' for layer in range(1, max_layers_bot + 1)]

    #  create dictionaries for flexural rebar
    n_top_dict = dict(zip(n_top_keys, n_bars_top))
    n_bot_dict = dict(zip(n_bot_keys, n_bars_bot))
    d_top_dict = dict(zip(d_top_keys, diams_top))
    d_bot_dict = dict(zip(d_bot_keys, diams_bot))

    #  create values for shear dictionaries
    link_legs_values = list(list(zip(*links_v))[0])
    link_diam_values = list(list(zip(*links_v))[1])
    link_spacing_values = list(list(zip(*links_v))[2])

    #  create dictionaries for shear rebar
    link_legs_dict = {'N_{s1_v}': link_legs_values}
    link_diam_dict = {'\\66_{s1_v}': link_diam_values}
    link_spacing_dict = {'s_{s1_v}': link_spacing_values}

    #  create master dictionary object to make dataframe unpacking all dictionaries created
    d = {**n_bot_dict,
         **d_bot_dict,
         **n_top_dict,
         **d_top_dict,
         **link_legs_dict,
         **link_diam_dict,
         **link_spacing_dict, }

    df = pd.DataFrame(d)

    return df

