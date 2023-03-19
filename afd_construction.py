from syntaxtree import *

def nullable(node):

    if(node.character in "ε?*"):
        return True
    elif(node.character == "|"):
        return (nullable(node.left_child) or nullable(node.right_child))
    elif(node.character == "."):
        return (nullable(node.left_child) and nullable(node.right_child))