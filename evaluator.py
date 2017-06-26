import grammar# Symbols, definitions and grammar 

variable_map = {} # contains a mapping of all current data values in current context


def eval_start(value_list):
	value =  eval(value_list[0])
	print ('\nEVALUATED:\n' + str(value)+ '...')
	return value


def eval_expr(value_list):
	term = value_list[0]
	expr_op = value_list[1]
	# evaluate term
	value = eval(term)
	# evaluate expr_op, is nullable!
	expr_op = eval(expr_op)
	# by default all terms are added with each other
	# dividing a-b is translated to a+(0-b)	
	if expr_op != None:
		value +=  expr_op
	return value

def eval_expr_op(value_list):
	value = None
	if len(value_list) > 0 and value_list[0] != None:
		tag = value_list[0] # mul or div
		term = value_list[1]
		expr_op = value_list[2]
		value = eval(term)
		expr_op = eval(expr_op)
		# subtraction is really adding the negative
		if tag[0] == grammar.SUB:
			value = 0 - value 
		if expr_op != None:
			value += expr_op
	return value


def eval_term(value_list):
	factor= value_list[0]
	term_op = value_list[1]
	value = eval(factor)
	term_op = eval(term_op)
	# by default all terms are multiplied with each other
	# dividing a/b is translated to a*(1/b)
	if term_op != None:
		value *= term_op
	return value

def eval_term_op(value_list):
	value = None
	if len(value_list) > 0 and value_list[0] != None:
		tag = value_list[0] # mul or div
		factor = value_list[1]
		term_op = value_list[2]
		value = eval(factor)
		term_op = eval(term_op)
		# do not change value for multiplication, by default terms_ops are multipled
		# divisionis really adding the negative
		if tag[0] == grammar.DIV:
			value = 1/value
		if term_op != None:
			 value *= term_op
	return value

def eval_factor(value_list):
	# factor : [num, value], [id, value],[lparen, expr, rparen]  
	factor = value_list[0]
	value = None
	if factor[0] == grammar.NUM:
		value = float(factor[1])
	elif factor[0] == grammar.L_PAREN:
		value = eval(value_list[1]) # eval expr, 2nd value in list
	return value

# Define callbacks for each individual nonterminal
eval_map = {
	grammar.START : eval_start,
	grammar.EXPR : eval_expr,
	grammar.EXPR_OP : eval_expr_op,
	grammar.TERM : eval_term,
	grammar.TERM_OP: eval_term_op,
	grammar.FACTOR : eval_factor
}
'''eval
	Evaluates the given parse tree root. 
	parse_tree - is a recursively generated tag, value_list pairing
	If the tag is a nonterminal, then the value list corresponds to a 
		production rule from the grammer
	If the tag is a terminal, then the value contains the parsed 
		lexeme from input string
''' 
def eval(root):
	value = None
	if root != None:
		tag = root[0]
		value_list = root[1]# is a list of value
		value = eval_map[tag](value_list)		
	return value