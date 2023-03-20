from regex import *
from graphviz import Digraph

class AFD(object):

    def __init__(self, name, title):
        self.regex = None
        self.states_counter = 0
        self.states = []
        self.transitions = []
        self.initial_state = []
        self.final_state = []
        self.symbols = []
        self.afd_name = name
        self.title = title

    # Se realiza la simulacion con el algoritmo del libro
    def simulation(self, string):
        # Se inicializan los estados con e_closure del inicial
        states = self.initial_state
        # Se inicia el conteo de caracteres de la cadena
        character_count = 0

        # Mientras hayan caracteres para verificar en el string
        while(character_count < len(string)):
            # Se toman los estados devueltos por e_closure del move con el caracter
            states = self.move(states, string[character_count])
            # Se pasa al siguiente caracter
            character_count += 1

        # Se hacen dos sets para lograr hacer operaciones de conjuntos entre ellos
        set_states = set(states)
        set_final_states = set(self.final_state)

        # Se verifica que los estados encontrados se encuentren en el conjunto de estados finales
        if(set_states.intersection(set_final_states).__len__() != 0):
            print("Cadena Aceptada")
        else:
            print("Cadena No Aceptada") 
    
    # Se utiliza el algoritmo de e-closure para calcular move
    def move(self, states, character):
        # Se inicia el stack con los estados de T
        states_stack = list(states)
        # Se inicia sin estados
        states_result = []

        # Se itera mientra el stack no se encuentre vacio
        while(len(states_stack) != 0):
            # Se saca el estado t
            state = states_stack.pop()
            # Se revisa en cada transicion
            for i in self.transitions:
                # Se revisa que tenga transicion con el caracter
                if(i[0] == state and i[1] == character):
                    # Si el estado no esta en los resultados se ingresa
                    if(i[2] not in states_result):
                        states_result.append(i[2])
        # Se retorna el resultado
        return states_result

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
            if(state in self.final_state):
                graph.node(str(state), str(state), shape="doublecircle", style="filled")
            else:
                graph.node(str(state), str(state), shape="circle")

        # Se crean las transiciones de los estados
        for transition in self.transitions:
            graph.edge(str(transition[0]), str(transition[2]), label=transition[1])

        # Se renderiza
        graph.render(f"./images/{self.afd_name}" + self.title, format="png", view=True)