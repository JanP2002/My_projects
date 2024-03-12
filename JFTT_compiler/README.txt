Jan Poręba 268446

Sposób wywołania kompilatora:
python3 kompilator.py <nazwa pliku wejściowego> <nazwa pliku wyjściowego>

Aby używać kompilatora należy doinstalować
(wykonać następujące polecenia w terminalu Ubuntu):
sudo apt update
sudo apt install python3.11
sudo apt install python3-pip
pip3 install ply

Kompilator testowany był na następujacych wersjach bibliotek:
Python 3.11.5
pip 23.3.1
ply 3.11
Wykorzystywane są również moduły:
enum, typing, sys, lexer, parser

Pliki:
----------------------
kompilator.py
lexer.py
parser.py
Register.py
Program.py
MemoryManager.py
LabelGenerator.py
Instructions.py
NonTerminals/Command.py
NonTerminals/Condition.py
NonTerminals/Declarations.py
NonTerminals/Identifier.py
NonTerminals/Main.py
NonTerminals/ProcCallParam.py
NonTerminals/Pocedure.py
NonTerminals/ProcHead.py

