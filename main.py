# Oscar Fernando López Barrios
# Carné 20679

from afn import *

text = "(a(a?b*|c+)b|baa)"

afn = AFN(text)
print(afn.transitions)
print(afn.states)