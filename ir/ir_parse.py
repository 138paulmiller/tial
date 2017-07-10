import llvmlite.ir as ir
# example production
#	A := B C
# rootA = [symbol, [rootB, rootC]]
# base node 

def start_ir(root, ir_builder):
	'''
	BODY
	'''
	#printf = ir_builder.make_func('printf', ir.IntType(32), (ir.IntType(8).as_pointer(),), var_arg=True)
	start = ir_builder.make_func('start', ir.IntType(32), ())
 	# append a body to it if definition
	block = start.append_basic_block() # append a block to the function
	ir_builder.builder.position_at_end(block) # move builder to end of fuction entry block
	# define printf												# voidptr
	body_ir(root[1][0], ir_builder)
	ir_builder.builder.position_at_end(block) # move builder to end of fuction entry block
	ir_builder.builder.ret(ir.Constant(ir.IntType(32), 0))


def body_ir(root, ir_builder ):
	'''
	STMT SEMICOLON BODY
    | EPSILON 
	'''
	if root[1][0] != None: # not epsilon
		stmt_ir(root[1][0], ir_builder)
		body_ir(root[1][2], ir_builder)


def stmt_ir(root, ir_builder):
	'''
	ASSIGN_STMT
    |  FUNC_DEF	
    | EXPR
	'''
	next_symbol = root[1][0][0] 
	if  next_symbol == 'ASSIGN_STMT':
		assign_stmt_ir(root[1][0], ir_builder)
	elif next_symbol == 'FUNC_DEF':
		func_def_ir(root[1][0], ir_builder)
	elif next_symbol == 'EXPR':
		expr_ir(root[1][0], ir_builder)


def assign_stmt_ir(root,  ir_builder):
	'''
	root[1] = [LET ID ASSIGN EXPR]		
	'''
	id_token = root[1][1] 
	expr=  root[1][3]
	value = expr_ir(expr, ir_builder)
	ir_builder.make_var(id_token[1], value, ir.FloatType())


def  func_call_ir(root, ir_builder):
	'''
	ID FUNC_ARGS
	'''
	id_token = root[1][0]
	args = func_args_ir(root[1][1], ir_builder)
	if args == None: # load variable from
		return ir_builder.get_var(id_token[1])
	else:
		return ir_builder.call_func(id_token[1], args)


	

	
def func_def_ir(root, ir_builder):
	'''
	DEF ID L_PAREN PARAMS R_PAREN  BODY RETURN   EXPR 
	0	1	2		3	   4		5		6		7
	'''
	id_token = root[1][1]
	param_types = []
	params=  params_ir(root[1][3],ir_builder)
	if params != None:
		for param in params:
			param_types.append(ir.FloatType())
	parent_block = ir_builder.builder.block
	func = ir_builder.make_func(id_token[1], ir.FloatType() ,param_types)
	i=0
	for arg in func.args:
		arg.name = params[i]
		ir_builder.set_var(arg.name, arg)
		i+=1	
	block = func.append_basic_block()
	ir_builder.builder.position_at_end(block) # move builder to end of fuction entry block
	body_ir(root[1][5], ir_builder)
	return_expr = expr_ir(root[1][7], ir_builder)
	# pop all vars from builder
	for arg in func.args:
		ir_builder.rm_var(arg.name, arg)
	ir_builder.builder.ret( return_expr)
	ir_builder.builder.position_at_end(parent_block) # go back to parent block before function definition
	return func



def func_args_ir(root, ir_builder):
	'''
	[0] FUNC_ARGS
	[1]L_PAREN  ARGS R_PAREN 
    	| EPSILON 
	'''
	args= None
	if root[1][0] != None:
		args= args_ir(root[1][1], ir_builder)
	return args


def params_ir(root, ir_builder):

	'''
	[0]PARAMS
	[1]ID, ID_LIST
	| EPSILON 
    '''
	params = None
	if root[1][0] != None:
		params = []
		params.append(root[1][0][1])
		id_list = id_list_ir(root[1][1], ir_builder)
		if id_list != None:
			for i in id_list:
				params.append(i) 
	return params 

def id_list_ir(root, ir_builder):

	'''
	[0]ID_LIST
	[1]COMMA, ID, ID_LIST
	| EPSILON 
    '''
	params = None
	if root[1][0] != None:
		params = []
		params.append(root[1][1][1])
		id_list = id_list_ir(root[1][2], ir_builder)
		if id_list != None:
			for i in id_list:
				params.append(i)
			 
	return params 



def args_ir(root, ir_builder):
	'''
	[0]ARGS
	[1]EXPR, EXPR_LIST
	| EPSILON 
    '''
	expr = None
	if root[1][0] != None:
		expr = []
		expr.append( expr_ir(root[1][0], ir_builder))
		expr_list = expr_list_ir(root[1][1], ir_builder)
		if expr_list != None:
			for e in expr_list:
				expr.append(e) 
	return expr


	


def expr_list_ir(root, ir_builder):
	'''
	[0]EXPR
	[1]COMMA EXPR EXPR_LIST
	| EPSILON
	'''
	expr = None
	if root[1][0] != None:
		expr = []
		expr.append(expr_ir(root[1][1], ir_builder))
		expr_list = expr_list_ir(root[1][2], ir_builder)
		if expr_list != None:
			for e in expr_list:
				expr.append(e)
	return expr


def expr_ir(root, ir_builder):
	'''
	TERM EXPR_OP 
	'''
	# always add
	term = term_ir(root[1][0], ir_builder)
	expr_op = expr_op_ir(root[1][1], ir_builder)
	if expr_op != None:
		term = ir_builder.builder.fadd(term , expr_op)
	return term


def expr_op_ir(root, ir_builder):
	'''
	ADD TERM EXPR_OP 
    | SUB TERM EXPR_OP
    | EPSILON 
	'''
	# unary, if sub make negative
	term = None
	if root[1][0] != None:
		if root[1][0][0] == 'SUB':
			term = ir_builder.builder.fmul(term_ir(root[1][1], ir_builder), ir.Constant(ir.FloatType(), -1))
		else:
			term = term_ir(root[1][1], ir_builder)
			expr_op = expr_op_ir(root[1][2], ir_builder)
			if expr_op != None:
				term = ir_builder.builder.fadd(term, expr_op)
	return term


def term_ir(root, ir_builder):
	'''
	FACTOR TERM_OP 
	'''
	factor = factor_ir(root[1][0], ir_builder)
	term_op = term_op_ir(root[1][1], ir_builder)
	if term_op:
		factor = ir_builder.builder.fmul(factor, term_op)
	return factor 


def term_op_ir(root, ir_builder):
	'''
	MUL FACTOR TERM_OP
	| DIV FACTOR TERM_OP 
	| EPSILON 
	'''
	factor = None
	if root[1][0] != None:
		if root[1][0][0] == 'DIV':
			factor = ir_builder.builder.fdiv(ir.Constant(ir.FloatType(), 1), factor(root[1][1]))
		else:
			factor = factor_ir(root[1][1], ir_builder)
			term_op = expr_op_ir(root[1][2], ir_builder)
			if term_op != None:
				factor = ir_builder.builder.fmul(factor, term_op)
	return factor 


def factor_ir(root, ir_builder):
	'''
	NUM
	| SUB NUM
    | STR
    | FUNC_CALL
    | L_PAREN EXPR R_PAREN 
	'''
	factor = None
	next_symbol = root[1][0][0]
	# root[1] is value_list so root[1][0] is first token
	if next_symbol == 'SUB':
		factor = ir.Constant(ir.FloatType(), -1*float(root[1][1][1]))
	elif next_symbol == 'NUM':
		factor = ir.Constant(ir.FloatType(), float(root[1][0][1]))
	elif next_symbol == 'STR':
		# TODO NOT WORKING!!!!!!!!!!!!!!!
		raw_str = (root[1][0][1]+'\00').encode('ascii')
		bytes = bytearray(raw_str)
		arr_type = ir.ArrayType(ir.IntType(8), len(bytes))
		fmt_bytes =  ir.Constant(arr_type, bytes)
		fmt_bytes =  ir_builder.builder.bitcast(fmt_bytes, ir.IntType(8).as_pointer()) 
		raw_input("BYTES:" +   str(fmt_bytes))
		fmt_ptr = ir_builder.builder.alloca(ir.IntType(8).as_pointer())
		factor = ir_builder.builder.store(fmt_bytes, fmt_ptr)
		raw_input("PTR:" +   str(fmt_ptr))
		
	elif next_symbol == 'FUNC_CALL':
		return func_call_ir(root[1][0], ir_builder)	
	elif next_symbol == 'L_PAREN':
		return expr_ir(root[1][1], ir_builder)	
	
	return factor

