import grammar
import adt
import session

'''
 Values defined must include value_list, context parameters
 
 value_list contains a list of tokens (tag, value pairs) parsed 
	according to the productions rule.
	Example Rule
		A : b c d will pass in value list containing parsed tokens(tag, value)
			value_list = [b, c, d] where b c d arer tokens that can be parsed using the contexts eval
					which will map the token to its corresponding user defined eval 
	Context - contains all the available declearations as well as access to the current 
				evaluation map
''' 
def eval_start(value_list, context):
	'''
	START : [BODY], 
			| [FUNC_DEF] 
	'''
	# create a declaration context on start
	return  context.eval(value_list[0], context)




def eval_func_def(value_list, context):
	'''
	FUNC_DEF : [  DEF, ID, L_PAREN, ID, ID_LIST, R_PAREN, BODY, END] 
				0	   1	  2		3	  4         5     6
	'''
	# create a new function object with the id, args, and body
	# and add it to the context. Do not evaluate it yet. Only on func call
	func_id = value_list[1][1]
	args = []
	args.append(value_list[3][1])
	 
	eval_args = context.eval(value_list[4], context)
	for arg in eval_args:
		args.append(arg)

	raw_input('ARGS:'+str( args))
	body = value_list[6]
	func_value = adt.func(func_id, args, body)
	context.set_var(func_id, func_value)
	return context




def eval_func_call(value_list, context):
	'''
	FUNC_CALL : [L_PAREN, ARGS, R_PAREN],
                        [EPSILON]
    '''
	if value_list[0] != None:
		
		value =  context.eval(value_list[1], context) # eval args
		print 'func call:', value
		return value
	return None

def eval_args(value_list, context):
	''''
		ARGS : [EXPR, EXPR_LIST]
			| [ EPSILON]
			
	'''
	if value_list[0] != grammar.EPSILON:
		args = []
		args.append(context.eval(value_list[0], context))
		raw_input(args)
		eval_args = context.eval(value_list[1], context)
		# evaluates if id list to users id_list func in action
		if eval_args != None:
			for arg in eval_args:
				args.append(arg)
			return args
		else: # single arg
			return args[0]
	return None

def eval_id_list(value_list, context):
	'''
		EXPR_LIST : [COMMA, ID, ID_LIST]
				| [EPSILON]
	'''
	value = None
	# accumulate ids into 1D list
	if value_list[0] != None: # not epsilon
		id_list = []
		value = value_list[1][1]
		# if the second id_list is not epsilon then accumulate ids
		print value_list[1]
		id_list.append(value_list[1])
		eval_id = context.eval(value_list[2], context)
		if eval_id != None:
			for eval_id in eval_list:
				id_list.append(eval_id)
			return id_list # returns values as a list
		# else if only single vale return as single item not a list
		return value
	return None


def eval_expr_list(value_list, context):
	'''
		EXPR_LIST : [COMMA, EXPR, EXPR_LIST]
				| [EPSILON]
	'''
	value = None
	# accumulate ids into 1D list
	if value_list[0] != None: # not epsilon
		value = value_list[1][1]
		# if the second id_list is not epsilon then accumulate ids
		eval_values = []
		eval_values.append(value)
		expr_list = context.eval(value_list[2], context)
		if expr_list != None: # if not epsilon
			for expr in expr_list:
				eval_values.append(expr)
			return eval_values # returns values as a list
		# else if only single vale return as single item not a list
	return 	value


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
	STMT:	[LET, ID, ASSIGN, EXPR, SEMICOLON]
			 0    1   2       3       4
	'''		
	value = None
	if len(value_list) == 5: #if four values, eval assignment
		var = value_list[1] 
		assign_tag = value_list[2]
		value = context.eval(value_list[3], context) # eval expr, third value in list
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
	 FACTOR : 	[NUM] 
				| [ID, FUNC_CALL]
				| [L_PAREN, EXPR, R_PAREN]  
	'''
	value = None
	factor = value_list[0] # get fist token from value list
	if factor[0] == grammar.NUM:
		value = float(factor[1])
	elif factor[0] == grammar.ID:
		args = context.eval(value_list[1], context)
		if args:
			raw_input('FUNCTION CALL!')
		else:
			value = context.get_var(factor[1]) # get var from context or its parent contexts
	elif factor[0] == grammar.L_PAREN:
		value = context.eval(value_list[1], context) # eval expr, 2nd value in list
	return value

