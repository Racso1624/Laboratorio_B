
def afdMinimization(afd):
    states = afd.states
    transitions = afd.transitions
    symbols = afd.symbols
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
        for partition in partitions:
            for state in partition:
                for symbol in symbols:
                    for transition in transitions:
                        if(transition[0] == state and transition[1] == symbol):
                            print(transition)
        not_distinguishable = False