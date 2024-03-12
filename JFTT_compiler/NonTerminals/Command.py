from enum import Enum

import Instructions
from typing import List

from LabelGenerator import LabelGenerator
from NonTerminals.Condition import Condition
from NonTerminals.Identifier import Identifier
from NonTerminals.ProcCallParam import ProcCallParam
from Register import REG


class OP(Enum):
    PLUS = "+"
    MINUS = "-"
    TIMES = "*"
    DIV = "/"
    MOD = "%"

    def __str__(self):
        return self.value


def generate_operation(op: OP):
    asm_code = []
    if op == OP.PLUS.value:
        asm_code.extend(Instructions.generate_adding())
    elif op == OP.MINUS.value:
        asm_code.extend(Instructions.generate_subtraction())
    elif op == OP.TIMES.value:
        asm_code.extend(Instructions.generate_multiplication())
    elif op == OP.DIV.value:
        asm_code.extend(Instructions.generate_division())
    elif op == OP.MOD.value:
        asm_code.extend(Instructions.generate_modulo())
    else:
        raise Exception("Nieprawidlowa operacja")
    return asm_code


class Command:
    def __init__(self, line_number=-1):
        self.line_number = line_number
        self.parent_procedure = None
        self.is_proc_call = False
        self.parent_procedure_label = None

    def set_parent_procedure(self, proc_pid):
        self.parent_procedure = proc_pid

    def set_parent_procedure_label(self, label):
        self.parent_procedure_label = label

    def translate(self, program):
        raise Exception("generateCode() not defined for %s" % self.__class__)


class CommandWriteNum(Command):
    def __init__(self, num, line_number=-1):
        super(CommandWriteNum, self).__init__(line_number)
        self.num = num

    def translate(self, p):
        asm_code = Instructions.set_register_const(REG.A, self.num)
        asm_code.append(Instructions.makeInstr('WRITE'))
        return asm_code


class CommandReadIdentifier(Command):
    def __init__(self, identifier: Identifier, line_number=-1):
        super(CommandReadIdentifier, self).__init__(line_number)
        self.identifier = identifier

    def translate(self, p):
        self.identifier.parent_procedure = self.parent_procedure
        asm_code = []
        asm_code.append(Instructions.makeInstr('READ'))
        asm_code.extend(self.identifier.translate_set_value())
        return asm_code


class CommandWriteIdentifier(Command):
    def __init__(self, identifier: Identifier, line_number=-1):
        super(CommandWriteIdentifier, self).__init__(line_number)
        self.identifier = identifier

    def translate(self, p):
        self.identifier.parent_procedure = self.parent_procedure
        asm_code = []
        asm_code.extend(self.identifier.translate_write_get_value())
        asm_code.append(Instructions.WRITE())
        return asm_code


class CommandIdentifierAssignNum(Command):
    def __init__(self, identifier: Identifier, val, line_number=-1):
        super(CommandIdentifierAssignNum, self).__init__(line_number)
        self.identifier = identifier
        self.val = val

    def translate(self, p):
        self.identifier.parent_procedure = self.parent_procedure
        asm_code = []
        asm_code.extend(Instructions.set_register_const(REG.A, self.val))
        asm_code.extend(self.identifier.translate_set_value())
        return asm_code


class CommandIdentifierAssignIdentifier(Command):
    def __init__(self, l_identifier: Identifier, r_identifier: Identifier, line_number=-1):
        super(CommandIdentifierAssignIdentifier, self).__init__(line_number)
        self.left_identifier = l_identifier
        self.right_identifier = r_identifier

    def translate(self, p):
        self.left_identifier.parent_procedure = self.parent_procedure
        self.right_identifier.parent_procedure = self.parent_procedure
        asm_code = []
        asm_code.extend(self.right_identifier.translate_assign_get_value())
        asm_code.extend(self.left_identifier.translate_set_value())
        return asm_code


class CommandIdentifierAssignNumOpNum(Command):
    def __init__(self, identifier: Identifier, num1, num2, operation, line_number):
        super(CommandIdentifierAssignNumOpNum, self).__init__(line_number)
        self.identifier = identifier
        self.num1 = num1
        self.num2 = num2
        self.operation = operation

    def translate(self, p):
        asm_code = []
        if self.operation == '+':
            result = self.num1 + self.num2
            asm_code.extend(Instructions.set_register_const(REG.A, result))
        elif self.operation == '-':
            result = 0
            if self.num2 < self.num1:
                result = self.num1 - self.num2
            asm_code.extend(Instructions.set_register_const(REG.A, result))
        elif self.operation == "*":
            result = self.num1 * self.num2
            asm_code.extend(Instructions.set_register_const(REG.A, result))
        elif self.operation == '/':
            result = 0
            if self.num2 != 0:
                result = self.num1 // self.num2
            asm_code.extend(Instructions.set_register_const(REG.A, result))
        elif self.operation == '%':
            result = 0
            if self.num2 != 0:
                result = self.num1 % self.num2
            asm_code.extend(Instructions.set_register_const(REG.A, result))
        else:
            raise Exception("Nieprawidlowa operacja")
        asm_code.extend(self.identifier.translate_set_value())
        return asm_code


class CommandIdentifierAssignIdentifierOpNum(Command):
    def __init__(self, identifier: Identifier, val1: Identifier, val2, operation, line_number):
        super(CommandIdentifierAssignIdentifierOpNum, self).__init__(line_number)
        self.identifier = identifier
        self.val1 = val1
        self.val2 = val2
        self.operation = operation

    def translate(self, p):
        self.identifier.parent_procedure = self.parent_procedure
        self.val1.parent_procedure = self.parent_procedure
        asm_code = []
        asm_code.extend(self.val1.translate_left_op_get_value())
        asm_code.extend(Instructions.set_register_const(REG.E, self.val2))
        asm_code.extend(generate_operation(self.operation))
        asm_code.extend(self.identifier.translate_set_value())
        return asm_code


class CommandIdentifierAssignNumOpIdentifier(Command):
    def __init__(self, identifier: Identifier, val1, val2: Identifier, operation, line_number):
        super(CommandIdentifierAssignNumOpIdentifier, self).__init__(line_number)
        self.identifier = identifier
        self.val1 = val1
        self.val2 = val2
        self.operation = operation

    def translate(self, p):
        self.identifier.parent_procedure = self.parent_procedure
        self.val2.parent_procedure = self.parent_procedure
        asm_code = []
        asm_code.extend(Instructions.set_register_const(REG.B, self.val1))
        asm_code.extend(self.val2.translate_right_op_get_value())
        asm_code.extend(generate_operation(self.operation))
        asm_code.extend(self.identifier.translate_set_value())
        return asm_code


class CommandIdentifierAssignIdentifierOpIdentifier(Command):
    def __init__(self, identifier: Identifier, val1: Identifier, val2: Identifier, operation, line_number):
        super(CommandIdentifierAssignIdentifierOpIdentifier, self).__init__(line_number)
        self.identifier = identifier
        self.val1 = val1
        self.val2 = val2
        self.operation = operation

    def translate(self, p):
        self.identifier.parent_procedure = self.parent_procedure
        self.val1.parent_procedure = self.parent_procedure
        self.val2.parent_procedure = self.parent_procedure
        asm_code = []
        asm_code.extend(self.val1.translate_left_op_get_value())
        asm_code.extend(self.val2.translate_right_op_get_value())
        asm_code.extend(generate_operation(self.operation))
        asm_code.extend(self.identifier.translate_set_value())
        return asm_code


class CommandIf(Command):
    def __init__(self, condition: Condition, commands: List[Command], line_number):
        super(CommandIf, self).__init__(line_number)
        self.condition = condition
        self.commands = commands

    def translate(self, p):
        self.condition.parent_proc = self.parent_procedure
        asm_code = []
        label_generator: LabelGenerator = LabelGenerator()
        asm_code.extend(self.condition.translate(p))
        if_end_label = label_generator.next_if_end_label()
        if self.condition.negation_mode:
            asm_code.append(Instructions.JPOS(if_end_label))
        else:
            asm_code.append(Instructions.JZERO(if_end_label))

        for i in range(0, len(self.commands)):
            self.commands[i].set_parent_procedure(self.parent_procedure)
            asm_code.extend(self.commands[i].translate(p))

        last_line = asm_code[len(asm_code) - 1]
        if last_line.split()[0] == "LABEL":
            asm_code[len(asm_code) - 1] = last_line + if_end_label
            label_generator.decrement_label_shift()
        else:
            asm_code.append(Instructions.LABEL(if_end_label))
        return asm_code


class CommandIfElse(Command):
    def __init__(self, condition: Condition, commands1: List[Command], commands2: List[Command], line_number):
        super(CommandIfElse, self).__init__(line_number)
        self.condition = condition
        self.commands1 = commands1
        self.commands2 = commands2

    def translate(self, p):
        self.condition.parent_proc = self.parent_procedure
        asm_code = []
        label_generator: LabelGenerator = LabelGenerator()
        asm_code.extend(self.condition.translate(p))
        if_end_label = label_generator.next_if_end_label()
        else_label = label_generator.next_else_label()
        if self.condition.negation_mode:
            asm_code.append(Instructions.JPOS(else_label))
        else:
            asm_code.append(Instructions.JZERO(else_label))

        for i in range(0, len(self.commands1)):
            self.commands1[i].set_parent_procedure(self.parent_procedure)
            asm_code.extend(self.commands1[i].translate(p))

        asm_code.append(Instructions.JUMP(if_end_label))

        self.commands2[0].set_parent_procedure(self.parent_procedure)
        first_command = self.commands2[0].translate(p)
        first_command[0] = else_label + " " + first_command[0]
        asm_code.extend(first_command)

        for i in range(1, len(self.commands2)):
            self.commands2[i].set_parent_procedure(self.parent_procedure)
            asm_code.extend(self.commands2[i].translate(p))

        last_line = asm_code[len(asm_code) - 1]
        if last_line.split()[0] == "LABEL":
            asm_code[len(asm_code) - 1] = last_line + " " + if_end_label
            label_generator.decrement_label_shift()
        else:
            asm_code.append(Instructions.LABEL(if_end_label))
        return asm_code


class CommandWhile(Command):
    def __init__(self, condition: Condition, commands: List[Command], line_number):
        super(CommandWhile, self).__init__(line_number)
        self.condition = condition
        self.commands = commands

    def translate(self, p):
        self.condition.parent_proc = self.parent_procedure
        asm_code = []
        label_generator: LabelGenerator = LabelGenerator()
        while_cond_label = label_generator.next_while_cond_label()
        while_end_label = label_generator.next_while_end_label()
        cond_asm = self.condition.translate(p)
        cond_asm[0] = while_cond_label + " " + cond_asm[0]
        asm_code.extend(cond_asm)

        if self.condition.negation_mode:
            asm_code.append(Instructions.JPOS(while_end_label))
        else:
            asm_code.append(Instructions.JZERO(while_end_label))

        for i in range(0, len(self.commands)):
            self.commands[i].set_parent_procedure(self.parent_procedure)
            asm_code.extend(self.commands[i].translate(p))

        asm_code.append(Instructions.JUMP(while_cond_label))

        last_line = asm_code[len(asm_code) - 1]
        if last_line.split()[0] == "LABEL":
            asm_code[len(asm_code) - 1] = last_line + while_end_label
            label_generator.decrement_label_shift()
        else:
            asm_code.append(Instructions.LABEL(while_end_label))
        return asm_code


class CommandRepeatUntil(Command):
    def __init__(self, condition: Condition, commands: List[Command], line_number):
        super(CommandRepeatUntil, self).__init__(line_number)
        self.condition = condition
        self.commands = commands

    def translate(self, p):
        self.condition.parent_proc = self.parent_procedure
        asm_code = []
        label_generator: LabelGenerator = LabelGenerator()
        repeat_label = label_generator.next_repeat_label()
        cond_asm = self.condition.translate(p)

        for i in range(0, len(self.commands)):
            self.commands[i].set_parent_procedure(self.parent_procedure)
            asm_code.extend(self.commands[i].translate(p))

        asm_code.extend(cond_asm)
        if self.condition.negation_mode:
            asm_code.append(Instructions.JPOS(repeat_label))
            label_generator.decrement_label_shift()
        else:
            asm_code.append(Instructions.JZERO(repeat_label))

        asm_code[0] = repeat_label + " " + asm_code[0]
        return asm_code


class ProcCall(Command):
    def __init__(self, proc_pid, params: List[ProcCallParam], line_number):
        super(ProcCall, self).__init__(line_number)
        self.procedure_pid = proc_pid
        self.is_proc_call = True
        self.params = params

    def translate(self, p):
        return Instructions.proc_call(self.procedure_pid, self.params, self.line_number, self.parent_procedure)
