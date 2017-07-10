import llvmlite.ir as ir
import llvmlite.binding as bind

class ir_engine():
	def __init__(self):
		bind.initialize()
		bind.initialize_native_target()
		bind.initialize_native_asmprinter()  # yes, even this one
			 # Create a target machine representing the host
		target = bind.Target.from_default_triple()
		self.target_machine = target.create_target_machine()
	    # And an execution engine with an empty backing module
		backing_mod = bind.parse_assembly("")
		self.engine = bind.create_mcjit_compiler(backing_mod, self.target_machine)
    

	def compile(self, module, objfile=None):
		# Create a LLVM module object from the IR
		asm_module = bind.parse_assembly(str(module)) # get llvm ir string to parse 
		print "PARSED ASM:"
		asm_module.verify()
	    # Now add the module and make sure it is ready for execution
		self.engine.add_module(asm_module)
		self.engine.finalize_object() 
		if objfile != None: # write to an obj
			file = open(objfile, "wb")
			obj = self.target_machine.emit_object(asm_module)
			file.write(obj)
			file.close()

		return asm_module

	def get_func_ptr(self, func_id):
		
		    	# Look up the function pointer (a Python int)
		return self.engine.get_function_address(func_id)
		
		

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