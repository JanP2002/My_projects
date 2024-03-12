from MemoryManager import MemoryManager
from MemoryManager import MemoryManagerException
from NonTerminals.ProcCallParam import ProcCallParam
from Register import REG
from typing import List


def makeInstr(instr, X="", Y=""):
    instr_str = "%s %s %s" % (instr, X, Y)
    return instr_str


def GET(reg: REG):
    return makeInstr('GET', reg.value)


def STORE(reg: REG):
    return makeInstr('STORE', reg.value)


def LOAD(reg: REG):
    return makeInstr('LOAD', reg.value)


def PUT(reg: REG):
    return makeInstr('PUT', reg.value)


def GET(reg: REG):
    return makeInstr('GET', reg.value)


def INC(reg: REG):
    return makeInstr('INC', reg.value)


def JUMP(j):
    return makeInstr('JUMP', j)


def JPOS(j):
    return makeInstr('JPOS', j)


def JZERO(j):
    return makeInstr('JZERO', j)


def DEC(reg: REG):
    return makeInstr('DEC', reg.value)


def ADD(reg: REG):
    return makeInstr('ADD', reg.value)


def SHL(reg: REG):
    return makeInstr('SHL', reg.value)


def SHR(reg: REG):
    return makeInstr('SHR', reg.value)


def SUB(reg: REG):
    return makeInstr('SUB', reg.value)


def RST(reg: REG):
    return makeInstr('RST', reg.value)


def STRK(reg: REG):
    return makeInstr('STRK', reg.value)


def JUMPR(reg: REG):
    return makeInstr('JUMPR', reg.value)


def READ():
    return makeInstr('READ')


def WRITE():
    return makeInstr('WRITE')


def HALT():
    return makeInstr('HALT')


def LABEL(label_str):
    return makeInstr("LABEL", label_str)


def proc_call(proc_pid, params: List[ProcCallParam], line_number, parent_proc=None):
    memory_manager: MemoryManager = MemoryManager()
    asm_code = []
    if parent_proc is not None:
        called_procedure = memory_manager.get_procedure(proc_pid, line_number)
        called_proc_label = called_procedure.label
        parent_procedure = memory_manager.get_procedure(parent_proc, line_number)
        parent_proc_label = parent_procedure.label
        if called_proc_label > parent_proc_label:
            raise MemoryManagerException("Blad w linii %i: Procedura %s nie jest zdefiniowana" %
                                         (line_number, proc_pid))
        elif called_proc_label == parent_proc_label:
            raise MemoryManagerException("Blad w linii %i: Proba rekurencyjnego wywolania procedury %s" %
                                         (line_number, proc_pid))
        params_pattern_list = called_procedure.params_declarations
        n_passed = len(params)
        n_pattern = len(params_pattern_list)
        if n_passed != n_pattern:
            raise ProcCallException("Blad w linii %i: Podano nieprawidlowa liczbe parametrow procedury %s" %
                                    (line_number, proc_pid))

        for i in range(n_pattern):
            passed_param_id = parent_proc + "##" + params[i].pid
            passed_param_variable = memory_manager.get_variable(passed_param_id, params[i].line_number)
            if passed_param_variable.is_local:
                passed_param_variable.is_initialized = True
                passed_param_address = passed_param_variable.memory_id
                asm_code.extend(set_register_const(REG.A, passed_param_address))
                proc_param_id = proc_pid + "##" + params_pattern_list[i].pid
                proc_param_declaration = memory_manager.get_variable(proc_param_id, line_number)
                if (passed_param_variable.is_array and not proc_param_declaration.is_array) or (
                        not passed_param_variable.is_array and proc_param_declaration.is_array):
                    raise ProcCallException("Blad w linii %i: Niewlasciwe parametry procedury %s" %
                                            (line_number, proc_pid))
                # if proc_param_declaration.must_be_initialized and (not passed_param_variable.is_initialized):
                #     print("Ostrzezenie: w linii %i zmienna moze nie byc zainicjowana %s" %
                #           (proc_param_declaration.uninitialized_usage_line,
                #            proc_param_declaration.context_pid))
                    # raise MemoryManagerException("Blad w linii %i: Proba uzycia niezainicjalizowanej zmiennej %s" %
                    #                              (proc_param_declaration.uninitialized_usage_line,
                    #                               proc_param_declaration.context_pid))
                proc_param_address = proc_param_declaration.memory_id
                asm_code.extend(set_register_const(REG.B, proc_param_address))
                asm_code.append(makeInstr('STORE', REG.B.value))

            elif passed_param_variable.is_param:
                formal_param_address = passed_param_variable.memory_id
                asm_code.extend(set_register_const(REG.B, formal_param_address))
                asm_code.append(makeInstr('LOAD', REG.B.value))
                proc_param_id = proc_pid + "##" + params_pattern_list[i].pid
                proc_param_declaration = memory_manager.get_variable(proc_param_id, line_number)
                if (passed_param_variable.is_array and not proc_param_declaration.is_array) or (
                        not passed_param_variable.is_array and proc_param_declaration.is_array):
                    raise ProcCallException("Blad w linii %i: Niewlasciwe parametry procedury %s" %
                                            (line_number, proc_pid))
                # if proc_param_declaration.must_be_initialized and ((not passed_param_variable.is_initialized)
                #                                                    and (not passed_param_variable.must_be_initialized)):
                #     context_pid = proc_param_declaration.context_pid
                #     if context_pid is None:
                #         context_pid = proc_param_declaration.pid
                #     passed_param_variable.set_uninitialized_error(context_pid,
                #                                                   proc_param_declaration.uninitialized_usage_line)

                proc_param_address = proc_param_declaration.memory_id
                asm_code.extend(set_register_const(REG.B, proc_param_address))
                asm_code.append(makeInstr('STORE', REG.B.value))

            else:
                raise ProcCallException("Nieprawidlowe zagniezdzone wywolanie procedury")

        asm_code.extend(set_register_const(REG.C, 4))
        return_address = called_procedure.activation_record_start
        asm_code.extend(set_register_const(REG.B, return_address))
        asm_code.append(makeInstr('STRK', REG.A.value))
        asm_code.append(makeInstr('ADD', REG.C.value))
        asm_code.append(makeInstr('STORE', REG.B.value))
        asm_code.append(makeInstr('JUMP', proc_pid + ":"))

    else:
        procedure = memory_manager.get_procedure(proc_pid, line_number)
        params_pattern_list = procedure.params_declarations
        n_passed = len(params)
        n_pattern = len(params_pattern_list)
        if n_passed != n_pattern:
            raise ProcCallException("Blad w linii %i: Podano nieprawidlowa liczbe parametrow procedury %s" %
                                    (line_number, proc_pid))

        for i in range(n_pattern):
            passed_param_variable = memory_manager.get_variable(params[i].pid, params[i].line_number)
            passed_param_variable.is_initialized = True
            passed_param_address = passed_param_variable.memory_id
            asm_code.extend(set_register_const(REG.A, passed_param_address))
            proc_param_id = proc_pid + "##" + params_pattern_list[i].pid
            proc_param_declaration = memory_manager.get_variable(proc_param_id, line_number)
            if (passed_param_variable.is_array and not proc_param_declaration.is_array) or (
                    not passed_param_variable.is_array and proc_param_declaration.is_array):
                raise ProcCallException("Blad w linii %i: Niewlasciwe parametry procedury %s" %
                                        (line_number, proc_pid))
            # if proc_param_declaration.must_be_initialized and (not passed_param_variable.is_initialized):
            #     print("Ostrzezenie: w linii %i zmienna moze nie byc zainicjowana %s" %
            #                                  (proc_param_declaration.uninitialized_usage_line,
            #                                   proc_param_declaration.context_pid))
            # raise MemoryManagerException("Blad w linii %i: Proba uzycia niezainicjalizowanej zmiennej %s" %
            #                              (proc_param_declaration.uninitialized_usage_line,
            #                               proc_param_declaration.context_pid))
            proc_param_address = proc_param_declaration.memory_id
            asm_code.extend(set_register_const(REG.B, proc_param_address))
            asm_code.append(makeInstr('STORE', REG.B.value))

        asm_code.extend(set_register_const(REG.C, 4))
        return_address = procedure.activation_record_start
        asm_code.extend(set_register_const(REG.B, return_address))
        asm_code.append(makeInstr('STRK', REG.A.value))
        asm_code.append(makeInstr('ADD', REG.C.value))
        asm_code.append(makeInstr('STORE', REG.B.value))
        asm_code.append(makeInstr('JUMP', proc_pid + ":"))

    return asm_code


def proc_return(proc_pid, line_number):
    memory_manager: MemoryManager = MemoryManager()
    procedure = memory_manager.get_procedure(proc_pid, line_number)
    return_address = procedure.activation_record_start
    asm_code = set_register_const(REG.B, return_address)
    asm_code.append(makeInstr('LOAD', REG.B.value))
    asm_code.append(makeInstr('JUMPR', REG.A.value))
    for decl in procedure.local_declarations:
        decl.is_initialized = False
    return asm_code


def set_register_const(reg, val):
    asm_code = [RST(reg)]

    bin_val = bin(val)[2:]  # number to binary representation
    length = len(bin_val)  # how many digits
    for i, digit in enumerate(bin_val):
        if digit == '1':
            asm_code.append(INC(reg))  # reg = reg + 1
        if i < length - 1:
            asm_code.append(SHL(reg))  # reg = reg << 1
    return asm_code


def generate_adding():
    asm_code = [GET(REG.B), ADD(REG.E)]
    return asm_code


def generate_subtraction():
    asm_code = [GET(REG.B), SUB(REG.E)]
    return asm_code


def generate_multiplication():
    asm_code = []
    asm_code.append(RST(REG.H))
    asm_code.append(GET(REG.B))
    asm_code.append(JZERO("+" + str(25)))
    asm_code.append(GET(REG.E))
    asm_code.append(JZERO("+" + str(23)))

    asm_code.append(GET(REG.E))
    asm_code.append(SUB(REG.B))
    asm_code.append(JZERO("+" + str(7)))

    # swap:
    asm_code.append(GET(REG.B))
    asm_code.append(PUT(REG.G))
    asm_code.append(GET(REG.E))
    asm_code.append(PUT(REG.B))
    asm_code.append(GET(REG.G))
    asm_code.append(PUT(REG.E))

    asm_code.append(GET(REG.E))
    asm_code.append(PUT(REG.F))
    asm_code.append(SHR(REG.F))
    asm_code.append(SHL(REG.F))
    asm_code.append(SUB(REG.F))

    asm_code.append(JZERO("+" + str(4)))
    asm_code.append(GET(REG.H))
    asm_code.append(ADD(REG.B))
    asm_code.append(PUT(REG.H))

    asm_code.append(SHL(REG.B))
    asm_code.append(SHR(REG.E))
    asm_code.append(GET(REG.E))
    asm_code.append(JPOS("-" + str(11)))

    asm_code.append(GET(REG.H))
    return asm_code


def generate_division():
    asm_code = []
    asm_code.append(RST(REG.H))
    asm_code.append(GET(REG.E))
    asm_code.append(JZERO("+" + str(26)))

    # asm_code.append(RST(REG.F))
    asm_code.append(GET(REG.B))
    asm_code.append(PUT(REG.D))

    asm_code.append(GET(REG.E))  #
    asm_code.append(PUT(REG.G))
    # asm_code.append(GET(REG.G))##
    asm_code.append(SUB(REG.D))  # w a inf. czy d < g
    asm_code.append(JPOS("+" + str(20)))

    asm_code.append(RST(REG.F))
    asm_code.append(INC(REG.F))
    # asm_code.extend(set_register_const(REG.F, 1))

    asm_code.append(JPOS("+" + str(6)))
    asm_code.append(SHL(REG.G))
    asm_code.append(SHL(REG.F))
    asm_code.append(GET(REG.G))
    asm_code.append(SUB(REG.D))
    asm_code.append(JZERO("-" + str(4)))

    asm_code.append(SHR(REG.G))
    asm_code.append(SHR(REG.F))
    asm_code.append(GET(REG.H))
    asm_code.append(ADD(REG.F))
    asm_code.append(PUT(REG.H))

    asm_code.append(GET(REG.D))
    asm_code.append(SUB(REG.G))
    asm_code.append(PUT(REG.D))

    asm_code.append(GET(REG.B))
    asm_code.append(SUB(REG.G))  # w a inf. czy g < b
    asm_code.append(JPOS("-" + str(22)))

    asm_code.append(GET(REG.H))
    return asm_code


def generate_modulo():
    asm_code = []
    asm_code.append(RST(REG.D))
    asm_code.append(GET(REG.E))
    asm_code.append(JZERO("+" + str(19)))

    asm_code.append(GET(REG.B))
    asm_code.append(PUT(REG.D))

    asm_code.append(GET(REG.E))  #
    asm_code.append(PUT(REG.G))
    # asm_code.append(GET(REG.G))##
    asm_code.append(SUB(REG.D))  # w a inf. czy d < g
    asm_code.append(JPOS("+" + str(13)))

    asm_code.append(JPOS("+" + str(5)))
    asm_code.append(SHL(REG.G))
    asm_code.append(GET(REG.G))
    asm_code.append(SUB(REG.D))
    asm_code.append(JZERO("-" + str(3)))

    asm_code.append(SHR(REG.G))

    asm_code.append(GET(REG.D))
    asm_code.append(SUB(REG.G))
    asm_code.append(PUT(REG.D))

    asm_code.append(GET(REG.B))
    asm_code.append(SUB(REG.G))  # w a inf. czy g < b
    asm_code.append(JPOS("-" + str(15)))

    asm_code.append(GET(REG.D))
    return asm_code


class ProcCallException(Exception):
    def __init__(self, msg):
        self.message = msg
