
def afdMinimization(afd):
    states = afd.states
    transitions = afd.transitions
    partitions = []
    acceptance_state = []
    normal_state = []

    for i in states:
        if(i in afd.final_state):
            acceptance_state.append(i)
        else:
            normal_state.append(i)

    if(len(acceptance_state) != 0):
        partitions.append(acceptance_state)
    if(len(normal_state) != 0):
        partitions.append(normal_state)

    not_distinguishable = True
    while(not_distinguishable):
        for i in partitions:
            pass