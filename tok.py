 


# token terminal tags
NUM = 'NUM'
AND = 'AND'
OR = 'OR'
NOT = 'NOT'
EQUAL  = 'EQUAL'
LESS = 'LESS'
L_EQUAL = 'L_EQUAL'
GREATER = 'GREATER'
G_EQUAL = 'G_EQUAL'
SUB = 'SUB'
ASSIGN = 'ASSIGN'
MUL = 'MUL'
DIV = 'DIV '
ADD = 'ADD'
L_PAREN = 'L_PAREN'
R_PAREN = 'R_PAREN'
IF = 'IF'
ELSE = 'ELSE'
END = 'END'
WHILE = 'WHILE'
ID = 'ID'
STR = 'STR'
TERMINATOR = 'TERMINATOR'


# definitions - corresponds each token terminal with a regex match
#                       (expression, terminal tag)
definitions = [
            (r'-?[0-9]*\.?[0-9]+', NUM),
            (r'and', AND),
            (r'or', OR),
            (r'not', NOT),
            (r'==', EQUAL),
            (r'<', LESS),
            (r'<=', L_EQUAL),
            (r'>', GREATER),
            (r'>=', G_EQUAL),
            (r'\+', ADD),
            (r'\(', L_PAREN),
            (r'\)', R_PAREN),
            (r'-', SUB),
            (r'=', ASSIGN),
            (r'\*',MUL),
            (r'/', DIV),
            (r'if', IF),
            (r'else', ELSE),
            (r'end', END),
            (r'while', WHILE),
            (r';', TERMINATOR),
            (r'[a-zA-Z_][a-zA-Z0-9_]*', ID),
            (r'\"[a-zA-Z0-9_ ]+\"', STR),
            (r'[ \t\n]+', None), #whitepsace
            (r'#\w+[^\n]+', None)] #comments, # everything but newline
