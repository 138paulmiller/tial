import terminals as t
import nonterminals as nt

START = 'START' # necessary start symbol
# necessary terminals
EPSILON = 'EPSILON'
EOI = 'EOI'

# Grammar consists of a nonterminal to rule list mapping:
#      Each nonterminal is map to a list of rules where a rule is an inorder list of symbols
rule_map = {
            START    : [ [nt.EXPR]   ],
            
            nt.EXPR     : [ [nt.TERM, nt.EXPR_OP]   ],
            
            nt.EXPR_OP  : [ [t.ADD, nt.TERM, nt.EXPR_OP], 
                            [t.SUB, nt.TERM, nt.EXPR_OP],
                            [EPSILON]],
            
            nt.TERM     : [ [nt.FACTOR, nt.TERM_OP]],
            
            nt.TERM_OP  : [ [t.MUL, nt.FACTOR, nt.TERM_OP], 
                            [t.DIV, nt.FACTOR, nt.TERM_OP], 
                            [EPSILON]],

            nt.FACTOR   : [ [t.NUM],
                            [t.ID],
                            [t.L_PAREN, nt.EXPR, t.R_PAREN]]
            }
