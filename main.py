# Oscar Fernando López Barrios
# Carné 20679

from afn import *
from afd_construction import *
from afd_minimization import *

# text = "(a|ε)b(a+)c?"
# text = "(b|b)*abb(a|b)*"
# text = "b*ab?"
# text = "b+abc+"
# text = "((1?)*)*"
# text = "0(0|1)*0"
# text = "0?(1|ε)?0*"
# text = "b*a(b|a)"
# text = "(a|b)*abb"
text = "b*ab?"
string = "a"
title = " Prueba"

afd = afdConstruction(text, title)
afn = AFN(text, title)
afd.simulation(string)
afn.simulation(string)
afn_to_afd = afn.subsetConstruction()
afdMinimization(afn_to_afd, "Minimizado AFD de AFN", title)
afdMinimization(afd, "Minimizado AFD Directo", title)