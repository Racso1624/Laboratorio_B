# Oscar Fernando López Barrios
# Carné 20679

from afn import *
from afd_construction import *
from afd_minimization import *

#text = "(a(a?b*|c+)b|baa)"
#text = "0?(1|ε)?0*"
#text = "(b|b)*abb(a|b)*"
text = "(a|b)*abb"
string = "abb"
#text = "(a|b)*a(a|b)(a|b)"
title = " Prueba"

afd = afdConstruction(text, title)
afn = AFN(text, title)
afn.simulation(string)
afn_to_afd = afn.subsetConstruction()
afdMinimization(afn_to_afd, "Minimizado AFD de AFN", title)
afdMinimization(afd, "Minimizado AFD Directo", title)