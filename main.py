# Oscar Fernando López Barrios
# Carné 20679

from afn import *
from afd_construction import *
from afd_minimization import *

#text = "(a(a?b*|c+)b|baa)"
text = "(a|b)*abb"
#text = "0?(1|ε)?0*"
#text = "(b|b)*abb(a|b)*"

afdConstruction(text)

afn = AFN(text)
afn_to_afd = afn.subsetConstruction()
afdMinimization(afn_to_afd)