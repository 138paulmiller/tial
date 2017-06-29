from grammar import *


START = 'START' # necessary symbol tags
EPSILON = 'EPSILON'

# nonterminal symbol tags. Symbols taht are mapped to production rules in grammer
BODY = 'BODY'
STMT   = 'STMT' # single execution line
EXPR = 'EXPR' # expressions grouped with adders
EXPR_OP = 'EXPR_OP'# operation with expression
TERM = 'TERM'       #expressions grouped by multipliers
TERM_OP = 'TERM_OP' # operation with term
FACTOR = 'FACTOR' # basic unit of expression

#terminal symbol tags
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
SEMICOLON = 'SEMICOLON'

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
      (r'\*', MUL),
      (r'/', DIV),
      (r'if', IF),
      (r'else', ELSE),
      (r'end', END),
      (r'while', WHILE),
      (r';', SEMICOLON),
      (r'[a-zA-Z_][a-zA-Z0-9_]*', ID),
      (r'\"[a-zA-Z0-9_ ]+\"', STR),
      (r'[ \t\n]+', None), #whitepsace
      (r'#\w+[^\n]+', None)] #comments, # everything but newline



# Grammar consists of a nonterminal to rule list mapping:
#      Each nonterminal is map to a list of rules where a rule is an inorder list of symbols
rule_map = {
            START    : [[BODY]],

            BODY     : [[STMT, BODY],
                        [EPSILON]],
            STMT     : [[ID, ASSIGN, EXPR, SEMICOLON]],
          
            EXPR     : [[TERM, EXPR_OP]],
            
            EXPR_OP  : [ [ADD, TERM, EXPR_OP], 
                        [SUB, TERM, EXPR_OP],
                        [EPSILON]],
            
            TERM     : [[FACTOR, TERM_OP]],
            
            TERM_OP  : [[MUL, FACTOR, TERM_OP], 
                        [DIV, FACTOR, TERM_OP], 
                        [EPSILON]],

            FACTOR   : [[NUM],
                        [ID],
                        [L_PAREN, EXPR, R_PAREN]]
            }
