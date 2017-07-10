import llvmlite.ir as ir

# Class used to simplify building ir instructions
class ir_builder():
	def __init__(self, parent=None):
		self.var_map = {} # 
		self.func_map = {} # 
		module = ir.Module()
		self.module = ir.Module()
		self.builder = ir.IRBuilder() # on start create new builder


	def get_func(self, name):
		if name in self.func_map:
			return self.func_map[name]
		else:
			print 'IR_GEN ERROR: Function: ', name, ' not declared or defined!'
		return None

	def get_var(self, name):
		if name in self.var_map:
			return self.var_map[name]
		else:
			print 'IR_GEN ERROR: Variable: ', name, ' not declared or defined!'
		return None

	def rm_var(self, name, value):
		self.var_map.pop(name) 



	def set_var(self, name, value):
		self.var_map[name] =  value


	def call_func(self, name, args):
		if name in self.func_map:
			func = self.func_map[name]
			return self.builder.call(func, args)
		else:
			print 'IR_GEN ERROR: Function: ', name, ' not declared!'
		return None
		


	def make_func(self, name, return_type, param_types, var_arg=False):
		if name in self.func_map:
			print 'IR_GEN ERROR: Function: ', name, ' is already defined!'
			return None
		else:
			func_type = ir.FunctionType(return_type, param_types,  var_arg=var_arg) # define paramter and return type
			func = ir.Function(self.module, func_type, name=name) # get the function in the given module
			self.func_map[name] = func
			return func


	def make_var(self, name, value, type):
		var_ptr = self.builder.alloca(type, name=name)
		self.builder.store(value, var_ptr)
		self.var_map[name] =  value