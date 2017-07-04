
# types

class object:
	# base object for all types
	def __init__(self, type):
		self.type = type

	def __repr__(self):
		return str(object.type)


class func(object):
	def __init__(self, id, arg_ids, body, return_args):
		object.__init__(self, 'func(')
		self.id = id
		self.arg_ids = arg_ids #variables to add to var map argumen
		self.body = body # new body new context, push new context than add vars
		self.return_args = return_args
		
	def __repr__(self):
		repr_str = 'func('
		i = 0
		if self.arg_ids != None:
			last = len(self.arg_ids)-1
			while i <= last:
				repr_str += str(self.arg_ids[i])
				if i != last:
					repr_str += ', ' 
				i+=1
		repr_str += ')'
		return repr_str


class set(object): # numerical value of expression 
	def __init__(self, values):
		object.__init__(self, 'set')
		self.values = values

	def __repr__(self):
		repr_str = 'set('
		i = 0
		last = len(self.values)-1
		while i <= last:
			repr_str += str(values[i])
			if i != last:
				repr_str += ', ' 
			i+=1
			
		repr_str += ')'
		return repr_str