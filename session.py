# defines a variable and function definition scopes
# Variable declarations will be hierarchal where each body generates a context.
class context:
	def __init__(self, evaluation_map, parent=None):
		self.var_map = {}
		self.evaluation_map = evaluation_map
		self.parent = parent


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


	def get_var(self, var_id):
		if var_id in self.var_map:
			return self.var_map[var_id]
		elif self.parent != None:
			return self.parent.get_var(var_id) # find variable in any contexts above the current scope
		return None


	def set_var(self, var_id, value):
		self.var_map[var_id] = value


	def print_vars(self):
		for var in self.var_map.keys():
			print var, '\t:=', self.var_map[var]
		

