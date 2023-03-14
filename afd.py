from regex import *
from graphviz import Digraph

class AFD(object):

    def __init__(self, regex):
        self.regex = regex
        self.postfix_expression = Regex(regex).postfix_expression
        print(self.postfix_expression)
        self.characters_stack = list(self.postfix_expression)
        self.states_counter = 0
        self.states = []
        self.transitions = []
        self.initial_state = []
        self.final_state = []
        self.symbols = []
        self.graphAF()
    
    # Funcion para graficar el automata
    def graphAF(self):
        
        # Se realiza el titulo del automata
        description = ("AFD de la Expresión " + self.regex)
        graph = Digraph()
        graph.attr(rankdir="LR", labelloc="t", label=description)

        # Por cada estado se crea la imagen para graficarlo
        for state in self.states:

            if(state in self.initial_state):
                graph.node(str(state), str(state), shape="circle", style="filled")
            elif(state in self.final_state):
                graph.node(str(state), str(state), shape="doublecircle", style="filled")
            else:
                graph.node(str(state), str(state), shape="circle")

        # Se coloca el inicio del automata
        graph.edge("INICIO", str(self.initial_state[0]))

        # Se crean las transiciones de los estados
        for transition in self.transitions:
            graph.edge(str(transition[0]), str(transition[2]), label=transition[1])

        # Se renderiza
        graph.render("./images/AFD", format="png", view=True)