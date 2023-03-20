from afd import *
from syntaxtree import *

# Se toma el algortimo para nullable
def nullable(node):

    # Se retornan nulos los simbolos que lo son
    if(node.character in "ε?*"):
        return True
    # Para el or se retorna los nulos de los dos hijos con or
    elif(node.character == "|"):
        return (nullable(node.left_child) or nullable(node.right_child))
    # Para concatenacion se retorna el nulo de los dos hijos con and
    elif(node.character == "."):
        return (nullable(node.left_child) and nullable(node.right_child))
    # Para la cerradura positiva se regresa el nulo del hijo
    elif(node.character == "+"):
        return nullable(node.left_child)
    # Si es un caracter no es nulo
    else:
        return False

# Se toma el algoritmo para realizar el firstpos
def firstpos(node):

    # Si es epsilon se regresa un vacio
    if(node.character == "ε"):
        return set()
    # Si es un or se regresa la union de los dos hijos
    elif(node.character == "|"):
        return (firstpos(node.right_child).union(firstpos(node.left_child)))
    # Si es concatenacion se regresa la union si el izquierdo es nulo, del contrario es el izquierdo
    elif(node.character == "."):
        if(nullable(node.left_child)):
            return (firstpos(node.right_child).union(firstpos(node.left_child)))
        else:
            return firstpos(node.left_child)
    # Para las cerraduras se regresa el firstpos de su hijo
    elif(node.character in "*+?"):
        return firstpos(node.left_child)
    # Si es un caracter se regresa solo la posicion
    else:
        return {node}

# Se toma el algoritmo para realizar el lastpos
def lastpos(node):

    # Para epsilon se regresa un vacio
    if(node.character == "ε"):
        return set()
    # Si es un or se regresa la union de los dos hijos
    elif(node.character == "|"):
        return (lastpos(node.right_child).union(lastpos(node.left_child)))
    # Si es concatenacion se regresa la union si el derecho es nulo, del contrario es el derecho
    elif(node.character == "."):
        if(nullable(node.right_child)):
            return (lastpos(node.right_child).union(lastpos(node.left_child)))
        else:
            return lastpos(node.right_child)
    # Para las cerraduras se regresa el firstpos de su hijo
    elif(node.character in "*+?"):
        return lastpos(node.left_child)
    # Si es un caracter se regresa solo la posicion
    else:
        return {node}

# Se utiliza el algoritmo para el followpos
def followpos(node):
    # Para cada caracter de concatenacion se realiza el algoritmo
    if(node.character == "."):
        # Se toma el lastpos y se itera
        pos_i = lastpos(node.left_child)
        # Para cada posicion que regresa lastpos
        for i in pos_i:
            # Se agrega la union del followpos con el firstpos del nodo derecho
            i.followpos = i.followpos.union(firstpos(node.right_child))
    # Para los caracteres de cerradura se realiza lo siguiente
    elif(node.character in "*+"):
        # Se toma lastpos y se itera
        pos_i = lastpos(node.left_child)
        # Para cada posicion que regresa lastpos
        for i in pos_i:
            # Se agrega la union del followpos con el firstpos del nodo derecho
            i.followpos = i.followpos.union(firstpos(node.left_child))

def computeProperties(nodes):
    for node in nodes:
        node.nullable = nullable(node)
        node.firstpos = firstpos(node)
        node.lastpos = lastpos(node)
        followpos(node)

def getSymbols(regex):

    symbols = []

    for i in regex:
        if(i not in symbols and i not in ".|*+?()"):
            symbols.append(i)

    return symbols


# Se utiliza el algoritmo para la construccion directa
def afdConstruction(regex):
    # Se crea el arbol
    tree = SyntaxTree(regex)
    # Se obtiene la raiz y la lista de nodos
    tree_root = tree.tree_root
    node_list = tree.node_list
    # Se crean los estados y transiciones del AFD
    states = ["S0"]
    transitions = []
    final_states = []
    symbols = getSymbols(regex)

    # Se ejecutan las propiedades de los nodos
    computeProperties(node_list)
    
    # Se crea dstates
    Dstates = [firstpos(tree_root)]
    state_counter = 0
    # Mientras no haya ninguno marcado se continua
    while(state_counter != len(Dstates)):
        # Se itera por cada simbolo
        for symbol in symbols:
            # Se crea el nuevo set
            new_state = set()
            # Por cada nodo de dstates
            for node in Dstates[state_counter]:
                # Une cada followpos
                if(node.character == symbol):
                    new_state = new_state.union(node.followpos)
            # Si el nuevo estado es vacio no se toma en cuenta
            if(len(new_state) != 0):
                # Si el estado no esta en Dstates se ingresa
                if(new_state not in Dstates):
                    Dstates.append(new_state)
                    states.append("S" + str(len(states)))
                # Se busca el estado de transicion
                new_state_counter = Dstates.index(new_state)
                # Se realiza la transicion
                transitions.append([states[state_counter], symbol, states[new_state_counter]])

        # Se hacen dos sets para lograr hacer operaciones de conjuntos entre ellos
        set_states = set(Dstates[state_counter])
        set_final_states = set(lastpos(tree_root))

        # Se verifica que los estados encontrados se encuentren en el conjunto de estados finales
        if(set_states.intersection(set_final_states).__len__() != 0):
            final_states.append(states[state_counter])

        # Se agrega un contador para marcar los estados
        state_counter += 1

        

    # Se crea el AFD
    afd = AFD("AFD Directo")
    afd.regex = regex
    afd.states = states
    afd.transitions = transitions
    afd.initial_state = states[0]
    afd.final_state = final_states
    afd.graphAF()
