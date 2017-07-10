import llvmlite.binding as bind

class ir_binder():
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
		
		
