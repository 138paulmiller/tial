import grammar
from cli import context


# Symbols, definitions and grammar 
# value list contains a list of tokens (tag, value pairs). 
# Evalutor handles token values
def eval_start(value_list, context):
	'''
	START : [STMT] 
	'''
	# create a declaration context on start
	value =  context.eval(value_list[0], context)
	print 'EVAL: ' + str(value)
	return value


def eval_stmt(value_list, context):
	'''
	STMT:	[ID, ASSIGN, EXPR, SEMICOLON]
	'''
	value = None
	if len(value_list) == 4: #if three values, eval assignment
		var = value_list[0] 
		assign_tag = value_list[1]
		value = context.eval(value_list[2], context) # eval expr, third value in list
		context.set_var(var[1], value) 
	return value



def eval_expr(value_list, context):
	'''
	EXPR : [TERM, EXPR_OP]
	''' 
	# evaluate term
	term = context.eval(value_list[0], context)
	# evaluate expr_op, is nullable!
	expr_op = context.eval(value_list[1], context)
	# by default all terms are added with each other
	# dividing a-b is translated to a+(0-b)	
	# add expression operations
	if expr_op != None:
		term +=  expr_op
	return term

def eval_expr_op(value_list, context):
	'''
	EXPR_OP :	[ADD, TERM, EXPR_OP]
            	| [SUB, TERM, EXPR_OP] 
            	| [EPSILON]
	'''
	term = None
	if len(value_list) > 0 and value_list[0] != None:
		tag_token = value_list[0] # mul or div token
		term = context.eval(value_list[1], context)
		expr_op = context.eval(value_list[2], context)
		# subtraction is really adding the negative
		if tag_token[0] == grammar.SUB:
			term = 0 -term 
		# add term to expression operation
		if expr_op != None:
			term += expr_op
	return term


def eval_term(value_list, context):
	'''
	TERM : [FACTOR, TERM_OP]
	'''
	factor = context.eval(value_list[0], context)
	term_op = context.eval(value_list[1], context)
	# by default all terms are multiplied with each other
	# dividing a/b is translated to a*(1/b)
	if term_op != None:
		factor *= term_op
	return factor

def eval_term_op(value_list, context):
	'''
	TERM_OP :	[MUL, FACTOR, TERM_OP]
            	| [DIV, FACTOR, TERM_OP] 
            	| [EPSILON]
	'''
	factor = None
	if len(value_list) > 0 and value_list[0] != None:
		tag = value_list[0] # mul or div
		factor = context.eval(value_list[1], context)
		term_op = context.eval(value_list[2], context)
		# do not change value for multiplication, by default terms_ops are multipled
		# divisionis really adding the negative
		if tag[0] == grammar.DIV:
			factor = 1/value
		# multiply factor with term operation
		if term_op != None:
			 factor *= term_op
	return factor

def eval_factor(value_list, context):
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
		value = context.get_var(factor[1]) # get var from context or its parent contexts
	elif factor[0] == grammar.L_PAREN:
		value = context.eval(value_list[1], context) # eval expr, 2nd value in list
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
