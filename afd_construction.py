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
        # Para cada 
        for i in pos_i:
            i.followpos.add(firstpos(node.right_child))
    elif(node.character in "*+"):
        pos_i = lastpos(node.left_child)
        for i in pos_i:
            i.followpos.add(firstpos(node.left_child))
    else:
        return set()
    
def afd_construction(regex):
    tree = SyntaxTree(regex)
    for i in tree.node_list:
        print(firstpos(i))
