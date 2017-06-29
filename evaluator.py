import grammar
from cli import context

'''
 Values defined must include value_list, context parameters
 
 value_list contains a list of tokens (tag, value pairs) parsed 
	according to the productions rule.
	Example Rule
		A : b c d will pass in value list containing parsed tokens(tag, value)
			value_list = [b, c, d] where b c d can be parsed using the contexts eval
					which will map the token to its corresponding user defined eval 
	Context - contains all the available declearations as well as access to the current 
				evaluation map
''' 
def eval_start(value_list, context):
	'''
	START : [BODY] 
	'''
	# create a declaration context on start
	value =  context.eval(value_list[0], context)
	print 'START EVAL BODY CONTEXT: '
	value.print_vars()


def eval_body(value_list, context):
	'''
	BODY : [BODY, STMT]
		 | [EPSILON] 
	'''
	# create a declaration context on start
	stmt_value = None
	body_value = None;
	if value_list != None:
		if value_list[0] != None: #  not EPSILON: 
			# eval body 
			body_value = context.eval(value_list[0], context)
			# evaluate stmt
			stmt_value =context.eval(value_list[1], context)
	
	
	return context



def eval_stmt(value_list, context):
	'''
	STMT:	[ID, ASSIGN, EXPR, SEMICOLON]
	'''
	value = None
	if len(value_list) == 4: #if four values, eval assignment
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
		# if value_list[0] = (FACTOR, value) then eval will return value 
		factor = context.eval(value_list[1], context)
		term_op = context.eval(value_list[2], context)
		# do not change value for multiplication, by default terms_ops are multipled
		# divisionis really adding the negative
		if tag[0] == grammar.DIV:
			factor = 1/factor
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

