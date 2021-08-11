def get_rebar(ixs, rebar):
    """function to get maximum amount of rebar for each location. Returns a vector with rebar for each location"""
    """ixs - indices; rebar - vector with etabs reinforcement"""

    rebar_v = [0 for i in range(len(ixs))]  # initialize vector to store amount of reinforcement

    for i in range(len(ixs)):  # for each location
        temp = []  # initialize temporary empty vector to store station indices for each location
        for j in range(len(ixs[i])):  # for each station index (one location might have 2 stations)
            k = ixs[i][j]
            temp.append(rebar[k])  # get rebar area for that station index
        rebar_v[i] = max(temp)  # chose highest amount of rebar for each location

    return rebar_v
