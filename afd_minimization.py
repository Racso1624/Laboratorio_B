from afd import *

# Funcion para minimizacion
def afdMinimization(afd, name, title):
    # Se obtienen los estados
    states = afd.states
    transitions = afd.transitions
    symbols = afd.symbols
    partitions = []
    acceptance_state = []
    normal_state = []

    # Se itera en la primera particion de los estados de aceptacion
    for i in states:
        if(i in afd.final_state):
            acceptance_state.append(i)
        else:
            normal_state.append(i)

    # Si hay dos particiones se guardan
    if(len(normal_state) != 0):
        partitions.append(normal_state)
    if(len(acceptance_state) != 0):
        partitions.append(acceptance_state)

    # Se itera hasta que sean distinguibles
    not_distinguishable = True
    while(not_distinguishable):
        # Se utiliza un diccionario para guardar particiones
        partition_dictionary = {}
        # Se itera en cada particion y estado de esta
        for partition in partitions:
            for state in partition:
                for symbol in symbols:
                    # Se itera en cada simbolo de cada una de las transiciones
                    for transition in transitions:
                        if(transition[0] == state and transition[1] == symbol):
                            for partition_2 in partitions:
                                if(transition[2] in partition_2):
                                    # Para cada simbolo se guarda el index de donde va cada una de las transiciones
                                    if(state not in partition_dictionary):
                                        partition_dictionary[state] = [[symbol, partitions.index(partition_2)]]
                                    else:
                                        value = partition_dictionary[state]
                                        value.append([symbol, partitions.index(partition_2)])
                                        partition_dictionary[state] = value
                        else:
                            if(state not in partition_dictionary):
                                    partition_dictionary[state] = []

        # Se crean las particiones de los simbolos y a que grupo llega cada uno
        states_partition = []
        new_partitions = []
        # Para cada estado de las particiones se revisa el diccionario
        for partition in partitions:
            for state in partition:
                value_partition = partition_dictionary[state]
                value_partition.append(partitions.index(partition))
                # Si el valor de las transiciones con los simbolos se agrega a la nueva particion
                if(value_partition not in states_partition):
                    states_partition.append(value_partition)
                    new_partitions.append([state])
                # Si existe ese valor de transicion con simbolos se agrega al grupo al que pertenece
                else:
                    if(value_partition in states_partition):
                        index = states_partition.index(value_partition)
                        new_partitions[index].append(state)       

        # Si las particiones nuevas y anteriores son iguales es que no se puede seguir operando
        if(partitions == new_partitions):
            not_distinguishable = False
        # Si no se guardan las particiones nuevas
        else:
            partitions = new_partitions

    # Se crean las nuevas listas de estados
    minimized_states = []
    minimized_transitions = []
    minimized_final_state = []

    # Por cada particion se crea un nuevo estado
    for partition in partitions:
        minimized_states.append("S" + str(partitions.index(partition)))

        # Se hacen dos sets para lograr hacer operaciones de conjuntos entre ellos
        set_states = set(partition)
        set_final_states = set(afd.final_state)

        # Se verifica que los estados encontrados se encuentren en el conjunto de estados finales
        if(set_states.intersection(set_final_states).__len__() != 0):
            minimized_final_state.append("S" + str(partitions.index(partition)))

    # Se crean las tranciones por cada una de las particiones
    for partition in partitions:
        # Por cada simbolo
        for symbol in symbols:
            index = partitions.index(partition)
            state_partition = states_partition[index]
            len_partition = len(state_partition) - 1
            # Para cada simbolo al que transiciona se crea la transicion
            for i in range(len_partition):
                if(state_partition[i][0] == symbol):
                    # Se agrega la transicion
                    minimized_transitions.append([minimized_states[index], symbol, minimized_states[state_partition[i][1]]])
    
    # Se crea el AFD
    afd_minimized = AFD(name, title)
    afd_minimized.regex = afd.regex
    afd_minimized.states = minimized_states
    afd_minimized.transitions = minimized_transitions
    afd_minimized.initial_state = minimized_states[0]
    afd_minimized.final_state = minimized_final_state
    afd_minimized.symbols = afd.symbols
    afd_minimized.graphAF()