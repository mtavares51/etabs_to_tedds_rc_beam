import numpy as np

# start testing variables
Width = 1300   # beam width
Top_Cover = 35  # beam cover
As_b_req = 3459  # bottom rebar
As_t = 500  # top rebar

Link_d = 12  # link diameter
Top_d = 32  # top bar diameter
Bottom_d = 32  # bottom bar diameter
Spacing = 75  # minimum spacing between bars

def place_rebar_long_flex(as_req, width, cover, link_d, d, spacing):
    """Calculates number of bars and layers that are needed to reach a required area of steel (as_req)"""
    """as_req - required area of steel"""
    """width - beam width; cover - beam side cover; link_d; shear link diameter in millimeters"""
    """d - diameter of bar; spacing - minimum spacing of bars"""

    layer = [2]  # initialize vector that stores number of bottom bars (minimum 2)
    as_ = layer[-1] * d ** 2 * np.pi / 4  # determine current area of reinforcement

    while as_ < as_req:  # while amount of reinforcement of the beam is less than required
        layer[-1] = layer[-1] + 1  # add one bar
        # evaluate distance between bars
        d_axis_b = (int(width) - 2 * cover - 2 * link_d - d) / (int(layer[-1]) - 1)  # distance between bar axis
        d_bars_b = d_axis_b - d  # distance between bars

        if d_bars_b < spacing:  # in case bars are spaced less than spacing variable
            layer[-1] = layer[-1] - 1  # go back to previous number of bars
            layer.append(2)  # add another layer of bars with minimum of 2 bars

        as_ = sum(layer) * d ** 2 * np.pi / 4  # update current area of reinforcement

    rebar = []

    for i in range(len(layer)):
        layers_list = [layer[i], d]
        rebar.append(layers_list)

    return rebar


# start testing variables
Asv_req = 1000  # transverse rebar area required in mm2/m
diameter_v = 12  # preferred rebar diameter
number_legs = 5  # number of link legs


def place_rebar_trans_v(asv_req, d_v, n_legs):
    """Calculates longitudinal spacing of shear links that are needed to reach a required area of steel (asv_req)"""
    """asv_req - required area of steel in mm2/m"""
    """d_v - diameter of shear link"""
    """n_legs - number of legs"""
    spacings = [250, 225, 200, 175, 150, 125, 100, 75]  # available spacings
    a_leg = np.pi * d_v ** 2 / 4  # area of each link leg
    a_links = a_leg * n_legs  # total area per links set

    for i in range(len(spacings)):

        Asv = a_links / (spacings[i] * 0.001)
        if Asv > asv_req:
            break
    a = [n_legs, d_v, spacings[i]]

    if i == len(spacings) - 1 and Asv < Asv_req:  # in case number of legs and diameters is not enough
        a = [0, 0, 0]

    return a

#place_rebar_trans_v(Asv_req, diameter_v, number_legs)

def place_rebar_long_torsion(as_tl_req, d):
    """Checks if 4 torsion bars provided in each corner of the beam are sufficient"""
    """as_tl_req - area of longitudinal reinforcement required for torsion"""
    """d - preferred diameter (this is initially the flexural rebar diameter. If not enough, chose one diameter above"""
    """returns a list with [n, d] where n is number of bars and d diameter of bar"""

    diameters = [12, 16, 20, 25, 32, 40]
    ix = diameters.index(d)

    while ix < len(diameters)-1:  # while loop to run through every diameters possible

        as_t = 4 * np.pi * d ** 2 / 4

        if as_t > as_tl_req:  # in case provided area is enough, break
            a = [4, d]
            break

        else:
            d = diameters[ix+1]
            ix += 1

    if as_t < as_tl_req:  # final check in case provided area is not enough
        a = [0, 0]

    return a

#As_tl_req = 900
#dia = 16
#place_rebar_long_torsion(As_tl_req, dia)

as_l_top = [[[5, 32]], [[11, 32], [11, 32], [5, 32]], [[5, 32]]]
as_l_bot = [[[8, 32]], [[5, 25]], [[7, 32]]]

def group_l_bars(as_l):
    '''This function returns two lists: 1) number of bars at layer 1, 2,.. etc at each station'''
    ''' and 2) diameters used at each layer for each station'''
    ''' zeros means that there's no rebar for that layer'''
    ''' input argument "al_l" should be the array/list given by longitudinal rebar placement function'''

    #  get maximum number of layers among all stations
    max_layers = max([len(as_l[i]) for i in range(len(as_l))])

    #  check all stations and add "null" layers of rebar in case station has less layers than maximum
    for i in range(len(as_l)):
        while len(as_l[i]) < max_layers:
            as_l[i].append([0, 0])

    # double loop to get number of bars and diameters for each layer in each station (to be developed with zip function?)
    n_bars = []  # initialize array to get number of bars
    diams = []  # initialized array to get diameters
    for i in range(max_layers):
        temp_n_bars = []  # temporary array to store number of bars for each station
        temp_diams = []  # temporary array to store diameters for each station
        for j in range(len(as_l)):
            temp_n_bars.append(as_l[j][i][0])  # j is the station iterable variable; i is the layer iterable variable
            temp_diams.append(as_l[j][i][1])
        n_bars.append(temp_n_bars)
        diams.append(temp_diams)
    return n_bars, diams, max_layers

#n_bars_top, diams_top, max_layers = group_l_bars(as_l_top)
#print(n_bars_top, diams_top)

#n_bars_bot, diams_bot, max_layers = group_l_bars(as_l_bot)
#print(n_bars_bot, diams_bot)
