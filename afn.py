from regex import *
from graphviz import Digraph
from afd import *

class AFN(object):

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
        self.thompsonConstruction()
        self.orderTransitions()
        self.graphAF()
        self.subsetConstruction()


    def thompsonConstruction(self):
        
        # El caracter que se toma es el ultimo del stack de toda la operacion en postfix
        # Se toma un caracter para conocer la operacion a realizar
        character = self.characters_stack.pop()

        # Dependiendo de la operacion se realiza cada una de las funciones
        if(character == '.'):
            return self.concatenation()
        elif(character == '|'):
            return self.union()
        elif(character == '*'):
            return self.kleene()
        elif(character == '+'):
            return self.positive()
        elif(character == '?'):
            return self.nullable()
        elif(len(self.characters_stack) == 0):
            return self.singleState(character)

    def singleState(self, symbol):
        
        # Se ingresa el simbolo a la lista de simbolos
        if(symbol not in self.symbols):
            self.symbols.append(symbol)

        # Se crea un nuevo estado inicial
        self.states_counter += 1
        # Se cuida que no se repitan estados en la lista
        if(self.states_counter not in self.states):
            self.states.append(self.states_counter)
        initial_state = self.states_counter

        # Se crea un nuevo estado final
        self.states_counter += 1
        # Se cuida que no se repitan estados en la lista
        if(self.states_counter not in self.states):
            self.states.append(self.states_counter)
        final_state = self.states_counter

        # Se realiza la transicion de los estados con el simbolo que se ingreso
        transition = [initial_state, symbol, final_state]
        self.transitions.append(transition)

        return initial_state, final_state


    def concatenation(self):
        
        # Se obtienen los dos caracteres para realizar la operacion
        character_1 = self.characters_stack.pop()
        character_2 = self.characters_stack.pop()
        print(character_1, character_2)

        # Si el primer caracter es otra operacion
        if(character_1 in ".|*+?"):
            
            # Se devuelven los caracteres al stack
            self.characters_stack.append(character_2)
            self.characters_stack.append(character_1)

            # Los estados para la operacion se obtiene de manera recursiva
            # Se vuelve a utilizar la funcion para operar dentro de la misma
            initial_state_1, final_state_1 = self.thompsonConstruction()
            # Se resta un estado para concaternar 
            self.states_counter -= 1
            initial_state_2, final_state_2 = self.thompsonConstruction()

        # Si el segundo caracter es una operacion
        elif(character_2 in ".|*+?"):

            # Se regresa el caracter al stack
            self.characters_stack.append(character_2)

            # Se crea el otro estado de manera singular
            initial_state_1, final_state_1 = self.singleState(character_1)
            # Se resta un estado para concaternar 
            self.states_counter -= 1
            # Se obtienen los estados de manera recursiva
            initial_state_2, final_state_2 = self.thompsonConstruction()
        
        # Si es una concatenacion normal
        else:
            # Se crea el otro estado de manera singular
            initial_state_1, final_state_1 = self.singleState(character_1)
            # Se resta un estado para concaternar 
            self.states_counter -= 1
            # Se crea el otro estado de manera singular
            initial_state_2, final_state_2 = self.singleState(character_2)

        return initial_state_1, final_state_2

    def union(self):
        
        # Se obtienen los dos caracteres para realizar la operacion
        character_1 = self.characters_stack.pop()
        character_2 = self.characters_stack.pop()

        # Se crea el estado inicial de la operacion
        self.states_counter += 1
        transition_state_1 = self.states_counter
        if(self.states_counter not in self.states):
            self.states.append(self.states_counter)

        # Si el primer caracter es otra operacion
        if(character_1 in ".|*+?"):
            
            # Se devuelven los caracteres al stack
            self.characters_stack.append(character_2)
            self.characters_stack.append(character_1)

            # Los estados para la operacion se obtiene de manera recursiva
            # Se vuelve a utilizar la funcion para operar dentro de la misma
            initial_state_1, final_state_1 = self.thompsonConstruction()
            initial_state_2, final_state_2 = self.thompsonConstruction()
        
        # Si el segundo caracter es una operacion
        elif(character_2 in ".|*+?"):

            # Se regresa el caracter al stack
            self.characters_stack.append(character_2)

            # Se obtienen los estados de manera recursiva
            initial_state_1, final_state_1 = self.thompsonConstruction()
            # Se crea el otro estado de manera singular
            initial_state_2, final_state_2 = self.singleState(character_1)

        # Si no existe operaciones dentro de la operacion
        else:
            
            # Se crean los estados singulares
            initial_state_1, final_state_1 = self.singleState(character_2)
            initial_state_2, final_state_2 = self.singleState(character_1)

        # Se obtiene el ultimo estado de la operacion
        self.states_counter += 1
        transition_state_2 = self.states_counter
        if(self.states_counter not in self.states):
            self.states.append(self.states_counter)    

        # Se realizan las transiciones por medio de la forma de la union
        # Esto por los estados que devuelven las operaciones
        transition_1 = [transition_state_1, "ε", initial_state_1]
        transition_2 = [transition_state_1, "ε", initial_state_2]
        transition_3 = [final_state_1, "ε", transition_state_2]
        transition_4 = [final_state_2, "ε", transition_state_2]

        # Se guardan las transiciones en la lista
        self.transitions.extend((transition_1, transition_2, transition_3, transition_4))

        # Se regresa el primer y ultimo estado, esto para la recursividad
        return transition_state_1, transition_state_2


    def kleene(self):
        
        # Se obtiene un caracter para kleene
        character_1 = self.characters_stack.pop()

        # Se crea el estado inicial de la operacion
        self.states_counter += 1
        transition_state_1 = self.states_counter
        if(self.states_counter not in self.states):
            self.states.append(self.states_counter)

        # Si el caracter 1 es una operacion
        if(character_1 in ".|*+?"):

            # Se regresa al stack el operador
            self.characters_stack.append(character_1)
            # Se obtienen de manera recursiva los estados
            initial_state_1, final_state_1 = self.thompsonConstruction()

        # Se el caracter no es una operacion
        else: 
            
            # Se realiza el estado singular
            initial_state_1, final_state_1 = self.singleState(character_1)

        # Se obtiene el estado final de la operacion
        self.states_counter += 1
        transition_state_2 = self.states_counter
        if(self.states_counter not in self.states):
            self.states.append(self.states_counter)

        # Se realizan las transiciones correspondientes para kleene
        transition_1 = [final_state_1, "ε", initial_state_1]
        transition_2 = [transition_state_1, "ε", initial_state_1]
        transition_3 = [final_state_1, "ε", transition_state_2]
        transition_4 = [transition_state_1, "ε", transition_state_2]

        # Se guardan las transiciones en la lista
        self.transitions.extend((transition_1, transition_2, transition_3, transition_4))
        
        # Se regresa el primer y ultimo estado, esto para la recursividad
        return transition_state_1, transition_state_2

    def positive(self):
        
        # Se obtiene un caracter para cerradura positiva
        character_1 = self.characters_stack.pop()

        # Se crea el estado inicial de la operacion
        self.states_counter += 1
        transition_state_1 = self.states_counter
        if(self.states_counter not in self.states):
            self.states.append(self.states_counter)

        # Si el caracter 1 es una operacion
        if(character_1 in ".|*+?"):

            # Se regresa al stack el operador
            self.characters_stack.append(character_1)
            # Se obtienen de manera recursiva los estados
            initial_state_1, final_state_1 = self.thompsonConstruction()

        # Se el caracter no es una operacion
        else: 
            
            # Se realiza el estado singular
            initial_state_1, final_state_1 = self.singleState(character_1)

        # Se obtiene el estado final de la operacion
        self.states_counter += 1
        transition_state_2 = self.states_counter
        if(self.states_counter not in self.states):
            self.states.append(self.states_counter)

        # Se realizan las transiciones correspondientes para cerradura positiva
        transition_1 = [final_state_1, "ε", initial_state_1]
        transition_2 = [transition_state_1, "ε", initial_state_1]
        transition_3 = [final_state_1, "ε", transition_state_2]

        # Se guardan las transiciones en la lista
        self.transitions.extend((transition_1, transition_2, transition_3))
        
        # Se regresa el primer y ultimo estado, esto para la recursividad
        return transition_state_1, transition_state_2


    def nullable(self):

        # Se obtiene un caracter para nullable
        character_1 = self.characters_stack.pop()

        # Se crea el estado inicial de la operacion
        self.states_counter += 1
        transition_state_1 = self.states_counter
        if(self.states_counter not in self.states):
            self.states.append(self.states_counter)

        # Si el caracter 1 es una operacion
        if(character_1 in ".|*+?"):

            # Se regresa al stack el operador
            self.characters_stack.append(character_1)
            # Se obtienen de manera recursiva los estados
            initial_state_1, final_state_1 = self.thompsonConstruction()

        # Si el caracter no es una operacion
        else: 
            
            # Se realiza el estado singular
            initial_state_1, final_state_1 = self.singleState(character_1)
        
        initial_state_2, final_state_2 = self.singleState("ε")

        # Se obtiene el estado final de la operacion
        self.states_counter += 1
        transition_state_2 = self.states_counter
        if(self.states_counter not in self.states):
            self.states.append(self.states_counter)

        # Se realizan las transiciones por medio de la forma de la nullable
        # Esto por los estados que devuelven las operaciones
        transition_1 = [transition_state_1, "ε", initial_state_1]
        transition_2 = [transition_state_1, "ε", initial_state_2]
        transition_3 = [final_state_1, "ε", transition_state_2]
        transition_4 = [final_state_2, "ε", transition_state_2]

        # Se guardan las transiciones en la lista
        self.transitions.extend((transition_1, transition_2, transition_3, transition_4))

        # Se regresa el primer y ultimo estado, esto para la recursividad
        return transition_state_1, transition_state_2
    

    # Se realiza la simulacion con el algoritmo del libro
    def simulation(self, string):
        # Se inicializan los estados con e_closure del inicial
        states = self.e_closure(self.initial_state)
        # Se inicia el conteo de caracteres de la cadena
        character_count = 0

        # Mientras hayan caracteres para verificar en el string
        while(character_count < len(string)):
            # Se toman los estados devueltos por e_closure del move con el caracter
            states = self.e_closure(self.move(states, string[character_count]))
            # Se pasa al siguiente caracter
            character_count += 1

        # Se hacen dos sets para lograr hacer operaciones de conjuntos entre ellos
        set_states = set(states)
        set_final_states = set(self.final_state)

        # Se verifica que los estados encontrados se encuentren en el conjunto de estados finales
        if(set_states.intersection(set_final_states).__len__() != 0):
            return "Cadena Aceptada"
        else:
            return "Cadena No Aceptada"
    
    # Se realiza SubSet Construction con el Algoritmo brindado
    def subsetConstruction(self):
        # Se inicializa con el Estado 0 y sin transiciones
        states = ["S0"]
        transitions = []
        final_states = []

        # Se inicializa Dstate con el e-closure
        Dstates = [self.e_closure(self.initial_state)]
        # Se tiene un state counter para marcar Dstates
        state_counter = 0

        # Mientras no haya ninguno marcado se continua
        while(state_counter != len(Dstates)):
            # Se itera por cada simbolo
            for symbol in self.symbols:
                # Se consigue el nuevo estado
                new_state = self.e_closure(self.move(Dstates[state_counter], symbol))
                # Se verifica que no sea un "estado muerto"
                if(len(new_state) != 0):
                    # Se ingresa el estado si no se encuentra en Dstates
                    if (new_state not in Dstates):
                        Dstates.append(new_state)
                        states.append("S" + str(len(states)))
                    
                    # Se busca el estado de transicion
                    new_state_counter = Dstates.index(new_state)
                    # Se realiza la transicion
                    transitions.append([states[state_counter], symbol, states[new_state_counter]])

            # Se hacen dos sets para lograr hacer operaciones de conjuntos entre ellos
            set_states = set(Dstates[state_counter])
            set_final_states = set(self.final_state)
            print(states[state_counter])
            print(set_states)
            print(set_final_states)

            # Se verifica que los estados encontrados se encuentren en el conjunto de estados finales
            if(set_states.intersection(set_final_states).__len__() != 0):
                final_states.append(states[state_counter])
            
            state_counter += 1

        # Se crea el AFD
        afd = AFD()
        afd.regex = self.regex
        afd.states = states
        afd.transitions = transitions
        afd.initial_state = states[0]
        afd.final_state = final_states
        afd.graphAF()
        
    
    # Se utiliza el algoritmo del libro para calcular e-closure
    def e_closure(self, states):
        # Se inicia el stack con los estados de T
        states_stack = list(states)
        # Se inicia el resultado con el estado T
        states_result = list(states)

        # Se itera mientra el stack no se encuentre vacio
        while(len(states_stack) != 0):
            # Se saca el estado t
            state = states_stack.pop()
            # Se revisa en cada transicion
            for i in self.transitions:
                # Se revisa que tenga transicion con ε 
                if(i[0] == state and i[1] == "ε"):
                    # Si el estado no esta en los resultados se ingresa
                    if(i[2] not in states_result):
                        states_result.append(i[2])
                        states_stack.append(i[2])
        
        # Se retorna el resultado
        return states_result
    
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
                # Se revisa que tenga transicion con ε 
                if(i[0] == state and i[1] == character):
                    # Si el estado no esta en los resultados se ingresa
                    if(i[2] not in states_result):
                        states_result.append(i[2])
                        states_stack.append(i[2])
        
        # Se retorna el resultado
        return states_result

    # Funcion realizada para ordenar las transiciones de manera que se puedan visualizar
    # con un orden de 1 a N estados
    def orderTransitions(self):
        
        # Se guardan los estados inicial y final
        self.initial_state.append(self.states[0])
        self.final_state.append(self.states_counter)

        # Se itera en las transiciones existentes
        for transition in self.transitions:
            transition_1 = transition[0]
            transition_2 = transition[2]
            
            # Se cambia el orden para cada transicion con respecto a los numeros de estados
            transition[0] = self.states[len(self.states) - transition_2]
            transition[2] = self.states[len(self.states) - transition_1]

    # Funcion para graficar el automata
    def graphAF(self):
        
        # Se realiza el titulo del automata
        description = ("AFN de la Expresión " + self.regex)
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
        graph.render("./images/AFN", format="png", view=True)