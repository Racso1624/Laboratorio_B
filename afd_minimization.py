from afd import *

def afdMinimization(afd, name):
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
                                        partition_dictionary[state] = [[symbol, partitions.index(partition_2)]]
                                    else:
                                        value = partition_dictionary[state]
                                        value.append([symbol, partitions.index(partition_2)])
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

    print(states_partition)
    minimized_states = []
    minimized_transitions = []
    minimized_final_state = []

    for partition in partitions:
        minimized_states.append("S" + str(partitions.index(partition)))

    for partition in partitions:
        for symbol in symbols:
            index = partitions.index(partition)
            state_partition = states_partition[index]
            len_partition = len(state_partition) - 1
            for i in range(len_partition):
                if(state_partition[i][0] == symbol):
                    minimized_transitions.append([minimized_states[index], symbol, minimized_states[state_partition[i][1]]])
    


    print(minimized_transitions)
    # Se crea el AFD
    afd_minimized = AFD(name)
    afd_minimized.regex = afd.regex
    afd_minimized.states = minimized_states
    afd_minimized.transitions = minimized_transitions
    afd_minimized.initial_state = minimized_states[0]
    afd_minimized.final_state = minimized_final_state
    afd_minimized.symbols = afd.symbols
    afd_minimized.graphAF()