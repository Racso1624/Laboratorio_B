# Oscar Fernando López Barrios
# Carné 20679

from afn import *
from syntaxtree import *

text = "(a(a?b*|c+)b|baa)"
#text = "(a|b)*abb"
#text = "a?"

tree = SyntaxTree(text)

afn = AFN(text)
print(afn.transitions)
print(afn.states)