import Instructions
from MemoryManager import MemoryManager
from NonTerminals.Declarations import ArrayDeclaration
from Register import REG


class Identifier:
    def __init__(self, pid, line_number=-1):
        self.line_number = line_number
        self.parent_procedure = None
        self.pid = pid

    def set_parent_procedure(self, proc_pid):
        self.parent_procedure = proc_pid

    def translate_set_value(self):
        asm_code = []
        memory_manager: MemoryManager = MemoryManager()
        if self.parent_procedure is not None:
            variable_id = self.parent_procedure + "##" + self.pid
            declaration = memory_manager.get_variable(variable_id, self.line_number)
            if declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Nieprawidlowe uzycie tablicy %s" % (self.line_number,
                                                                                                self.pid))
            address = declaration.get_memory_id()
            if declaration.is_param:
                asm_code.append(Instructions.PUT(REG.H))
                asm_code.extend(Instructions.set_register_const(REG.B, address))
                asm_code.append(Instructions.LOAD(REG.B))
                asm_code.append(Instructions.PUT(REG.B))
                asm_code.append(Instructions.GET(REG.H))
                asm_code.append(Instructions.STORE(REG.B))
            else:
                asm_code.extend(Instructions.set_register_const(REG.B, address))
                asm_code.append(Instructions.STORE(REG.B))
            declaration.is_initialized = True
        else:
            declaration = memory_manager.get_variable(self.pid, self.line_number)
            if declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Nieprawidlowe uzycie tablicy %s" % (self.line_number,
                                                                                                self.pid))
            address = declaration.get_memory_id()
            asm_code.extend(Instructions.set_register_const(REG.B, address))
            asm_code.append(Instructions.STORE(REG.B))
            declaration.is_initialized = True

        return asm_code

    def translate_write_get_value(self):
        asm_code = []
        memory_manager: MemoryManager = MemoryManager()
        if self.parent_procedure is not None:
            variable_id = self.parent_procedure + "##" + self.pid
            declaration = memory_manager.get_variable(variable_id, self.line_number)
            if declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Nieprawidlowe uzycie tablicy %s" % (self.line_number,
                                                                                                self.pid))
            if declaration.is_param:
                # if (not declaration.is_initialized) and (not declaration.must_be_initialized):
                #     declaration.set_uninitialized_error(self.pid, self.line_number)
                address = declaration.get_memory_id()
                asm_code.extend(Instructions.set_register_const(REG.B, address))
                asm_code.append(Instructions.makeInstr('LOAD', REG.B.value))
                asm_code.append(Instructions.makeInstr('LOAD', REG.A.value))
            else:
                if not declaration.is_initialized:
                    print("Ostrzezenie w linii %i: Zmienna %s moze nie byc zainicjoana" %
                          (self.line_number, declaration.pid))
                address = declaration.get_memory_id()
                asm_code.extend(Instructions.set_register_const(REG.B, address))
                asm_code.append(Instructions.makeInstr('LOAD', REG.B.value))
        else:
            declaration = memory_manager.get_variable(self.pid, self.line_number)
            if declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Nieprawidlowe uzycie tablicy %s" % (self.line_number,
                                                                                                self.pid))
            if not declaration.is_initialized:
                print("Ostrzezenie w linii %i: Zmienna %s moze nie byc zainicjoana" %
                      (self.line_number, declaration.pid))
            address = declaration.get_memory_id()
            asm_code.extend(Instructions.set_register_const(REG.B, address))
            asm_code.append(Instructions.makeInstr('LOAD', REG.B.value))
        return asm_code

    def translate_assign_get_value(self):
        asm_code = []
        memory_manager: MemoryManager = MemoryManager()
        if self.parent_procedure is not None:
            variable_id = self.parent_procedure + "##" + self.pid
            declaration = memory_manager.get_variable(variable_id, self.line_number)
            address = declaration.get_memory_id()
            if declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Nieprawidlowe uzycie tablicy %s" % (self.line_number,
                                                                                                self.pid))
            if declaration.is_param:
                # if (not declaration.is_initialized) and (not declaration.must_be_initialized):
                #     declaration.set_uninitialized_error(self.pid, self.line_number)
                asm_code.extend(Instructions.set_register_const(REG.F, address))
                asm_code.append(Instructions.LOAD(REG.F))  # adres zmiennej pid w reg a
                asm_code.append(Instructions.LOAD(REG.A))  # wartosc zmiennej pid w reg a
            else:
                if not declaration.is_initialized:
                    print("Ostrzezenie: W linii %i zmienna %s moze nie byc zainicjoana" %
                          (self.line_number, self.pid))
                asm_code.extend(Instructions.set_register_const(REG.F, address))  # adres zmiennej pid w reg f
                asm_code.append(Instructions.LOAD(REG.F))
        else:
            declaration = memory_manager.get_variable(self.pid, self.line_number)
            if declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Nieprawidlowe uzycie tablicy %s" % (self.line_number,
                                                                                                self.pid))
            if not declaration.is_initialized:
                print("Ostrzezenie w linii %i: Zmienna %s moze nie byc zainicjoana" %
                      (self.line_number, declaration.pid))
            address = declaration.get_memory_id()
            asm_code.extend(Instructions.set_register_const(REG.F, address))  # adres zmiennej pid w reg f
            asm_code.append(Instructions.LOAD(REG.F))
        return asm_code

    def translate_left_op_get_value(self):
        asm_code = []
        memory_manager: MemoryManager = MemoryManager()
        if self.parent_procedure is not None:
            variable_id = self.parent_procedure + "##" + self.pid
            declaration = memory_manager.get_variable(variable_id, self.line_number)
            address = declaration.get_memory_id()
            if declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Nieprawidlowe uzycie tablicy %s" % (self.line_number,
                                                                                                self.pid))
            if declaration.is_param:
                # if (not declaration.is_initialized) and (not declaration.must_be_initialized):
                #     declaration.set_uninitialized_error(self.pid, self.line_number)
                asm_code.extend(Instructions.set_register_const(REG.F, address))
                asm_code.append(Instructions.LOAD(REG.F))  # adres zmiennej pid w reg a
                asm_code.append(Instructions.LOAD(REG.A))  # wartosc zmiennej pid w reg a
                asm_code.append(Instructions.PUT(REG.B))
            else:
                if not declaration.is_initialized:
                    print("Ostrzezenie: W linii %i zmienna %s moze nie byc zainicjoana" %
                          (self.line_number, self.pid))
                asm_code.extend(Instructions.set_register_const(REG.F, address))  # adres zmiennej pid w reg f
                asm_code.append(Instructions.LOAD(REG.F))
                asm_code.append(Instructions.PUT(REG.B))
        else:
            declaration = memory_manager.get_variable(self.pid, self.line_number)
            if declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Nieprawidlowe uzycie tablicy %s" % (self.line_number,
                                                                                                self.pid))
            if not declaration.is_initialized:
                print("Ostrzezenie w linii %i: Zmienna %s moze nie byc zainicjoana" %
                      (self.line_number, declaration.pid))
            address = declaration.get_memory_id()
            asm_code.extend(Instructions.set_register_const(REG.F, address))  # adres zmiennej pid w reg f
            asm_code.append(Instructions.LOAD(REG.F))
            asm_code.append(Instructions.PUT(REG.B))
        return asm_code

    def translate_right_op_get_value(self):
        asm_code = []
        memory_manager: MemoryManager = MemoryManager()
        if self.parent_procedure is not None:
            variable_id = self.parent_procedure + "##" + self.pid
            declaration = memory_manager.get_variable(variable_id, self.line_number)
            address = declaration.get_memory_id()
            if declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Nieprawidlowe uzycie tablicy %s" % (self.line_number,
                                                                                                self.pid))
            if declaration.is_param:
                # if (not declaration.is_initialized) and (not declaration.must_be_initialized):
                #     declaration.set_uninitialized_error(self.pid, self.line_number)
                asm_code.extend(Instructions.set_register_const(REG.F, address))
                asm_code.append(Instructions.LOAD(REG.F))  # adres zmiennej pid w reg a
                asm_code.append(Instructions.LOAD(REG.A))  # wartosc zmiennej pid w reg a
                asm_code.append(Instructions.PUT(REG.E))
            else:
                if not declaration.is_initialized:
                    print("Ostrzezenie: W linii %i zmienna %s moze nie byc zainicjoana" %
                          (self.line_number, self.pid))
                address = declaration.get_memory_id()
                asm_code.extend(Instructions.set_register_const(REG.F, address))  # adres zmiennej pid w reg f
                asm_code.append(Instructions.LOAD(REG.F))
                asm_code.append(Instructions.PUT(REG.E))
        else:
            declaration = memory_manager.get_variable(self.pid, self.line_number)
            if declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Nieprawidlowe uzycie tablicy %s" % (self.line_number,
                                                                                                self.pid))
            if not declaration.is_initialized:
                print("Ostrzezenie w linii %i: Zmienna %s moze nie byc zainicjoana" %
                      (self.line_number, declaration.pid))
            address = declaration.get_memory_id()
            asm_code.extend(Instructions.set_register_const(REG.F, address))  # adres zmiennej pid w reg f
            asm_code.append(Instructions.LOAD(REG.F))
            asm_code.append(Instructions.PUT(REG.E))
        return asm_code

    def translate_left_cond_get_value(self):
        asm_code = []
        memory_manager: MemoryManager = MemoryManager()
        if self.parent_procedure is not None:
            variable_id = self.parent_procedure + "##" + self.pid
            declaration = memory_manager.get_variable(variable_id, self.line_number)
            address = declaration.get_memory_id()
            if declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Nieprawidlowe uzycie tablicy %s" % (self.line_number,
                                                                                                self.pid))
            if declaration.is_param:
                # if (not declaration.is_initialized) and (not declaration.must_be_initialized):
                #     declaration.set_uninitialized_error(self.pid, self.line_number)
                asm_code.extend(Instructions.set_register_const(REG.F, address))
                asm_code.append(Instructions.LOAD(REG.F))  # adres zmiennej pid w reg a
                asm_code.append(Instructions.LOAD(REG.A))  # wartosc zmiennej pid w reg a
                asm_code.append(Instructions.PUT(REG.C))
            else:
                if not declaration.is_initialized:
                    print("Ostrzezenie: W linii %i zmienna %s moze nie byc zainicjoana" %
                          (self.line_number, self.pid))
                asm_code.extend(Instructions.set_register_const(REG.F, address))  # adres zmiennej pid w reg f
                asm_code.append(Instructions.LOAD(REG.F))
                asm_code.append(Instructions.PUT(REG.C))
        else:
            declaration = memory_manager.get_variable(self.pid, self.line_number)
            if declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Nieprawidlowe uzycie tablicy %s" % (self.line_number,
                                                                                                self.pid))
            if not declaration.is_initialized:
                print("Ostrzezenie w linii %i: Zmienna %s moze nie byc zainicjoana" %
                      (self.line_number, declaration.pid))
            address = declaration.get_memory_id()
            asm_code.extend(Instructions.set_register_const(REG.F, address))  # adres zmiennej pid w reg f
            asm_code.append(Instructions.LOAD(REG.F))
            asm_code.append(Instructions.PUT(REG.C))
        return asm_code

    def translate_right_cond_get_value(self):
        asm_code = []
        memory_manager: MemoryManager = MemoryManager()
        if self.parent_procedure is not None:
            variable_id = self.parent_procedure + "##" + self.pid
            declaration = memory_manager.get_variable(variable_id, self.line_number)
            address = declaration.get_memory_id()
            if declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Nieprawidlowe uzycie tablicy %s" % (self.line_number,
                                                                                                self.pid))
            if declaration.is_param:
                # if (not declaration.is_initialized) and (not declaration.must_be_initialized):
                #     declaration.set_uninitialized_error(self.pid, self.line_number)
                asm_code.extend(Instructions.set_register_const(REG.F, address))
                asm_code.append(Instructions.LOAD(REG.F))  # adres zmiennej pid w reg a
                asm_code.append(Instructions.LOAD(REG.A))  # wartosc zmiennej pid w reg a
                asm_code.append(Instructions.PUT(REG.D))
            else:
                if not declaration.is_initialized:
                    print("Ostrzezenie: W linii %i zmienna %s moze nie byc zainicjoana" %
                          (self.line_number, self.pid))
                asm_code.extend(Instructions.set_register_const(REG.F, address))  # adres zmiennej pid w reg f
                asm_code.append(Instructions.LOAD(REG.F))
                asm_code.append(Instructions.PUT(REG.D))
        else:
            declaration = memory_manager.get_variable(self.pid, self.line_number)
            if declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Nieprawidlowe uzycie tablicy %s" % (self.line_number,
                                                                                                self.pid))
            if not declaration.is_initialized:
                print("Ostrzezenie w linii %i: Zmienna %s moze nie byc zainicjoana" %
                      (self.line_number, declaration.pid))
            address = declaration.get_memory_id()
            asm_code.extend(Instructions.set_register_const(REG.F, address))  # adres zmiennej pid w reg f
            asm_code.append(Instructions.LOAD(REG.F))
            asm_code.append(Instructions.PUT(REG.D))
        return asm_code


class ArrayNumIdentifier(Identifier):
    def __init__(self, pid, idx, line_number=-1, ):
        super(ArrayNumIdentifier, self).__init__(pid, line_number)
        self.idx = idx

    def translate_set_value(self):
        asm_code = []
        memory_manager: MemoryManager = MemoryManager()
        if self.parent_procedure is not None:
            variable_id = self.parent_procedure + "##" + self.pid
            declaration: ArrayDeclaration = memory_manager.get_variable(variable_id, self.line_number)
            if not declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Zmienna %s nie jest tablica" % (self.line_number,
                                                                                            self.pid))
            if declaration.is_param:
                address = declaration.get_memory_id()
                asm_code.append(Instructions.PUT(REG.H))
                asm_code.extend(Instructions.set_register_const(REG.B, address))
                asm_code.append(Instructions.LOAD(REG.B))
                asm_code.extend(Instructions.set_register_const(REG.G, self.idx))
                asm_code.append(Instructions.ADD(REG.G))
                asm_code.append(Instructions.PUT(REG.B))
                asm_code.append(Instructions.GET(REG.H))
                asm_code.append(Instructions.STORE(REG.B))
            else:
                if self.idx < 0 or self.idx >= declaration.array_size:
                    raise ArrayUsageException("Blad w linii %i: Proba odwolania sie do komorki z poza tablicy %s" % (
                        self.line_number, self.pid))
                address = declaration.get_memory_id() + self.idx
                asm_code.extend(Instructions.set_register_const(REG.B, address))
                asm_code.append(Instructions.STORE(REG.B))
                if isinstance(declaration, ArrayDeclaration):
                    declaration.initialized_fields.append(self.idx)

        else:
            declaration = memory_manager.get_variable(self.pid, self.line_number)
            if not declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Zmienna %s nie jest tablica" % (self.line_number,
                                                                                            self.pid))
            if self.idx < 0 or self.idx >= declaration.array_size:
                raise ArrayUsageException("Blad w linii %i: Proba odwolania sie do komorki z poza tablicy %s" % (
                    self.line_number, self.pid))
            address = declaration.get_memory_id() + self.idx
            asm_code.extend(Instructions.set_register_const(REG.B, address))
            asm_code.append(Instructions.STORE(REG.B))
            if isinstance(declaration, ArrayDeclaration):
                declaration.initialized_fields.append(self.idx)
        return asm_code

    def translate_write_get_value(self):
        asm_code = []
        memory_manager: MemoryManager = MemoryManager()
        if self.parent_procedure is not None:
            variable_id = self.parent_procedure + "##" + self.pid
            declaration = memory_manager.get_variable(variable_id, self.line_number)
            if not declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Zmienna %s nie jest tablica" % (self.line_number,
                                                                                            self.pid))
            if declaration.is_param:
                # if (not declaration[address].is_initialized) and (not declaration.must_be_initialized):
                #     declaration.set_uninitialized_error(self.pid, self.line_number)
                address = declaration.get_memory_id()
                asm_code.extend(Instructions.set_register_const(REG.B, address))
                asm_code.append(Instructions.LOAD(REG.B))
                asm_code.extend(Instructions.set_register_const(REG.G, self.idx))
                asm_code.append(Instructions.ADD(REG.G))
                asm_code.append(Instructions.LOAD(REG.A))
            else:
                if self.idx < 0 or self.idx >= declaration.array_size:
                    raise ArrayUsageException("Blad w linii %i: Proba odwolania sie do komorki z poza tablicy %s" % (
                        self.line_number, self.pid))
                address = declaration.get_memory_id() + self.idx
                if isinstance(declaration, ArrayDeclaration) and self.idx not in declaration.initialized_fields:
                    print("Ostrzezenie w linii %i: %s[%i] moze nie byc zainicjowane" %
                          (self.line_number, self.pid, self.idx))
                asm_code.extend(Instructions.set_register_const(REG.B, address))
                asm_code.append(Instructions.makeInstr('LOAD', REG.B.value))
        else:
            declaration = memory_manager.get_variable(self.pid, self.line_number)
            if not declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Zmienna %s nie jest tablica" % (self.line_number,
                                                                                            self.pid))
            if self.idx < 0 or self.idx >= declaration.array_size:
                raise ArrayUsageException("Blad w linii %i: Proba odwolania sie do komorki z poza tablicy %s" % (
                    self.line_number, self.pid))
            address = declaration.get_memory_id() + self.idx
            if isinstance(declaration, ArrayDeclaration) and self.idx not in declaration.initialized_fields:
                print("Ostrzezenie w linii %i: %s[%i] moze nie byc zainicjowane" %
                      (self.line_number, self.pid, self.idx))
            asm_code.extend(Instructions.set_register_const(REG.B, address))
            asm_code.append(Instructions.makeInstr('LOAD', REG.B.value))
        return asm_code

    def translate_assign_get_value(self):
        asm_code = []
        memory_manager: MemoryManager = MemoryManager()
        if self.parent_procedure is not None:
            variable_id = self.parent_procedure + "##" + self.pid
            declaration = memory_manager.get_variable(variable_id, self.line_number)
            if not declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Zmienna %s nie jest tablica" % (self.line_number,
                                                                                            self.pid))
            if declaration.is_param:
                address = declaration.get_memory_id()
                # if (not declaration[address].is_initialized) and (not declaration.must_be_initialized):
                #     declaration.set_uninitialized_error(self.pid, self.line_number)
                asm_code.extend(Instructions.set_register_const(REG.F, address))
                asm_code.append(Instructions.makeInstr('LOAD', REG.F.value))
                asm_code.extend(Instructions.set_register_const(REG.G, self.idx))
                asm_code.append(Instructions.ADD(REG.G))
                asm_code.append(Instructions.makeInstr('LOAD', REG.A.value))
            else:
                if self.idx < 0 or self.idx >= declaration.array_size:
                    raise ArrayUsageException("Blad w linii %i: Proba odwolania sie do komorki z poza tablicy %s" % (
                        self.line_number, self.pid))
                address = declaration.get_memory_id() + self.idx
                if isinstance(declaration, ArrayDeclaration) and self.idx not in declaration.initialized_fields:
                    print("Ostrzezenie w linii %i: %s[%i] moze nie byc zainicjowane" %
                          (self.line_number, self.pid, self.idx))
                asm_code.extend(Instructions.set_register_const(REG.F, address))
                asm_code.append(Instructions.makeInstr('LOAD', REG.F.value))
        else:
            declaration = memory_manager.get_variable(self.pid, self.line_number)
            if not declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Zmienna %s nie jest tablica" % (self.line_number,
                                                                                            self.pid))
            if self.idx < 0 or self.idx >= declaration.array_size:
                raise ArrayUsageException("Blad w linii %i: Proba odwolania sie do komorki z poza tablicy %s" % (
                    self.line_number, self.pid))
            address = declaration.get_memory_id() + self.idx
            if isinstance(declaration, ArrayDeclaration) and self.idx not in declaration.initialized_fields:
                print("Ostrzezenie w linii %i: %s[%i] moze nie byc zainicjowane" %
                      (self.line_number, self.pid, self.idx))
            asm_code.extend(Instructions.set_register_const(REG.F, address))
            asm_code.append(Instructions.makeInstr('LOAD', REG.F.value))
        return asm_code

    def translate_left_op_get_value(self):
        asm_code = []
        memory_manager: MemoryManager = MemoryManager()
        if self.parent_procedure is not None:
            variable_id = self.parent_procedure + "##" + self.pid
            declaration = memory_manager.get_variable(variable_id, self.line_number)
            if not declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Zmienna %s nie jest tablica" % (self.line_number,
                                                                                            self.pid))

            if declaration.is_param:
                address = declaration.get_memory_id()
                # if (not declaration[address].is_initialized) and (not declaration.must_be_initialized):
                #     declaration.set_uninitialized_error(self.pid, self.line_number)
                asm_code.extend(Instructions.set_register_const(REG.F, address))
                asm_code.append(Instructions.makeInstr('LOAD', REG.F.value))
                asm_code.extend(Instructions.set_register_const(REG.G, self.idx))
                asm_code.append(Instructions.ADD(REG.G))
                asm_code.append(Instructions.makeInstr('LOAD', REG.A.value))
                asm_code.append(Instructions.makeInstr('PUT', REG.B.value))
            else:
                if self.idx < 0 or self.idx >= declaration.array_size:
                    raise ArrayUsageException("Blad w linii %i: Proba odwolania sie do komorki z poza tablicy %s" % (
                        self.line_number, self.pid))
                address = declaration.get_memory_id() + self.idx
                if isinstance(declaration, ArrayDeclaration) and self.idx not in declaration.initialized_fields:
                    print("Ostrzezenie w linii %i: %s[%i] moze nie byc zainicjowane" %
                          (self.line_number, self.pid, self.idx))
                asm_code.extend(Instructions.set_register_const(REG.F, address))
                asm_code.append(Instructions.makeInstr('LOAD', REG.F.value))
                asm_code.append(Instructions.makeInstr('PUT', REG.B.value))
        else:
            declaration = memory_manager.get_variable(self.pid, self.line_number)
            if not declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Zmienna %s nie jest tablica" % (self.line_number,
                                                                                            self.pid))
            if self.idx < 0 or self.idx >= declaration.array_size:
                raise ArrayUsageException("Blad w linii %i: Proba odwolania sie do komorki z poza tablicy %s" % (
                    self.line_number, self.pid))
            address = declaration.get_memory_id() + self.idx
            if isinstance(declaration, ArrayDeclaration) and self.idx not in declaration.initialized_fields:
                print("Ostrzezenie w linii %i: %s[%i] moze nie byc zainicjowane" %
                      (self.line_number, self.pid, self.idx))
            asm_code.extend(Instructions.set_register_const(REG.F, address))
            asm_code.append(Instructions.makeInstr('LOAD', REG.F.value))
            asm_code.append(Instructions.makeInstr('PUT', REG.B.value))
        return asm_code

    def translate_right_op_get_value(self):
        asm_code = []
        memory_manager: MemoryManager = MemoryManager()
        if self.parent_procedure is not None:
            variable_id = self.parent_procedure + "##" + self.pid
            declaration = memory_manager.get_variable(variable_id, self.line_number)
            if not declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Zmienna %s nie jest tablica" % (self.line_number,
                                                                                            self.pid))

            if declaration.is_param:
                address = declaration.get_memory_id()
                # if (not declaration[address].is_initialized) and (not declaration.must_be_initialized):
                #     declaration.set_uninitialized_error(self.pid, self.line_number)
                asm_code.extend(Instructions.set_register_const(REG.F, address))
                asm_code.append(Instructions.makeInstr('LOAD', REG.F.value))
                asm_code.extend(Instructions.set_register_const(REG.G, self.idx))
                asm_code.append(Instructions.ADD(REG.G))
                asm_code.append(Instructions.makeInstr('LOAD', REG.A.value))
                asm_code.append(Instructions.makeInstr('PUT', REG.E.value))
            else:
                if self.idx < 0 or self.idx >= declaration.array_size:
                    raise ArrayUsageException("Blad w linii %i: Proba odwolania sie do komorki z poza tablicy %s" % (
                        self.line_number, self.pid))
                address = declaration.get_memory_id() + self.idx
                if isinstance(declaration, ArrayDeclaration) and self.idx not in declaration.initialized_fields:
                    print("Ostrzezenie w linii %i: %s[%i] moze nie byc zainicjowane" %
                          (self.line_number, self.pid, self.idx))
                asm_code.extend(Instructions.set_register_const(REG.F, address))
                asm_code.append(Instructions.makeInstr('LOAD', REG.F.value))
                asm_code.append(Instructions.makeInstr('PUT', REG.E.value))
        else:
            declaration = memory_manager.get_variable(self.pid, self.line_number)
            if not declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Zmienna %s nie jest tablica" % (self.line_number,
                                                                                            self.pid))
            if self.idx < 0 or self.idx >= declaration.array_size:
                raise ArrayUsageException("Blad w linii %i: Proba odwolania sie do komorki z poza tablicy %s" % (
                    self.line_number, self.pid))
            address = declaration.get_memory_id() + self.idx
            if isinstance(declaration, ArrayDeclaration) and self.idx not in declaration.initialized_fields:
                print("Ostrzezenie w linii %i: %s[%i] moze nie byc zainicjowane" %
                      (self.line_number, self.pid, self.idx))
            asm_code.extend(Instructions.set_register_const(REG.F, address))
            asm_code.append(Instructions.makeInstr('LOAD', REG.F.value))
            asm_code.append(Instructions.makeInstr('PUT', REG.E.value))
        return asm_code

    def translate_left_cond_get_value(self):
        asm_code = []
        memory_manager: MemoryManager = MemoryManager()
        if self.parent_procedure is not None:
            variable_id = self.parent_procedure + "##" + self.pid
            declaration = memory_manager.get_variable(variable_id, self.line_number)
            if not declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Zmienna %s nie jest tablica" % (self.line_number,
                                                                                            self.pid))

            if declaration.is_param:
                address = declaration.get_memory_id()
                # if (not declaration[address].is_initialized) and (not declaration.must_be_initialized):
                #     declaration.set_uninitialized_error(self.pid, self.line_number)
                asm_code.extend(Instructions.set_register_const(REG.F, address))
                asm_code.append(Instructions.makeInstr('LOAD', REG.F.value))
                asm_code.extend(Instructions.set_register_const(REG.G, self.idx))
                asm_code.append(Instructions.ADD(REG.G))
                asm_code.append(Instructions.makeInstr('LOAD', REG.A.value))
                asm_code.append(Instructions.makeInstr('PUT', REG.C.value))
            else:
                if self.idx < 0 or self.idx >= declaration.array_size:
                    raise ArrayUsageException("Blad w linii %i: Proba odwolania sie do komorki z poza tablicy %s" % (
                        self.line_number, self.pid))
                address = declaration.get_memory_id() + self.idx
                if isinstance(declaration, ArrayDeclaration) and self.idx not in declaration.initialized_fields:
                    print("Ostrzezenie w linii %i: %s[%i] moze nie byc zainicjowane" %
                          (self.line_number, self.pid, self.idx))
                asm_code.extend(Instructions.set_register_const(REG.F, address))
                asm_code.append(Instructions.makeInstr('LOAD', REG.F.value))
                asm_code.append(Instructions.makeInstr('PUT', REG.C.value))
        else:
            declaration = memory_manager.get_variable(self.pid, self.line_number)
            if not declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Zmienna %s nie jest tablica" % (self.line_number,
                                                                                            self.pid))
            if self.idx < 0 or self.idx >= declaration.array_size:
                raise ArrayUsageException("Blad w linii %i: Proba odwolania sie do komorki z poza tablicy %s" % (
                    self.line_number, self.pid))
            address = declaration.get_memory_id() + self.idx
            if isinstance(declaration, ArrayDeclaration) and self.idx not in declaration.initialized_fields:
                print("Ostrzezenie w linii %i: %s[%i] moze nie byc zainicjowane" %
                      (self.line_number, self.pid, self.idx))
            asm_code.extend(Instructions.set_register_const(REG.F, address))
            asm_code.append(Instructions.makeInstr('LOAD', REG.F.value))
            asm_code.append(Instructions.makeInstr('PUT', REG.C.value))
        return asm_code

    def translate_right_cond_get_value(self):
        asm_code = []
        memory_manager: MemoryManager = MemoryManager()
        if self.parent_procedure is not None:
            variable_id = self.parent_procedure + "##" + self.pid
            declaration = memory_manager.get_variable(variable_id, self.line_number)
            if not declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Zmienna %s nie jest tablica" % (self.line_number,
                                                                                            self.pid))

            if declaration.is_param:
                address = declaration.get_memory_id()
                # if (not declaration[address].is_initialized) and (not declaration.must_be_initialized):
                #     declaration.set_uninitialized_error(self.pid, self.line_number)
                asm_code.extend(Instructions.set_register_const(REG.F, address))
                asm_code.append(Instructions.makeInstr('LOAD', REG.F.value))
                asm_code.extend(Instructions.set_register_const(REG.G, self.idx))
                asm_code.append(Instructions.ADD(REG.G))
                asm_code.append(Instructions.makeInstr('LOAD', REG.A.value))
                asm_code.append(Instructions.makeInstr('PUT', REG.D.value))
            else:
                if self.idx < 0 or self.idx >= declaration.array_size:
                    raise ArrayUsageException("Blad w linii %i: Proba odwolania sie do komorki z poza tablicy %s" % (
                        self.line_number, self.pid))
                address = declaration.get_memory_id() + self.idx
                if isinstance(declaration, ArrayDeclaration) and self.idx not in declaration.initialized_fields:
                    print("Ostrzezenie w linii %i: %s[%i] moze nie byc zainicjowane" %
                          (self.line_number, self.pid, self.idx))
                asm_code.extend(Instructions.set_register_const(REG.F, address))
                asm_code.append(Instructions.makeInstr('LOAD', REG.F.value))
                asm_code.append(Instructions.makeInstr('PUT', REG.D.value))
        else:
            declaration = memory_manager.get_variable(self.pid, self.line_number)
            if not declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Zmienna %s nie jest tablica" % (self.line_number,
                                                                                            self.pid))
            if self.idx < 0 or self.idx >= declaration.array_size:
                raise ArrayUsageException("Blad w linii %i: Proba odwolania sie do komorki z poza tablicy %s" % (
                    self.line_number, self.pid))
            address = declaration.get_memory_id() + self.idx
            if isinstance(declaration, ArrayDeclaration) and self.idx not in declaration.initialized_fields:
                print("Ostrzezenie w linii %i: %s[%i] moze nie byc zainicjowane" %
                      (self.line_number, self.pid, self.idx))
            asm_code.extend(Instructions.set_register_const(REG.F, address))
            asm_code.append(Instructions.makeInstr('LOAD', REG.F.value))
            asm_code.append(Instructions.makeInstr('PUT', REG.D.value))
        return asm_code


class ArrayPidIdentifier(Identifier):
    def __init__(self, pid, index_pid, line_number=-1):
        super(ArrayPidIdentifier, self).__init__(pid, line_number)
        self.index_pid = index_pid

    def translate_set_value(self):
        asm_code = []
        memory_manager: MemoryManager = MemoryManager()
        if self.parent_procedure is not None:
            variable_id = self.parent_procedure + "##" + self.pid
            idx_variable_id = self.parent_procedure + "##" + self.index_pid
            declaration = memory_manager.get_variable(variable_id, self.line_number)
            if not declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Zmienna %s nie jest tablica" % (self.line_number,
                                                                                            self.pid))
            idx_declaration = memory_manager.get_variable(idx_variable_id, self.line_number)
            if idx_declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Niewlasciwe uzycie tablicy %s" % (self.line_number,
                                                                                              self.index_pid))
            asm_code.append(Instructions.PUT(REG.H))
            beg_address = declaration.get_memory_id()
            idx_address = idx_declaration.get_memory_id()
            if declaration.is_param and idx_declaration.is_param:
                asm_code.extend(Instructions.set_register_const(REG.F, idx_address))
                asm_code.append(Instructions.LOAD(REG.F))
                asm_code.append(Instructions.LOAD(REG.A))
                asm_code.append(Instructions.PUT(REG.F))
                asm_code.extend(Instructions.set_register_const(REG.B, beg_address))
                asm_code.append(Instructions.LOAD(REG.B))
                asm_code.append(Instructions.ADD(REG.F))
                asm_code.append(Instructions.PUT(REG.B))
                asm_code.append(Instructions.GET(REG.H))
                asm_code.append(Instructions.STORE(REG.B))
            elif declaration.is_param and idx_declaration.is_local:
                if not idx_declaration.is_initialized:
                    print("Ostrzerzenie: Zmienna %s w linii %i moze byc niezainicjowana" % (self.index_pid,
                                                                                           self.line_number))
                asm_code.extend(Instructions.set_register_const(REG.F, idx_address))
                asm_code.append(Instructions.LOAD(REG.F))
                asm_code.append(Instructions.PUT(REG.F))
                asm_code.extend(Instructions.set_register_const(REG.B, beg_address))
                asm_code.append(Instructions.LOAD(REG.B))
                asm_code.append(Instructions.ADD(REG.F))
                asm_code.append(Instructions.PUT(REG.B))
                asm_code.append(Instructions.GET(REG.H))
                asm_code.append(Instructions.STORE(REG.B))
            elif declaration.is_local and idx_declaration.is_param:
                asm_code.extend(Instructions.set_register_const(REG.B, beg_address))
                asm_code.extend(Instructions.set_register_const(REG.F, idx_address))
                asm_code.append(Instructions.LOAD(REG.F))
                asm_code.append(Instructions.LOAD(REG.A))
                asm_code.append(Instructions.ADD(REG.B))
                asm_code.append(Instructions.PUT(REG.B))
                asm_code.append(Instructions.GET(REG.H))
                asm_code.append(Instructions.STORE(REG.B))
            else:
                if not idx_declaration.is_initialized:
                    print("Ostrzerzenie: Zmienna %s w linii %i moze byc niezainicjowana" % (self.index_pid,
                                                                                            self.line_number))
                asm_code.extend(Instructions.set_register_const(REG.B, beg_address))
                asm_code.extend(Instructions.set_register_const(REG.F, idx_address))
                asm_code.append(Instructions.LOAD(REG.F))
                asm_code.append(Instructions.ADD(REG.B))
                asm_code.append(Instructions.PUT(REG.B))
                asm_code.append(Instructions.GET(REG.H))
                asm_code.append(Instructions.STORE(REG.B))
        else:
            declaration = memory_manager.get_variable(self.pid, self.line_number)
            if not declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Zmienna %s nie jest tablica" % (self.line_number,
                                                                                            self.pid))
            idx_declaration = memory_manager.get_variable(self.index_pid, self.line_number)
            if idx_declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Niewlasciwe uzycie tablicy %s" % (self.line_number,
                                                                                              self.index_pid))
            if not idx_declaration.is_initialized:
                print("Ostrzerzenie: Zmienna %s w linii %i moze byc niezainicjowana" % (self.index_pid,
                                                                                        self.line_number))
            asm_code.append(Instructions.PUT(REG.H))
            beg_address = declaration.get_memory_id()
            asm_code.extend(Instructions.set_register_const(REG.B, beg_address))
            idx_address = idx_declaration.get_memory_id()
            asm_code.extend(Instructions.set_register_const(REG.F, idx_address))
            asm_code.append(Instructions.LOAD(REG.F))
            asm_code.append(Instructions.ADD(REG.B))
            asm_code.append(Instructions.PUT(REG.B))
            asm_code.append(Instructions.GET(REG.H))
            asm_code.append(Instructions.STORE(REG.B))
        return asm_code

    def translate_write_get_value(self):
        asm_code = []
        memory_manager: MemoryManager = MemoryManager()
        if self.parent_procedure is not None:
            variable_id = self.parent_procedure + "##" + self.pid
            idx_variable_id = self.parent_procedure + "##" + self.index_pid
            declaration = memory_manager.get_variable(variable_id, self.line_number)
            idx_declaration = memory_manager.get_variable(idx_variable_id, self.line_number)
            if not declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Zmienna %s nie jest tablica" % (self.line_number,
                                                                                            self.pid))
            if idx_declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Niewlasciwe uzycie tablicy %s" % (self.line_number,
                                                                                              self.index_pid))
            address = declaration.get_memory_id()
            idx_address = idx_declaration.get_memory_id()
            if declaration.is_param and idx_declaration.is_param:
                asm_code.extend(Instructions.set_register_const(REG.G, address))
                asm_code.append(Instructions.LOAD(REG.G))
                asm_code.append(Instructions.PUT(REG.G))
                asm_code.extend(Instructions.set_register_const(REG.F, idx_address))
                asm_code.append(Instructions.makeInstr('LOAD', REG.F.value))
                asm_code.append(Instructions.makeInstr('LOAD', REG.A.value))
                asm_code.append(Instructions.ADD(REG.G))
                # asm_code.append(Instructions.PUT(REG.G))
                asm_code.append(Instructions.LOAD(REG.A))
            elif declaration.is_param and idx_declaration.is_local:
                if not idx_declaration.is_initialized:
                    print("Ostrzerzenie: Zmienna %s w linii %i moze byc niezainicjowana" % (self.index_pid,
                                                                                            self.line_number))
                asm_code.extend(Instructions.set_register_const(REG.G, address))
                asm_code.append(Instructions.LOAD(REG.G))
                asm_code.append(Instructions.PUT(REG.G))
                asm_code.extend(Instructions.set_register_const(REG.F, idx_address))
                asm_code.append(Instructions.makeInstr('LOAD', REG.F.value))
                asm_code.append(Instructions.ADD(REG.G))
                # asm_code.append(Instructions.PUT(REG.G))
                asm_code.append(Instructions.LOAD(REG.A))
            elif declaration.is_local and idx_declaration.is_param:
                asm_code.extend(Instructions.set_register_const(REG.G, address))
                asm_code.extend(Instructions.set_register_const(REG.F, idx_address))
                asm_code.append(Instructions.makeInstr('LOAD', REG.F.value))
                asm_code.append(Instructions.makeInstr('LOAD', REG.A.value))
                asm_code.append(Instructions.ADD(REG.G))
                asm_code.append(Instructions.LOAD(REG.A))
            else:
                if not idx_declaration.is_initialized:
                    print("Ostrzerzenie: Zmienna %s w linii %i moze byc niezainicjowana" % (self.index_pid,
                                                                                            self.line_number))
                asm_code.extend(Instructions.set_register_const(REG.G, address))
                asm_code.extend(Instructions.set_register_const(REG.F, idx_address))
                asm_code.append(Instructions.makeInstr('LOAD', REG.F.value))
                asm_code.append(Instructions.ADD(REG.G))
                asm_code.append(Instructions.LOAD(REG.A))
        else:
            declaration = memory_manager.get_variable(self.pid, self.line_number)
            if not declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Zmienna %s nie jest tablica" % (self.line_number,
                                                                                            self.pid))
            idx_declaration = memory_manager.get_variable(self.index_pid, self.line_number)
            if idx_declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Niewlasciwe uzycie tablicy %s" % (self.line_number,
                                                                                              self.index_pid))
            if not idx_declaration.is_initialized:
                print("Ostrzerzenie: Zmienna %s w linii %i moze byc niezainicjowana" % (self.index_pid,
                                                                                        self.line_number))
            beg_address = declaration.get_memory_id()
            idx_address = idx_declaration.get_memory_id()
            asm_code.extend(Instructions.set_register_const(REG.G, beg_address))
            asm_code.extend(Instructions.set_register_const(REG.F, idx_address))
            asm_code.append(Instructions.makeInstr('LOAD', REG.F.value))
            asm_code.append(Instructions.ADD(REG.G))
            # asm_code.append(Instructions.PUT(REG.G))
            asm_code.append(Instructions.LOAD(REG.A))
        return asm_code

    def translate_assign_get_value(self):
        asm_code = []
        memory_manager: MemoryManager = MemoryManager()
        if self.parent_procedure is not None:
            variable_id = self.parent_procedure + "##" + self.pid
            idx_variable_id = self.parent_procedure + "##" + self.index_pid
            declaration = memory_manager.get_variable(variable_id, self.line_number)
            idx_declaration = memory_manager.get_variable(idx_variable_id, self.line_number)
            if not declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Zmienna %s nie jest tablica" % (self.line_number,
                                                                                            self.pid))
            if idx_declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Niewlasciwe uzycie tablicy %s" % (self.line_number,
                                                                                              self.index_pid))
            address = declaration.get_memory_id()
            idx_address = idx_declaration.get_memory_id()
            if declaration.is_param and idx_declaration.is_param:
                asm_code.extend(Instructions.set_register_const(REG.G, address))
                asm_code.append(Instructions.LOAD(REG.G))
                asm_code.append(Instructions.PUT(REG.G))
                asm_code.extend(Instructions.set_register_const(REG.F, idx_address))
                asm_code.append(Instructions.makeInstr('LOAD', REG.F.value))
                asm_code.append(Instructions.makeInstr('LOAD', REG.A.value))
                asm_code.append(Instructions.ADD(REG.G))
                # asm_code.append(Instructions.PUT(REG.G))
                asm_code.append(Instructions.LOAD(REG.A))
            elif declaration.is_param and idx_declaration.is_local:
                if not idx_declaration.is_initialized:
                    print("Ostrzerzenie: Zmienna %s w linii %i moze byc niezainicjowana" % (self.index_pid,
                                                                                            self.line_number))
                asm_code.extend(Instructions.set_register_const(REG.G, address))
                asm_code.append(Instructions.LOAD(REG.G))
                asm_code.append(Instructions.PUT(REG.G))
                asm_code.extend(Instructions.set_register_const(REG.F, idx_address))
                asm_code.append(Instructions.makeInstr('LOAD', REG.F.value))
                asm_code.append(Instructions.ADD(REG.G))
                # asm_code.append(Instructions.PUT(REG.G))
                asm_code.append(Instructions.LOAD(REG.A))
            elif declaration.is_local and idx_declaration.is_param:
                asm_code.extend(Instructions.set_register_const(REG.G, address))
                asm_code.extend(Instructions.set_register_const(REG.F, idx_address))
                asm_code.append(Instructions.makeInstr('LOAD', REG.F.value))
                asm_code.append(Instructions.makeInstr('LOAD', REG.A.value))
                asm_code.append(Instructions.ADD(REG.G))
                asm_code.append(Instructions.LOAD(REG.A))
            else:
                if not idx_declaration.is_initialized:
                    print("Ostrzerzenie: Zmienna %s w linii %i moze byc niezainicjowana" % (self.index_pid,
                                                                                            self.line_number))
                asm_code.extend(Instructions.set_register_const(REG.G, address))
                asm_code.extend(Instructions.set_register_const(REG.F, idx_address))
                asm_code.append(Instructions.makeInstr('LOAD', REG.F.value))
                asm_code.append(Instructions.ADD(REG.G))
                asm_code.append(Instructions.LOAD(REG.A))
        else:
            declaration = memory_manager.get_variable(self.pid, self.line_number)
            if not declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Zmienna %s nie jest tablica" % (self.line_number,
                                                                                            self.pid))
            idx_declaration = memory_manager.get_variable(self.index_pid, self.line_number)
            if idx_declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Niewlasciwe uzycie tablicy %s" % (self.line_number,
                                                                                              self.index_pid))
            if not idx_declaration.is_initialized:
                print("Ostrzerzenie: Zmienna %s w linii %i moze byc niezainicjowana" % (self.index_pid,
                                                                                        self.line_number))
            beg_address = declaration.get_memory_id()
            idx_address = idx_declaration.get_memory_id()
            asm_code.extend(Instructions.set_register_const(REG.G, beg_address))
            asm_code.extend(Instructions.set_register_const(REG.F, idx_address))
            asm_code.append(Instructions.makeInstr('LOAD', REG.F.value))
            asm_code.append(Instructions.ADD(REG.G))
            # asm_code.append(Instructions.PUT(REG.G))
            asm_code.append(Instructions.LOAD(REG.A))
        return asm_code

    def translate_left_op_get_value(self):
        asm_code = []
        memory_manager: MemoryManager = MemoryManager()
        if self.parent_procedure is not None:
            variable_id = self.parent_procedure + "##" + self.pid
            idx_variable_id = self.parent_procedure + "##" + self.index_pid
            declaration = memory_manager.get_variable(variable_id, self.line_number)
            idx_declaration = memory_manager.get_variable(idx_variable_id, self.line_number)
            if not declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Zmienna %s nie jest tablica" % (self.line_number,
                                                                                            self.pid))
            if idx_declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Niewlasciwe uzycie tablicy %s" % (self.line_number,
                                                                                              self.index_pid))
            address = declaration.get_memory_id()
            idx_address = idx_declaration.get_memory_id()
            if declaration.is_param and idx_declaration.is_param:
                asm_code.extend(Instructions.set_register_const(REG.G, address))
                asm_code.append(Instructions.LOAD(REG.G))
                asm_code.append(Instructions.PUT(REG.G))
                asm_code.extend(Instructions.set_register_const(REG.F, idx_address))
                asm_code.append(Instructions.makeInstr('LOAD', REG.F.value))
                asm_code.append(Instructions.makeInstr('LOAD', REG.A.value))
                asm_code.append(Instructions.ADD(REG.G))
                # asm_code.append(Instructions.PUT(REG.G))
                asm_code.append(Instructions.LOAD(REG.A))
                asm_code.append(Instructions.PUT(REG.B))
            elif declaration.is_param and idx_declaration.is_local:
                if not idx_declaration.is_initialized:
                    print("Ostrzerzenie: Zmienna %s w linii %i moze byc niezainicjowana" % (self.index_pid,
                                                                                            self.line_number))
                asm_code.extend(Instructions.set_register_const(REG.G, address))
                asm_code.append(Instructions.LOAD(REG.G))
                asm_code.append(Instructions.PUT(REG.G))
                asm_code.extend(Instructions.set_register_const(REG.F, idx_address))
                asm_code.append(Instructions.makeInstr('LOAD', REG.F.value))
                asm_code.append(Instructions.ADD(REG.G))
                # asm_code.append(Instructions.PUT(REG.G))
                asm_code.append(Instructions.LOAD(REG.A))
                asm_code.append(Instructions.PUT(REG.B))
            elif declaration.is_local and idx_declaration.is_param:
                asm_code.extend(Instructions.set_register_const(REG.G, address))
                asm_code.extend(Instructions.set_register_const(REG.F, idx_address))
                asm_code.append(Instructions.makeInstr('LOAD', REG.F.value))
                asm_code.append(Instructions.makeInstr('LOAD', REG.A.value))
                asm_code.append(Instructions.ADD(REG.G))
                asm_code.append(Instructions.LOAD(REG.A))
                asm_code.append(Instructions.PUT(REG.B))
            else:
                if not idx_declaration.is_initialized:
                    print("Ostrzerzenie: Zmienna %s w linii %i moze byc niezainicjowana" % (self.index_pid,
                                                                                            self.line_number))
                asm_code.extend(Instructions.set_register_const(REG.G, address))
                asm_code.extend(Instructions.set_register_const(REG.F, idx_address))
                asm_code.append(Instructions.makeInstr('LOAD', REG.F.value))
                asm_code.append(Instructions.ADD(REG.G))
                asm_code.append(Instructions.LOAD(REG.A))
                asm_code.append(Instructions.PUT(REG.B))
        else:
            declaration = memory_manager.get_variable(self.pid, self.line_number)
            if not declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Zmienna %s nie jest tablica" % (self.line_number,
                                                                                            self.pid))
            idx_declaration = memory_manager.get_variable(self.index_pid, self.line_number)
            if idx_declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Niewlasciwe uzycie tablicy %s" % (self.line_number,
                                                                                              self.index_pid))
            if not idx_declaration.is_initialized:
                print("Ostrzerzenie: Zmienna %s w linii %i moze byc niezainicjowana" % (self.index_pid,
                                                                                        self.line_number))
            beg_address = declaration.get_memory_id()
            idx_address = idx_declaration.get_memory_id()
            asm_code.extend(Instructions.set_register_const(REG.G, beg_address))
            asm_code.extend(Instructions.set_register_const(REG.F, idx_address))
            asm_code.append(Instructions.makeInstr('LOAD', REG.F.value))
            asm_code.append(Instructions.ADD(REG.G))
            # asm_code.append(Instructions.PUT(REG.G))
            asm_code.append(Instructions.LOAD(REG.A))
            asm_code.append(Instructions.PUT(REG.B))
        return asm_code

    def translate_right_op_get_value(self):
        asm_code = []
        memory_manager: MemoryManager = MemoryManager()
        if self.parent_procedure is not None:
            variable_id = self.parent_procedure + "##" + self.pid
            idx_variable_id = self.parent_procedure + "##" + self.index_pid
            declaration = memory_manager.get_variable(variable_id, self.line_number)
            idx_declaration = memory_manager.get_variable(idx_variable_id, self.line_number)
            if not declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Zmienna %s nie jest tablica" % (self.line_number,
                                                                                            self.pid))
            if idx_declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Niewlasciwe uzycie tablicy %s" % (self.line_number,
                                                                                              self.index_pid))
            address = declaration.get_memory_id()
            idx_address = idx_declaration.get_memory_id()
            if declaration.is_param and idx_declaration.is_param:
                asm_code.extend(Instructions.set_register_const(REG.G, address))
                asm_code.append(Instructions.LOAD(REG.G))
                asm_code.append(Instructions.PUT(REG.G))
                asm_code.extend(Instructions.set_register_const(REG.F, idx_address))
                asm_code.append(Instructions.makeInstr('LOAD', REG.F.value))
                asm_code.append(Instructions.makeInstr('LOAD', REG.A.value))
                asm_code.append(Instructions.ADD(REG.G))
                # asm_code.append(Instructions.PUT(REG.G))
                asm_code.append(Instructions.LOAD(REG.A))
                asm_code.append(Instructions.PUT(REG.E))
            elif declaration.is_param and idx_declaration.is_local:
                if not idx_declaration.is_initialized:
                    print("Ostrzerzenie: Zmienna %s w linii %i moze byc niezainicjowana" % (self.index_pid,
                                                                                            self.line_number))
                asm_code.extend(Instructions.set_register_const(REG.G, address))
                asm_code.append(Instructions.LOAD(REG.G))
                asm_code.append(Instructions.PUT(REG.G))
                asm_code.extend(Instructions.set_register_const(REG.F, idx_address))
                asm_code.append(Instructions.makeInstr('LOAD', REG.F.value))
                asm_code.append(Instructions.ADD(REG.G))
                # asm_code.append(Instructions.PUT(REG.G))
                asm_code.append(Instructions.LOAD(REG.A))
                asm_code.append(Instructions.PUT(REG.E))
            elif declaration.is_local and idx_declaration.is_param:
                asm_code.extend(Instructions.set_register_const(REG.G, address))
                asm_code.extend(Instructions.set_register_const(REG.F, idx_address))
                asm_code.append(Instructions.makeInstr('LOAD', REG.F.value))
                asm_code.append(Instructions.makeInstr('LOAD', REG.A.value))
                asm_code.append(Instructions.ADD(REG.G))
                asm_code.append(Instructions.LOAD(REG.A))
                asm_code.append(Instructions.PUT(REG.E))
            else:
                if not idx_declaration.is_initialized:
                    print("Ostrzerzenie: Zmienna %s w linii %i moze byc niezainicjowana" % (self.index_pid,
                                                                                            self.line_number))
                asm_code.extend(Instructions.set_register_const(REG.G, address))
                asm_code.extend(Instructions.set_register_const(REG.F, idx_address))
                asm_code.append(Instructions.makeInstr('LOAD', REG.F.value))
                asm_code.append(Instructions.ADD(REG.G))
                asm_code.append(Instructions.LOAD(REG.A))
                asm_code.append(Instructions.PUT(REG.E))
        else:
            declaration = memory_manager.get_variable(self.pid, self.line_number)
            if not declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Zmienna %s nie jest tablica" % (self.line_number,
                                                                                            self.pid))
            idx_declaration = memory_manager.get_variable(self.index_pid, self.line_number)
            if idx_declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Niewlasciwe uzycie tablicy %s" % (self.line_number,
                                                                                              self.index_pid))
            if not idx_declaration.is_initialized:
                print("Ostrzerzenie: Zmienna %s w linii %i moze byc niezainicjowana" % (self.index_pid,
                                                                                        self.line_number))
            beg_address = declaration.get_memory_id()
            idx_address = idx_declaration.get_memory_id()
            asm_code.extend(Instructions.set_register_const(REG.G, beg_address))
            asm_code.extend(Instructions.set_register_const(REG.F, idx_address))
            asm_code.append(Instructions.makeInstr('LOAD', REG.F.value))
            asm_code.append(Instructions.ADD(REG.G))
            # asm_code.append(Instructions.PUT(REG.G))
            asm_code.append(Instructions.LOAD(REG.A))
            asm_code.append(Instructions.PUT(REG.E))
        return asm_code

    def translate_left_cond_get_value(self):
        asm_code = []
        memory_manager: MemoryManager = MemoryManager()
        if self.parent_procedure is not None:
            variable_id = self.parent_procedure + "##" + self.pid
            idx_variable_id = self.parent_procedure + "##" + self.index_pid
            declaration = memory_manager.get_variable(variable_id, self.line_number)
            idx_declaration = memory_manager.get_variable(idx_variable_id, self.line_number)
            if not declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Zmienna %s nie jest tablica" % (self.line_number,
                                                                                            self.pid))
            if idx_declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Niewlasciwe uzycie tablicy %s" % (self.line_number,
                                                                                              self.index_pid))
            address = declaration.get_memory_id()
            idx_address = idx_declaration.get_memory_id()
            if declaration.is_param and idx_declaration.is_param:
                asm_code.extend(Instructions.set_register_const(REG.G, address))
                asm_code.append(Instructions.LOAD(REG.G))
                asm_code.append(Instructions.PUT(REG.G))
                asm_code.extend(Instructions.set_register_const(REG.F, idx_address))
                asm_code.append(Instructions.makeInstr('LOAD', REG.F.value))
                asm_code.append(Instructions.makeInstr('LOAD', REG.A.value))
                asm_code.append(Instructions.ADD(REG.G))
                # asm_code.append(Instructions.PUT(REG.G))
                asm_code.append(Instructions.LOAD(REG.A))
                asm_code.append(Instructions.PUT(REG.C))
            elif declaration.is_param and idx_declaration.is_local:
                if not idx_declaration.is_initialized:
                    print("Ostrzerzenie: Zmienna %s w linii %i moze byc niezainicjowana" % (self.index_pid,
                                                                                            self.line_number))
                asm_code.extend(Instructions.set_register_const(REG.G, address))
                asm_code.append(Instructions.LOAD(REG.G))
                asm_code.append(Instructions.PUT(REG.G))
                asm_code.extend(Instructions.set_register_const(REG.F, idx_address))
                asm_code.append(Instructions.makeInstr('LOAD', REG.F.value))
                asm_code.append(Instructions.ADD(REG.G))
                # asm_code.append(Instructions.PUT(REG.G))
                asm_code.append(Instructions.LOAD(REG.A))
                asm_code.append(Instructions.PUT(REG.C))
            elif declaration.is_local and idx_declaration.is_param:
                asm_code.extend(Instructions.set_register_const(REG.G, address))
                asm_code.extend(Instructions.set_register_const(REG.F, idx_address))
                asm_code.append(Instructions.makeInstr('LOAD', REG.F.value))
                asm_code.append(Instructions.makeInstr('LOAD', REG.A.value))
                asm_code.append(Instructions.ADD(REG.G))
                asm_code.append(Instructions.LOAD(REG.A))
                asm_code.append(Instructions.PUT(REG.C))
            else:
                if not idx_declaration.is_initialized:
                    print("Ostrzerzenie: Zmienna %s w linii %i moze byc niezainicjowana" % (self.index_pid,
                                                                                            self.line_number))
                asm_code.extend(Instructions.set_register_const(REG.G, address))
                asm_code.extend(Instructions.set_register_const(REG.F, idx_address))
                asm_code.append(Instructions.makeInstr('LOAD', REG.F.value))
                asm_code.append(Instructions.ADD(REG.G))
                asm_code.append(Instructions.LOAD(REG.A))
                asm_code.append(Instructions.PUT(REG.C))
        else:
            declaration = memory_manager.get_variable(self.pid, self.line_number)
            if not declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Zmienna %s nie jest tablica" % (self.line_number,
                                                                                            self.pid))
            idx_declaration = memory_manager.get_variable(self.index_pid, self.line_number)
            if idx_declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Niewlasciwe uzycie tablicy %s" % (self.line_number,
                                                                                              self.index_pid))
            if not idx_declaration.is_initialized:
                print("Ostrzerzenie: Zmienna %s w linii %i moze byc niezainicjowana" % (self.index_pid,
                                                                                        self.line_number))
            beg_address = declaration.get_memory_id()
            idx_address = idx_declaration.get_memory_id()
            asm_code.extend(Instructions.set_register_const(REG.G, beg_address))
            asm_code.extend(Instructions.set_register_const(REG.F, idx_address))
            asm_code.append(Instructions.makeInstr('LOAD', REG.F.value))
            asm_code.append(Instructions.ADD(REG.G))
            # asm_code.append(Instructions.PUT(REG.G))
            asm_code.append(Instructions.LOAD(REG.A))
            asm_code.append(Instructions.PUT(REG.C))
        return asm_code

    def translate_right_cond_get_value(self):
        asm_code = []
        memory_manager: MemoryManager = MemoryManager()
        if self.parent_procedure is not None:
            variable_id = self.parent_procedure + "##" + self.pid
            idx_variable_id = self.parent_procedure + "##" + self.index_pid
            declaration = memory_manager.get_variable(variable_id, self.line_number)
            idx_declaration = memory_manager.get_variable(idx_variable_id, self.line_number)
            if not declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Zmienna %s nie jest tablica" % (self.line_number,
                                                                                            self.pid))
            if idx_declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Niewlasciwe uzycie tablicy %s" % (self.line_number,
                                                                                              self.index_pid))
            address = declaration.get_memory_id()
            idx_address = idx_declaration.get_memory_id()
            if declaration.is_param and idx_declaration.is_param:
                asm_code.extend(Instructions.set_register_const(REG.G, address))
                asm_code.append(Instructions.LOAD(REG.G))
                asm_code.append(Instructions.PUT(REG.G))
                asm_code.extend(Instructions.set_register_const(REG.F, idx_address))
                asm_code.append(Instructions.makeInstr('LOAD', REG.F.value))
                asm_code.append(Instructions.makeInstr('LOAD', REG.A.value))
                asm_code.append(Instructions.ADD(REG.G))
                # asm_code.append(Instructions.PUT(REG.G))
                asm_code.append(Instructions.LOAD(REG.A))
                asm_code.append(Instructions.PUT(REG.D))
            elif declaration.is_param and idx_declaration.is_local:
                if not idx_declaration.is_initialized:
                    print("Ostrzerzenie: Zmienna %s w linii %i moze byc niezainicjowana" % (self.index_pid,
                                                                                            self.line_number))
                asm_code.extend(Instructions.set_register_const(REG.G, address))
                asm_code.append(Instructions.LOAD(REG.G))
                asm_code.append(Instructions.PUT(REG.G))
                asm_code.extend(Instructions.set_register_const(REG.F, idx_address))
                asm_code.append(Instructions.makeInstr('LOAD', REG.F.value))
                asm_code.append(Instructions.ADD(REG.G))
                # asm_code.append(Instructions.PUT(REG.G))
                asm_code.append(Instructions.LOAD(REG.A))
                asm_code.append(Instructions.PUT(REG.D))
            elif declaration.is_local and idx_declaration.is_param:
                asm_code.extend(Instructions.set_register_const(REG.G, address))
                asm_code.extend(Instructions.set_register_const(REG.F, idx_address))
                asm_code.append(Instructions.makeInstr('LOAD', REG.F.value))
                asm_code.append(Instructions.makeInstr('LOAD', REG.A.value))
                asm_code.append(Instructions.ADD(REG.G))
                asm_code.append(Instructions.LOAD(REG.A))
                asm_code.append(Instructions.PUT(REG.D))
            else:
                if not idx_declaration.is_initialized:
                    print("Ostrzerzenie: Zmienna %s w linii %i moze byc niezainicjowana" % (self.index_pid,
                                                                                            self.line_number))
                asm_code.extend(Instructions.set_register_const(REG.G, address))
                asm_code.extend(Instructions.set_register_const(REG.F, idx_address))
                asm_code.append(Instructions.makeInstr('LOAD', REG.F.value))
                asm_code.append(Instructions.ADD(REG.G))
                asm_code.append(Instructions.LOAD(REG.A))
                asm_code.append(Instructions.PUT(REG.D))
        else:
            declaration = memory_manager.get_variable(self.pid, self.line_number)
            if not declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Zmienna %s nie jest tablica" % (self.line_number,
                                                                                            self.pid))
            idx_declaration = memory_manager.get_variable(self.index_pid, self.line_number)
            if idx_declaration.is_array:
                raise ArrayUsageException("Blad w linii %i: Niewlasciwe uzycie tablicy %s" % (self.line_number,
                                                                                              self.index_pid))
            if not idx_declaration.is_initialized:
                print("Ostrzerzenie: Zmienna %s w linii %i moze byc niezainicjowana" % (self.index_pid,
                                                                                        self.line_number))
            beg_address = declaration.get_memory_id()
            idx_address = idx_declaration.get_memory_id()
            asm_code.extend(Instructions.set_register_const(REG.G, beg_address))
            asm_code.extend(Instructions.set_register_const(REG.F, idx_address))
            asm_code.append(Instructions.makeInstr('LOAD', REG.F.value))
            asm_code.append(Instructions.ADD(REG.G))
            # asm_code.append(Instructions.PUT(REG.G))
            asm_code.append(Instructions.LOAD(REG.A))
            asm_code.append(Instructions.PUT(REG.D))
        return asm_code


class ArrayUsageException(Exception):
    def __init__(self, msg):
        self.message = msg
