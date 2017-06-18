 


# token terminal tags
NUMBER = 'NUMBER'
AND = 'AND'
OR = 'OR'
NOT = 'NOT'
EQUAL  = 'EQUAL'
LESS = 'LESS'
LESS_EQUAL = 'LESS_EQUAL'
GREATER = 'GREATER'
GREATER_EQUAL = 'GREATER_EQUAL'
MINUS = 'MINUS'
ASSIGN = 'ASSIGN'
MULTIPLY = 'MULTIPLY'
DIVIDE = 'DIVIDE '
PLUS = 'PLUS'
LEFT_PAREN = 'LEFT_PAREN'
RIGHT_PAREN = 'RIGHT_PAREN'
IF = 'IF'
ELSE = 'ELSE'
END = 'END'
WHILE = 'WHILE'
SEMICOLON = 'SEMICOLON'
IDENTIFIER = 'IDENTIFIER'
STRING = 'STRING'
TERMINATOR = 'SEMICOLON'


# definitions - corresponds each token terminal with a regex match
#                       (expression, terminal tag)
definitions = [
            (r'-?[0-9]*\.?[0-9]+', NUMBER),
            (r'and', AND),
            (r'or', OR),
            (r'not', NOT),
            (r'==', EQUAL),
            (r'<', LESS),
            (r'<=', LESS_EQUAL),
            (r'>', GREATER),
            (r'>=', GREATER_EQUAL),
            (r'\+', PLUS),
            (r'\(', LEFT_PAREN),
            (r'\)', RIGHT_PAREN),
            (r'-', MINUS),
            (r'=', ASSIGN),
            (r'\*',MULTIPLY),
            (r'/', DIVIDE),
            (r'if', IF),
            (r'else', ELSE),
            (r'end', END),
            (r'while', WHILE),
            (r';', SEMICOLON),
            (r'[a-zA-Z_][a-zA-Z0-9_]*', IDENTIFIER),
            (r'\"[a-zA-Z0-9_ ]+\"', STRING),
            (r'[ \t\n]+', None), #whitepsace
            (r'#\w+[^\n]+', None)] #comments, # everything but newline
