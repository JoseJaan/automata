from automata.fa.dfa import DFA
from automata.fa.nfa import NFA
from automata.pda.dpda import DPDA
from automata.tm.dtm import DTM
import uuid
import os
import pygraphviz as pgv

class Automata:
    def __init__(self, id, type, config):
        self.id = id
        self.type = type
        self.config = config

        if type == "DFA":
            self.instance = DFA(
                states=config["states"],
                input_symbols=config["input_symbols"],
                transitions=config["transitions"],
                initial_state=config["initial_state"],
                final_states=config["final_states"]
            )
        elif type == "NFA":
            self.instance = NFA(
                states=config["states"],
                input_symbols=config["input_symbols"],
                transitions=config["transitions"],
                initial_state=config["initial_state"],
                final_states=config["final_states"]
            )
        elif type == "DPDA":
            self.instance = DPDA(**config)
        elif type == "DTM":
            self.instance = DTM(**config)
        else:
            raise ValueError("Invalid automata type")
        
    def validate_string(self, input_string):
        try:
            if self.type in ["DFA", "NFA"]:
                return self.instance.accepts_input(input_string)
            elif self.type == "DPDA":
                return self.instance.accepts_input(input_string)
            elif self.type == "DTM":
                return self.instance.accepts_input(input_string)
            else:
                raise ValueError(f"Validation not implemented for type {self.type}")
        except Exception as e:
            raise ValueError(f"Error validating string: {str(e)}")
    
    def generate_image(self, save_path):
        try:
            diagram = self.instance.show_diagram()
            diagram.draw(f"{save_path}.png", prog='dot', format='png')
            return f"{save_path}.png"
        except Exception as e:
            raise ValueError(f"Erro ao gerar imagem do autômato: {str(e)}")

    def show_diagram(self):
        return self.instance.show_diagram()

class AutomataManager:
    def __init__(self):
        self.automatas = {}

    def create_automata(self, type, config):
        automata_id = str(uuid.uuid4())

        # Convert lists to sets for automata-lib compatibility
        config["states"] = set(config["states"])
        config["input_symbols"] = set(config["input_symbols"])
        config["final_states"] = set(config["final_states"])

        automata = Automata(automata_id, type, config)
        self.automatas[automata_id] = automata
        return automata

    def get_automata(self, automata_id):
        return self.automatas.get(automata_id)