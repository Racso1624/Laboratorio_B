from regex import *

class SyntaxTree():

    def __init__(self, regex):
        self.regex = regex
        self.replaceNullable()
        self.postfix =  Regex(self.regex).postfix_expression + "#."

    
    def replaceNullable(self):
        
        expression = self.regex

        while(expression.count('?') != 0):
            index = expression.index('?')
            character = expression[index - 1]
            string = character + "?"
            new_string = f"({character}|ε)"
            expression =  expression.replace(string, new_string)

        self.regex = expression

class Node:
    
    def __init__(self, character, firstpos, lastpos):
        self.character = character
        self.firstpos = firstpos
        self.lastpos = lastpos
