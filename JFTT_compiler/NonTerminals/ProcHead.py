from typing import List
from NonTerminals.Declarations import ParamDeclaration


class ProcHead:
    def __init__(self, pid, args_declarations: List[ParamDeclaration], line_number=-1):
        self.pid = pid
        self.line_number = line_number
        for declaration in args_declarations:
            declaration.parent_procedure = pid
        self.args_declarations = args_declarations
