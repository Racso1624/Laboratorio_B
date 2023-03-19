from syntaxtree import *

def nullable(node):

    if(node.character in "ε?*"):
        return True
    elif(node.character == "|"):
        return (nullable(node.left_child) or nullable(node.right_child))
    elif(node.character == "."):
        return (nullable(node.left_child) and nullable(node.right_child))
    elif(node.character == "+"):
        return nullable(node.left_child)
    else:
        return False
    
def firstpos(node):

    if(node.character == "ε"):
        return set()
    elif(node.character == "|"):
        return (firstpos(node.right_child).union(node.left_child))
    elif(node.character == "."):
        if(nullable(node.left_child)):
            return (firstpos(node.right_child).union(node.left_child))
        else:
            return firstpos(node.left_child)
    elif(node.character in "*+?"):
        return firstpos(node.left_child)
    else:
        return {node.position}
    
def lastpos(node):

    if(node.character == "ε"):
        return set()
    elif(node.character == "|"):
        return (firstpos(node.right_child).union(node.left_child))
    elif(node.character == "."):
        if(nullable(node.right_child)):
            return (firstpos(node.right_child).union(node.left_child))
        else:
            return firstpos(node.right_child)
    elif(node.character in "*+?"):
        return firstpos(node.left_child)
    else:
        return {node.position}
    
def followpos(node):
    
    if(node.character == "."):
        pos_i = lastpos(node.left_child)
        for i in pos_i:
            i.followpos.add(firstpos(node.right_child))
    elif(node.character in "*+"):
        pos_i = lastpos(node.left_child)
        for i in pos_i:
            i.followpos.add(firstpos(node.left_child))
    else:
        return set()