
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
        partition_dictionary = {}

        for partition in partitions:
            for state in partition:
                for symbol in symbols:
                    for transition in transitions:
                        if(transition[0] == state and transition[1] == symbol):
                            for partition_2 in partitions:
                                if(transition[2] in partition_2):
                                    if(state not in partition_dictionary):
                                        partition_dictionary[state] = [partitions.index(partition_2)]
                                    else:
                                        value = partition_dictionary[state]
                                        value.append(partitions.index(partition_2))
                                        partition_dictionary[state] = value

        states_partition = []
        new_partitions = []
        for partition in partitions:
            for state in partition:
                value_partition = partition_dictionary[state]
                value_partition.append(partitions.index(partition))

                if(value_partition not in states_partition):
                    states_partition.append(value_partition)
                    new_partitions.append([state])
                else:
                    if(value_partition in states_partition):
                        index = states_partition.index(value_partition)
                        new_partitions[index].append(state)       

        if(partitions == new_partitions):
            not_distinguishable = False
        else:
            partitions = new_partitions

    