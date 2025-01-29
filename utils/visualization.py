from automata.fa.dfa import DFA
from automata.fa.nfa import NFA
from automata.pda.dpda import DPDA
from automata.tm.dtm import DTM

def visualize_automata(automata):
    if isinstance(automata, (DFA, NFA, DPDA, DTM)):
        return automata.show_diagram()
    else:
        raise ValueError("Unsupported automata type for visualization")