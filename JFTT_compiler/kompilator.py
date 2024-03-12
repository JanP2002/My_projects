from parser import parser, lexer
import sys


def read_file(filename):
    with open(filename, "r") as file:
        return file.read()


def write_to_file(filename, content):
    with open(filename, "w") as file:
        file.write(content)


inputFile = sys.argv[1]
outFile = sys.argv[2]
try:
    data = read_file(inputFile)
    print("Plik kompilowany '%s'" % inputFile)
    program = parser.parse(data, lexer)
    output = program.get_asm_code()
    write_to_file(outFile, output)
    print("Plik wyjsciowy: '%s'" % outFile)
except Exception as err:
    print(err)
    #print(err.with_traceback())
    exit(1)
    