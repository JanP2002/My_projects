from NonTerminals.Condition import ConditionNumNum,  \
    ConditionNumIdentifier, ConditionIdentifierNum, ConditionIdentifierIdentifier
from NonTerminals.Identifier import Identifier, ArrayNumIdentifier, ArrayPidIdentifier
from NonTerminals.ProcCallParam import ProcCallParam
from NonTerminals.ProcHead import ProcHead
from NonTerminals.Procedure import Procedure
from lexer import lexer, tokens
import ply.yacc as yacc
from Program import Program
from NonTerminals.Main import Main
from NonTerminals.Command import CommandWriteNum, \
    ProcCall, CommandIf, CommandIfElse, \
    CommandWhile, CommandRepeatUntil, CommandWriteIdentifier, \
    CommandReadIdentifier, CommandIdentifierAssignNum, CommandIdentifierAssignIdentifier, \
    CommandIdentifierAssignNumOpNum, CommandIdentifierAssignNumOpIdentifier, CommandIdentifierAssignIdentifierOpNum, \
    CommandIdentifierAssignIdentifierOpIdentifier
from NonTerminals.Declarations import VarDeclaration, ParamDeclaration, ArrayDeclaration


def p_program_all_procedures_main(p):
    """program_all : procedures main"""
    p[0] = Program(p[1], p[2])


def p_procedures_declarations_commands(p):
    """procedures : procedures PROCEDURE proc_head IS declarations IN commands END"""
    if not p[1]:
        p[1] = []

    curr_procedure = Procedure(p[3], p[5], p[7])
    p[1].append(curr_procedure)
    p[0] = p[1]


def p_procedures_commands(p):
    """procedures : procedures PROCEDURE proc_head IS IN commands END"""
    if not p[1]:
        p[1] = []

    curr_procedure = Procedure(p[3], [], p[6])
    p[1].append(curr_procedure)
    p[0] = p[1]


def p_procedures_empty(p):
    """procedures : """
    p[0] = []


def p_proc_head(p):
    """proc_head : pid l_paren args_decl r_paren"""
    p[0] = ProcHead(p[1], p[3], p.lineno(1))


def p_proc_call(p):
    """proc_call : pid l_paren args r_paren"""
    p[0] = ProcCall(p[1], p[3], p.lineno(1))


def p_args_decl_append(p):
    """args_decl : args_decl COMMA pid"""
    if not p[1]:
        p[1] = []
    decl1 = ParamDeclaration(p[3], False, p.lineno(2))
    p[1].append(decl1)
    p[0] = p[1]


def p_args_decl_append_array(p):
    """args_decl : args_decl COMMA arr_specificator pid"""
    if not p[1]:
        p[1] = []
    decl1 = ParamDeclaration(p[4], True, p.lineno(2))
    p[1].append(decl1)
    p[0] = p[1]


def p_args_decl(p):
    """args_decl : pid"""
    p[0] = [ParamDeclaration(p[1], False, p.lineno(1))]


def p_args_decl_array(p):
    """args_decl : arr_specificator pid"""
    p[0] = [ParamDeclaration(p[2], True, p.lineno(1))]


def p_args_append(p):
    """args : args COMMA pid"""
    if not p[1]:
        p[1] = []
    param1 = ProcCallParam(p[3], p.lineno(2))
    p[1].append(param1)
    p[0] = p[1]


def p_args(p):
    """args : pid"""
    p[0] = [ProcCallParam(p[1], p.lineno(1))]


def p_main_commands(p):
    """main : PROGRAM IS IN commands END"""
    p[0] = Main([], p[4])


def p_main_declarations_commands(p):
    """main : PROGRAM IS declarations IN commands END"""
    # print(*p[3])
    p[0] = Main(p[3], p[5])


def p_declarations_append(p):
    """declarations : declarations COMMA pid"""
    if not p[1]:
        p[1] = []
    decl1 = VarDeclaration(p[3], False, p.lineno(2))
    p[1].append(decl1)
    p[0] = p[1]


def p_array_declarations_append(p):
    """declarations : declarations COMMA pid arr_l_paren num arr_r_paren"""
    if not p[1]:
        p[1] = []
    decl1 = ArrayDeclaration(p[3], p.lineno(2), False, None, False, p[5])
    p[1].append(decl1)
    p[0] = p[1]


def p_declarations(p):
    """declarations : pid"""
    p[0] = [VarDeclaration(p[1], False, p.lineno(1))]


def p_array_declarations(p):
    """declarations : pid arr_l_paren num arr_r_paren"""
    p[0] = [ArrayDeclaration(p[1], p.lineno(1), False, None, False, p[3])]


def p_commands_append(p):
    """commands  : commands command"""
    if not p[1]:
        p[1] = []
    p[1].append(p[2])
    p[0] = p[1]


def p_commands(p):
    """commands  : command"""
    p[0] = [p[1]]


def p_command_write_num(p):
    """command  : WRITE num SEMICOLON"""
    p[0] = CommandWriteNum(p[2])


def p_command_write_identifier(p):
    """command  : WRITE identifier SEMICOLON"""
    p[0] = CommandWriteIdentifier(p[2], p.lineno(2))


def p_command_read_identifier(p):
    """command : READ identifier SEMICOLON"""
    p[0] = CommandReadIdentifier(p[2])


def p_command_identifier_assign_num(p):
    """command  : identifier ASSIGN num SEMICOLON"""
    p[0] = CommandIdentifierAssignNum(p[1], p[3], p.lineno(2))


def p_command_identifier_assign_identifier(p):
    """command  : identifier ASSIGN identifier SEMICOLON"""
    p[0] = CommandIdentifierAssignIdentifier(p[1], p[3], p.lineno(2))


def p_command_identifier_assign_num_op_num(p):
    """command : identifier ASSIGN num op num SEMICOLON"""
    p[0] = CommandIdentifierAssignNumOpNum(p[1], p[3], p[5], p[4], p.lineno(2))


def p_command_identifier_assign_num_op_identifier(p):
    """command : identifier ASSIGN num op identifier SEMICOLON"""
    p[0] = CommandIdentifierAssignNumOpIdentifier(p[1], p[3], p[5], p[4], p.lineno(2))


def p_command_identifier_assign_identifier_op_num(p):
    """command : identifier ASSIGN identifier op num SEMICOLON"""
    p[0] = CommandIdentifierAssignIdentifierOpNum(p[1], p[3], p[5], p[4], p.lineno(2))


def p_command_identifier_assign_identifier_op_identifier(p):
    """command : identifier ASSIGN identifier op identifier SEMICOLON"""
    p[0] = CommandIdentifierAssignIdentifierOpIdentifier(p[1], p[3], p[5], p[4], p.lineno(2))


def p_identifier_pid(p):
    """identifier : pid"""
    p[0] = Identifier(p[1], p.lineno(1))


def p_identifier_array_num(p):
    """identifier : pid arr_l_paren num arr_r_paren"""
    p[0] = ArrayNumIdentifier(p[1], p[3], p.lineno(1))


def p_identifier_array_pid(p):
    """identifier : pid arr_l_paren pid arr_r_paren"""
    p[0] = ArrayPidIdentifier(p[1], p[3], p.lineno(1))


def p_command_if(p):
    """command : IF condition THEN commands ENDIF"""
    p[0] = CommandIf(p[2], p[4], p.lineno(1))


def p_command_if_else(p):
    """command : IF condition THEN commands ELSE commands ENDIF"""
    p[0] = CommandIfElse(p[2], p[4], p[6], p.lineno(1))


def p_command_while(p):
    """command : WHILE condition DO commands ENDWHILE"""
    p[0] = CommandWhile(p[2], p[4], p.lineno(1))


def p_command_repeat_until(p):
    """command : REPEAT commands UNTIL condition SEMICOLON"""
    p[0] = CommandRepeatUntil(p[4], p[2], p.lineno(1))


def p_condition_num_num(p):
    """condition : num cop num"""
    p[0] = ConditionNumNum(p[1], p[3], p[2], p.lineno(1))


def p_condition_num_identifier(p):
    """condition : num cop identifier"""
    p[0] = ConditionNumIdentifier(p[1], p[3], p[2], p.lineno(1))


def p_condition_identifier_num(p):
    """condition : identifier cop num"""
    p[0] = ConditionIdentifierNum(p[1], p[3], p[2], p.lineno(1))


def p_condition_identifier_identifier(p):
    """condition : identifier cop identifier"""
    p[0] = ConditionIdentifierIdentifier(p[1], p[3], p[2], p.lineno(1))


def p_cop(p):
    """cop : LT
    | GT
    | LE
    | GE
    | EQ
    | NE"""
    p[0] = p[1]


def p_command_proc_call(p):
    """command : proc_call SEMICOLON"""
    p[0] = p[1]


def p_error(p):
    raise SyntaxError("Unexpected token '%s' at line %i" % (p.value, p.lineno))


parser = yacc.yacc()
