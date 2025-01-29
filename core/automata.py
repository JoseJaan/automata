from automata.fa.dfa import DFA
from automata.fa.nfa import NFA
from automata.pda.dpda import DPDA
from automata.tm.dtm import DTM
import uuid

class Automata:
    def __init__(self, id, type, config):
        self.id = id
        self.type = type
        self.config = config

class AutomataManager:
    def __init__(self):
        self.automatas = {}

    def create_automata(self, type, config):
        automata_id = str(uuid.uuid4())

        # Convert lists to sets for automata-lib compatibility
        config["states"] = set(config["states"])
        config["input_symbols"] = set(config["input_symbols"])
        config["final_states"] = set(config["final_states"])

        if type == "DFA":
            automata = DFA(
                states=config["states"],
                input_symbols=config["input_symbols"],
                transitions=config["transitions"],
                initial_state=config["initial_state"],
                final_states=config["final_states"]
            )
        elif type == "NFA":
            automata = NFA(
                states=config["states"],
                input_symbols=config["input_symbols"],
                transitions=config["transitions"],
                initial_state=config["initial_state"],
                final_states=config["final_states"]
            )
        elif type == "DPDA":
            automata = DPDA(**config)
        elif type == "DTM":
            automata = DTM(**config)
        else:
            raise ValueError("Invalid automata type")

        self.automatas[automata_id] = Automata(automata_id, type, config)
        return self.automatas[automata_id]