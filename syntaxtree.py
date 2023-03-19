from regex import *

class SyntaxTree():

    def __init__(self, regex):
        self.regex = regex
        self.postfix =  Regex(self.regex).postfix_expression + "#."
        self.node_list = []
        self.tree_root = None

    def buildTree(self):
        
        node_stack = []
        position_counter = 1

        for character in self.postfix:
            
            if(character in "+*?"):
                new_node = Node(character)
                new_node.left_child(node_stack.pop())
                node_stack.append(new_node)
                self.node_list.append(new_node)
            elif(character in ".|"):
                new_node = Node(character)
                new_node.right_child(node_stack.pop())
                new_node.left_child(node_stack.pop())
                node_stack.append(new_node)
                self.node_list.append(new_node)
            else:
                new_node = Node(character, position_counter)
                node_stack.append(new_node)
                self.node_list.append(new_node)
        
        self.tree_root = node_stack.pop()


class Node:
    
    def __init__(self, character, position = None):
        self.character = character
        self.firstpos = set()
        self.lastpos = set()
        self.followpos = set()
        self.position = position
        self.left_child = None
        self.right_child = None