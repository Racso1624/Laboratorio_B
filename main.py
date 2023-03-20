# Oscar Fernando López Barrios
# Carné 20679

from afn import *
from afd_construction import *
from afd_minimization import *

#text = "(a(a?b*|c+)b|baa)"
text = "ba|b(a*)"
#text = "0?(1|ε)?0*"
#text = "(b|b)*abb(a|b)*"
#text = "(a|b)*abb"
string = "aaa"

afdConstruction(text)
afn = AFN(text)
afn_to_afd = afn.subsetConstruction()
afdMinimization(afn_to_afd, "Minimizado AFD de AFN")