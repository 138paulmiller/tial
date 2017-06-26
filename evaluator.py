import grammar# Symbols, definitions and grammar 

var_map = {}

def eval_start(value_list):
	'''
	START : [STMT] 
			|[EXPR]
	'''
	value =  eval(value_list[0])
	print 'EVAL: ' + str(value)
	print 'VAR MAP:'
	for var in var_map.keys():
		print var, '=', var_map[var]
	return value


def eval_stmt(value_list):
	'''
	STMT:	[ID, ASSIGN, EXPR]
        
	'''
	value = None
	if len(value_list) == 3: #if three values, eval assignment
		var = value_list[0] 
		assign_tag = value_list[1]
		value = eval(value_list[2]) # eval expr, third value in list
		var_map[var[1]] = value
	return value




def eval_expr(value_list):
	'''
	EXPR : [TERM, EXPR_OP]
	''' 
	# evaluate term
	term = eval(value_list[0])
	# evaluate expr_op, is nullable!
	expr_op = eval(value_list[1])
	# by default all terms are added with each other
	# dividing a-b is translated to a+(0-b)	
	# add expression operations
	if expr_op != None:
		term +=  expr_op
	return term

def eval_expr_op(value_list):
	'''
	EXPR_OP :	[ADD, TERM, EXPR_OP]
            	| [SUB, TERM, EXPR_OP] 
            	| [EPSILON]
	'''
	term = None
	if len(value_list) > 0 and value_list[0] != None:
		tag_token = value_list[0] # mul or div token
		term = eval(value_list[1])
		expr_op = eval(value_list[2])
		# subtraction is really adding the negative
		if tag_token[0] == grammar.SUB:
			term = 0 -term 
		# add term to expression operation
		if expr_op != None:
			term += expr_op
	return term


def eval_term(value_list):
	'''
	TERM : [FACTOR, TERM_OP]
	'''
	factor = eval(value_list[0])
	term_op = eval(value_list[1])
	# by default all terms are multiplied with each other
	# dividing a/b is translated to a*(1/b)
	if term_op != None:
		factor *= term_op
	return factor

def eval_term_op(value_list):
	'''
	TERM_OP :	[MUL, FACTOR, TERM_OP]
            	| [DIV, FACTOR, TERM_OP] 
            	| [EPSILON]
	'''
	factor = None
	if len(value_list) > 0 and value_list[0] != None:
		tag = value_list[0] # mul or div
		factor = eval(value_list[1])
		term_op = eval(value_list[2])
		# do not change value for multiplication, by default terms_ops are multipled
		# divisionis really adding the negative
		if tag[0] == grammar.DIV:
			factor = 1/value
		# multiply factor with term operation
		if term_op != None:
			 factor *= term_op
	return factor

def eval_factor(value_list):
	'''
	 FACTOR : 	[NUM, VALUE] 
				| [ID, VALUE]
				| [R_PAREN, EXPR, R_PAREN]  
	'''
	value = None
	factor = value_list[0] # get fist token from value list
	if factor[0] == grammar.NUM:
		value = float(factor[1])
	elif factor[0] == grammar.ID:
		value = var_map[factor[1]]
	elif factor[0] == grammar.L_PAREN:
		value = eval(value_list[1]) # eval expr, 2nd value in list
	return value

# Defines what function will process each tag
eval_map = {
			grammar.START 	: eval_start,
			grammar.STMT 	: eval_stmt,
			grammar.EXPR  	: eval_expr,
			grammar.EXPR_OP : eval_expr_op, 
			grammar.TERM 	: eval_term,
			grammar.TERM_OP : eval_term_op,
			grammar.FACTOR 	: eval_factor
			}
	
'''eval
	Evaluates the given parse tree's root token. (tag, value). 
	The tag is used to redirects the value list to the appropriate function 
	parse_tree - is a recursively generated tag, value_list pairing
	If the tag is a nonterminal, then the value list corresponds to a 
		production rule from the grammer
	If the tag is a terminal, then the value contains the parsed 
		lexeme from input string
''' 
def eval(token):
	value = None
	if token != None:
		tag = token[0]
		value_list = token[1]# is a list of value
		# tags map to functions defined to evaluated each particular tag
		value = eval_map[tag](value_list)		
	return value