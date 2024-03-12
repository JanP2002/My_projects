class VarDeclaration:
    def __init__(self, pid, is_arr=False, line_number=-1, is_local=False, parent_proc=None, is_param=False):
        self.pid = pid
        self.line_number = line_number
        self.is_array = is_arr
        self.memory_id = None
        self.length = 1
        self.is_initialized = False
        self.is_local = is_local
        self.parent_procedure = parent_proc
        self.is_param = is_param

    def is_array(self):
        return self.is_array

    def to_string(self):
        return str((self.pid, self.memory_id, self.length, "Array" if self.is_array else "Var"))

    def set_memory_id(self, mem_id):
        self.memory_id = mem_id

    def get_memory_id(self):
        return self.memory_id


class ParamDeclaration(VarDeclaration):
    def __init__(self, pid, is_array=False, line_number=-1, parent_proc=None):
        super(ParamDeclaration, self).__init__(pid, is_array, line_number, False, parent_proc, True)
        self.is_initialized = False
        self.must_be_initialized = False
        # self.uninitialized_usage_line = None
        # self.context_pid = None
        self.array_size = 0

    # def set_uninitialized_error(self, context_pid, line_number):
    #     self.must_be_initialized = True
    #     self.uninitialized_usage_line = line_number
    #     self.context_pid = context_pid


class ArrayDeclaration(VarDeclaration):
    def __init__(self, pid, line_number=-1, is_local=False, parent_proc=None, is_param=False, array_size=0):
        super(ArrayDeclaration, self).__init__(pid, True, line_number, is_local, parent_proc, is_param)
        self.array_size = array_size
        self.initialized_fields = []
