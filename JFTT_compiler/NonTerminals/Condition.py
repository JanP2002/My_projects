import Instructions
from NonTerminals.Identifier import Identifier
from Register import REG
from enum import Enum


class COP(Enum):
    LT = "<"
    GT = ">"
    LE = "<="
    GE = ">="
    EQ = "="
    NE = "!="

    def __str__(self):
        return self.value


def generate_compare(cop: COP):
    asm_code = []
    negation_mode = False
    if cop == COP.LT.value:
        asm_code.append(Instructions.makeInstr('GET', REG.D))
        asm_code.append(Instructions.makeInstr('SUB', REG.C))
    elif cop == COP.GT.value:
        asm_code.append(Instructions.makeInstr('GET', REG.C))
        asm_code.append(Instructions.makeInstr('SUB', REG.D))
    elif cop == COP.LE.value: # not C > D:
        asm_code.append(Instructions.makeInstr('GET', REG.C))
        asm_code.append(Instructions.makeInstr('SUB', REG.D))
        negation_mode = True
    elif cop == COP.GE.value: # not C < D
        asm_code.append(Instructions.makeInstr('GET', REG.D))
        asm_code.append(Instructions.makeInstr('SUB', REG.C))
        negation_mode = True
    elif cop == COP.EQ.value:
        asm_code.append(Instructions.GET(REG.C))
        asm_code.append(Instructions.SUB(REG.D))
        asm_code.append(Instructions.PUT(REG.E))
        asm_code.append(Instructions.GET(REG.D))
        asm_code.append(Instructions.SUB(REG.C))
        asm_code.append(Instructions.ADD(REG.E))
        negation_mode = True
    elif cop == COP.NE.value:
        asm_code.append(Instructions.GET(REG.C))
        asm_code.append(Instructions.SUB(REG.D))
        asm_code.append(Instructions.PUT(REG.E))
        asm_code.append(Instructions.GET(REG.D))
        asm_code.append(Instructions.SUB(REG.C))
        asm_code.append(Instructions.ADD(REG.E))
    else:
        raise Exception("Nieprawidlowa operacja")

    return [asm_code, negation_mode]


class Condition:
    def __init__(self, val1, val2, compare_op, line_number, parent_proc=None):
        self.compare_operator = compare_op
        self.val1 = val1
        self.val2 = val2
        self.parent_proc = parent_proc
        self.line_number = line_number
        self.negation_mode = False

    def translate(self, program):
        raise Exception("generateCode() not defined for %s" % self.__class__)


class ConditionNumNum(Condition):
    def __init__(self, val1, val2, compare_op, line_number):
        super(ConditionNumNum, self).__init__(val1, val2, compare_op, line_number)

    def translate(self, p):
        asm_code = []
        if self.compare_operator == COP.LT.value:
            if self.val1 < self.val2:
                asm_code.extend(Instructions.set_register_const(REG.A, 1))
            else:
                asm_code.extend(Instructions.set_register_const(REG.A, 0))
        elif self.compare_operator == COP.GT.value:
            if self.val1 > self.val2:
                asm_code.extend(Instructions.set_register_const(REG.A, 1))
            else:
                asm_code.extend(Instructions.set_register_const(REG.A, 0))
        elif self.compare_operator == COP.GE.value:
            if self.val1 >= self.val2:
                asm_code.extend(Instructions.set_register_const(REG.A, 1))
            else:
                asm_code.extend(Instructions.set_register_const(REG.A, 0))
        elif self.compare_operator == COP.LE.value:
            if self.val1 <= self.val2:
                asm_code.extend(Instructions.set_register_const(REG.A, 1))
            else:
                asm_code.extend(Instructions.set_register_const(REG.A, 0))
        elif self.compare_operator == COP.EQ.value:
            if self.val1 == self.val2:
                asm_code.extend(Instructions.set_register_const(REG.A, 1))
            else:
                asm_code.extend(Instructions.set_register_const(REG.A, 0))
        elif self.compare_operator == COP.NE.value:
            if self.val1 != self.val2:
                asm_code.extend(Instructions.set_register_const(REG.A, 1))
            else:
                asm_code.extend(Instructions.set_register_const(REG.A, 0))

        return asm_code


class ConditionIdentifierNum(Condition):
    def __init__(self, val1: Identifier, val2, compare_op, line_number):
        super(ConditionIdentifierNum, self).__init__(val1, val2, compare_op, line_number)

    def translate(self, p):
        self.val1.set_parent_procedure(self.parent_proc)
        asm_code = []
        asm_code.extend(self.val1.translate_left_cond_get_value())
        asm_code.extend(Instructions.set_register_const(REG.D, self.val2))
        compare_obj = generate_compare(self.compare_operator)
        asm_code.extend(compare_obj[0])
        self.negation_mode = compare_obj[1]
        return asm_code


class ConditionNumIdentifier(Condition):
    def __init__(self, val1, val2: Identifier, compare_op, line_number):
        super(ConditionNumIdentifier, self).__init__(val1, val2, compare_op, line_number)

    def translate(self, p):
        self.val1.set_parent_procedure(self.parent_proc)
        asm_code = []
        asm_code.extend(Instructions.set_register_const(REG.C, self.val1))
        asm_code.extend(self.val2.translate_right_cond_get_value())
        compare_obj = generate_compare(self.compare_operator)
        asm_code.extend(compare_obj[0])
        self.negation_mode = compare_obj[1]
        return asm_code


class ConditionIdentifierIdentifier(Condition):
    def __init__(self, val1: Identifier, val2: Identifier, compare_op, line_number):
        super(ConditionIdentifierIdentifier, self).__init__(val1, val2, compare_op, line_number)

    def translate(self, p):
        self.val1.set_parent_procedure(self.parent_proc)
        self.val2.set_parent_procedure(self.parent_proc)
        asm_code = []
        asm_code.extend(self.val1.translate_left_cond_get_value())
        asm_code.extend(self.val2.translate_right_cond_get_value())
        compare_obj = generate_compare(self.compare_operator)
        asm_code.extend(compare_obj[0])
        self.negation_mode = compare_obj[1]
        return asm_code
