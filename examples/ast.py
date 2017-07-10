from llvmlite import ir
# example production
#	A := B C
# rootA = [symbol, [rootB, rootC]]
# base node 
class node():
	def __init__(self, root):
		self.tag = root[0] #symbol tag 
		self.values = root[1] # list of values

	def __str__(self):
		return str(self.tag) + ' ' + str(self.values)		

class start(node):
	'''
	BODY
	'''
	def __init__(self, root):
		node.__init__(self, root)
		self.body = body(self.values[0])
	
	def __str__(self):
		return str(self.body)	


class body(node):
	'''
	STMT SEMICOLON BODY
    | EPSILON 
	'''
	def __init__(self, root):
		node.__init__(self, root)
		self.stmt =  None
		self.body = None
		if len(self.values) == 2:
			self.stmt = stmt(self.values[0])
			self.body = body(self.values[2])
		self.values = None
	def __str__(self):
		if self.stmt != None:
			return str(self.stmt) + '\n' + str(self.body)		
		return ''
	

class stmt(node):
	'''
	root[1]: [ASSIGN_STMT]
    		|  [FUNC_DEF	]
    		| [EXPR]
	'''
	def __init__(self, root):
		node.__init__(self, root)
		self.expr = None
		if self.values[0][0] == 'FUNC_DEF':
			self.expr = func_def(self.values[0])
		else:
			self.expr = assign_stmt(self.values[0])
		self.values = None

	def __str__(self):
		return str(self.expr)

class func_call(node):
	'''
	root[1]:[ID FUNC_ARGS]
	'''
	def __init__(self, root):
		node.__init__(self, root)
		self.id = self.values[0]
		self.func_args = func_args(self.values[1])
		self.values = None

	def __str__(self):
		return  str(self.id) + '(' + str(self.func_args)+')'	
	

class func_def(node):
	'''
	root[1]: [DEF ID L_PAREN ARGS R_PAREN  BODY RETURN ARGS 
		0	1	2		3	4		5		6		7
	'''
	
	def __init__(self, root):
		node.__init__(self, root)
		self.id = self.values[1]
		self.parameter_args = args(self.values[3]) # must be identifiers!
		self.body = body(self.values[5])
		self.return_args = args(self.values[7])
		self.values = None

	def __str__(self):
			return 'FUNC: ' + str(self.id) + '(' + str(self.parameter_args)+ ')\n' + str(self.body) + '\n RETURN: ' + str(self.return_args)	
	
class func_args(node):
	'''
	L_PAREN  ARGS R_PAREN 
    | EPSILON 
	'''
	def __init__(self, root):
		node.__init__(self, root)
		self.args = None
		if len(self.values) == 3:
			self.args = args(self.values[1])
		self.values = None
	
	def __str__(self):
		if self.args != None:
			return str(self.args)
		return ''


class args(node):
	'''
	EXPR, EXPR_LIST
    | EPSILON 
    '''
	def __init__(self, root):
		node.__init__(self, root)
		self.expr = None
		self.expr_list = None
		if len(self.values) == 2:
			self.expr = expr(self.values[0])
			self.expr_list = expr_list(self.values[1])
		self.values = None

	def __str__(self):
		if self.expr != None:
			return str(self.expr) + str(self.expr_list)
		return ''

class assign_stmt(node):
	'''
	ID ASSIGN EXPR SEMICOLON 		
	'''
	def __init__(self, root):
		node.__init__(self, root)
		self.id= self.values[0]
		self.expr = expr(self.values[2])
		self.values = None

	def __str__(self):
		return str(self.id) + ' = ' + str(self.expr)

class expr_list(node):
	'''
	COMMA EXPR EXPR_LIST
	| EPSILON
	'''
	def __init__(self, root):
		node.__init__(self, root)
		self.expr = None
		self.expr_list = None
		if len(self.values) == 3:
			self.expr = expr(self.values[1])
			self.expr_list = expr_list(self.values[2])
		self.values = None

	def __str__(self):
		if self.expr != None:		
			return ', ' + str(self.expr) + str(self.expr_list)
		return ''



class expr(node):
	'''
	TERM EXPR_OP 
	'''
	def __init__(self, root):
		node.__init__(self, root)
		self.term =	term(self.values[0])
		self.expr_op = expr_op(self.values[1])
		self.values = None
	
	def __str__(self):
		return str(self.term) + ' ' + str(self.expr_op)


class expr_op(node):
	'''
	ADD TERM EXPR_OP 
    | SUB TERM EXPR_OP
    | EPSILON 
	'''
	def __init__(self, root):
		node.__init__(self, root)
		self.op =None
		self.term =	None
		self.expr_op= None
		if len(self.values) == 3:
			self.op = self.values[0]
			self.term =	term(self.values[1])
			self.expr_op = expr_op(self.values[2])
		self.values = None

	def __str__(self):
		if self.op != None:
			return str(self.op) + ' ' + str(self.term) + ' ' + str(self.expr_op)
		return ''

class term(node):
	'''
	FACTOR TERM_OP 
	'''
	def __init__(self, root):
		node.__init__(self, root)
		self.factor =	factor(self.values[0])
		self.term_op = term_op(self.values[1])
		self.values = None
	
	def __str__(self):
		return str(self.factor) + ' ' + str(self.term_op)



class term_op(node):
	'''
	MUL FACTOR TERM_OP
    | DIV FACTOR TERM_OP 
    | EPSILON 
	'''
	def __init__(self, root):
		node.__init__(self, root)
		self.op = None
		self.factor =None
		self.term_op =None
		if len(self.values) == 3:
			self.op = self.values[0]
			self.factor =	factor(self.values[1])
			self.term_op = term_op(self.values[2])
		self.values = None

	def __str__(self):
		if self.op != None:
			return str(self.op) + ' ' + str(self.factor) + ' ' + str(self.term_op)
		return ''


class factor(node):
	'''
	NUM
    | FUNC_CALL
    | L_PAREN EXPR R_PAREN 
	'''
	def __init__(self, root):
		node.__init__(self, root)
		self.value = self.values[0]
		if self.value[0] == 'NUM':
			self.value = self.value 
		if self.value[0] == 'FUNC_CALL':
			self.value = func_call(self.values[0])
		elif self.value[0] == 'L_PAREN':
			self.value = expr(self.values[1])
		self.values = None

	def __str__(self):
		return str(self.value)



