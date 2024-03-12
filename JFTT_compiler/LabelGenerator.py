def _generate_label(label_type, number):
    return label_type + str(number) + ":"


class LabelGenerator:
    _instance = None
    if_end_label_counter = 0
    else_label_counter = 0
    while_cond_label_counter = 0
    while_end_label_counter = 0
    repeat_label_counter = 0
    label_shift = 0
    IF_END = "IF_END"
    ELSE = "ELSE"
    WHILE_COND = "WHILE_COND"
    WHILE_END = "WHILE_END"
    REPEAT = "REPEAT"

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        pass

    def next_if_end_label(self):
        self.if_end_label_counter += 1
        self.label_shift += 1
        return _generate_label(self.IF_END, self.if_end_label_counter)

    def next_else_label(self):
        self.else_label_counter += 1
        return _generate_label(self.ELSE, self.else_label_counter)

    def next_while_cond_label(self):
        self.while_cond_label_counter += 1
        return _generate_label(self.WHILE_COND, self.while_cond_label_counter)

    def next_while_end_label(self):
        self.while_end_label_counter += 1
        self.label_shift += 1
        return _generate_label(self.WHILE_END, self.while_end_label_counter)

    def next_repeat_label(self):
        self.repeat_label_counter += 1
        return _generate_label(self.REPEAT, self.repeat_label_counter)

    def get_shift(self):
        return self.label_shift

    def decrement_label_shift(self):
        if self.label_shift > 0:
            self.label_shift -= 1
