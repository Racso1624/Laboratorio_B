# Oscar Fernando López Barrios
# Carné 20679

from afn import *
from afd_construction import *

#text = "(a(a?b*|c+)b|baa)"
#text = "(a|b)*abb"
#text = "a?"
text = "(a*)+"

afdConstruction(text)

afn = AFN(text)
print(afn.transitions)
print(afn.states)