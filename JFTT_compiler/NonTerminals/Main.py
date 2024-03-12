from NonTerminals.Declarations import VarDeclaration
from typing import List
from MemoryManager import MemoryManager


class Main:

    def __init__(self, declarations: List[VarDeclaration], commands):
        self.declarations = declarations
        self.commands = commands
        self.instructions = []
