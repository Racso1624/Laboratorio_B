
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

    if(len(normal_state) != 0):
        partitions.append(normal_state)
    if(len(acceptance_state) != 0):
        partitions.append(acceptance_state)

    not_distinguishable = True
    while(not_distinguishable):
        partitions_table = []
        for partition in partitions:
            for state in states:
                for symbol in symbols:
                    for transition in transitions:
                        if(transition[0] == state and transition[1] == symbol):
                            for partition_2 in partitions:
                                if(transition[2] in partition_2):
                                    partitions_table.append([state, symbol, partitions.index(partition_2), partitions.index(partition)])

        new_partition = []
        for partition in partitions:
            pass                        
        not_distinguishable = False