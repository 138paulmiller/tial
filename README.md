# tial
Tial Is Another Language 


### LL(1) Grammar Parser
	The ll1 package includes a generated LL(1) parser. Construction of this
	parser requires grammar defintions and production rules.
	The grammar consists of nonterminals that are mapped to an ordered list of terminals and noterminals.
	The ordered list defines the production rule for the corresponding nonterminal.
	Terminals are defined using regular expressions. 
	
## Example Terminal Definitions
	definitions = [
      (r'-?[0-9]*\.?[0-9]+', NUM),
      (r'\+', ADD),
      (r'\(', L_PAREN),
      (r'\)', R_PAREN),
      (r'-', SUB),
      (r'=', ASSIGN),
      (r'[a-zA-Z_][a-zA-Z0-9_]*', ID),
      #	use none to ignore these matches in input
      (r'[ \t\n]+', None), 		# whitespace
      (r'#\w+[^\n]+', None) 	# comment
      ] 	


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
