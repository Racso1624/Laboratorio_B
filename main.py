# Oscar Fernando López Barrios
# Carné 20679

from afn import *

#text = "(a(a?b*|c+)b|baa)"
text = "a|b"

afn = AFN(text)
print(afn.transitions)
print(afn.states)