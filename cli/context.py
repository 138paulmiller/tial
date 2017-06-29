# defines a variable and function definition scopes
# Variable declarations will be hierarchal where each body generates a context.
class context:
	def __init__(self, evaluation_map):
		self.var_map = {}
		self.evaluation_map = evaluation_map
		self.parent = None


	'''evaluate
    Evaluates the given parse tree's root token. (tag, value). 
    The tag is mapped to a function defined by evaluation map

	''' 
	def eval(self, token, context):
	    value = None
	    if token != None and len(token) > 1:
	        tag = token[0]
	        value_list = token[1]# is a list of value
	        # tags map to functions defined to evaluated each particular tag
	        value = self.evaluation_map[tag](value_list, context)     
	    return value


	def get_var(self, id):
		if id in self.var_map:
			return self.var_map[id]
		elif self.parent != None:
			return self.parent.get_var(id) # find variable in any contexts above the current scope
		return None


	def set_var(self, id, value):
		self.var_map[id] = value


	def print_vars(self):
		for var in self.var_map.keys():
			print var, '=', self.var_map[var]


