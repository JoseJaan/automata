from automata.fa.dfa import DFA
from automata.fa.nfa import NFA
from automata.pda.dpda import DPDA
from automata.tm.dtm import DTM

def visualize_automata(automata):
    if isinstance(automata, (DFA, NFA, DPDA, DTM)):
        try:
            diagram = automata.show_diagram()
            return diagram
        except AttributeError:
            raise ValueError(f"The automaton of type {type(automata).__name__} does not support diagram visualization.")
    else:
        raise ValueError("Unsupported automaton type for visualization")