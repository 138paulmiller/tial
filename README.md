## tial
Tial Is Another Language. It is also easy to customize :)
This repository comes with the ll1 package. This package contains is used to construct an LL(1) parser to return a corresponding
parse tree. Each node is a list such that the first element is the symbol tag, and the remaining elements are roots to other 
nodes that correspond to one of the grammar production rules. 

### Building a Custom Language
This project bridges the gap between the grammar definition and evaluation stage.
The modules within this repository allow users to define an LL(1) parsable grammar and define
the functions to evaluate each rule.
To achieve this functionality, the user must provide the following components:
* Token Definitions
	- A list of regular expressions each paired with a symbol. 
	The symbols can be used within the grammar and define acceptable the string literals of the language.
* Grammar
	- The grammar is defined as a rule map such that each symbol has a list of corresponding rules.
	with each rule as an inorder list of symbols.
 * Evaluation Map
 	- Each symbol that has a rule must also has an evaluator. 
	The evaluator is a function that accepts a value list and a context 
	and is used to do define how to evaluate each production rule.


### Example Language
The following example can parse arithmetic expressions.
Some caveats to this grammar can be seen in the following example.
	1 + (-3);

#### Example Token Definitions
	definitions = [
      	(r'-?[0-9]*\.?[0-9]+', 'NUM'),
      	(r'\(', 'L_PAREN'),
      	(r'\)', 'R_PAREN'),
      	(r'\*', 'MUL'),
      	(r'/', 'DIV'),
      	(r'\+', 'ADD'),
      	(r'-', 'SUB'),
	(r';', 'SEMICOLON'),
      	#	use none to ignore these matches in input
      	(r'[ \t\n]+', None), 		# whitespace
      	(r'#\w+[^\n]+', None) 	# comment
      	] 	

#### Example Grammar
	grammar = {
	    'START'    : [['BODY']],

            'BODY'     : [['EXPR', 'BODY'],
                        [EPSILON]],
          
            'EXPR'     : [['TERM', 'EXPR_OP', 'SEMICOLON']],
            
            'EXPR_OP'  : [ ['ADD', 'TERM', 'EXPR_OP'], 
                        ['SUB', 'TERM', 'EXPR_OP'],
                        ['EPSILON']],
            
            'TERM'     : [['FACTOR', 'TERM_OP']],
            
            'TERM_OP'  : [['MUL', 'FACTOR', 'TERM_OP'], 
                        ['DIV', 'FACTOR', 'TERM_OP'], 
                        ['EPSILON']],

            'FACTOR'   : [['NUM'],
                        ['L_PAREN', 'EXPR', 'R_PAREN']]
            }
#### Example Evaulation Map
	evaluation_map = {
		    'START'   : eval_start,
		    'BODY'    : eval_body,
		    'STMT'    : eval_stmt,
		    'EXPR'    : eval_expr,
		    'EXPR_OP' : eval_expr_op, 
		    'TERM'    : eval_term,
		    'TERM_OP' : eval_term_op,
		    'FACTOR'  : eval_factor
		    }
		    
#### Constructing the Parser and Evaluator
	# Where START, EPSILON are symbols used to identify start and epsilon symbols used by grammer
	ll1_parser = ll1_init(grammar, 'START', 'EPSILON', definitions)
    	# creates a root context where evalautions will be contained
	root_context = session.context(evaluation_map)
	
#### Evaluating Source Code
	# parse the string representation of source code
	root =  parser.parse(code) # gets root of ast
        parser.print_tree(root)
	# evaluate the ast with repsect to root_context 
	# the value returned is the context returned evaluation context
    	context =root_context.eval(root, root_context)
	
#### Defining Evaluator
For each nonterminal there should be a corresponding evaluator
the evaluator for 'START' : eval_start should accept a value_list and context  
	value_list - contains a list of ast roots for each rule
	context  - holds accesable variables 
NOTE: if value_list[0] == EPSILON then value_list[0] == None 
If a token within the value_list is a nonterminal is value can be evaluated by the context,
else the token is the pair (symbol, value) .
	symbol -  corresponds to the regex identifier passed into token definition
	value - is the matched string literal from source code

##### Example Evaluator for Grammar
	def eval_start(value_list, context):
		'''
		START : [ BODY ]
		'''
		return context.eval(value_list[0], context) # return evaluated body
		'''
	def eval_body(value_list, context):
		'''
		BODY : [EXPR, BODY] 
			|[EPSILON] 
		'''
		# create a declaration context on start
		stmt_value = None 
		body_value = None;
		if value_list != None:
			if value_list[0] != None: #  not EPSILON: 
				# eval expr
				body_value = context.eval(value_list[0], context)
				# evaluate body
				stmt_value =context.eval(value_list[1], context)
		return context

	def eval_expr(value_list, context):
		'''
		EXPR : [TERM, EXPR_OP, SEMICOLON]
		''' 
		# evaluate term
		term = context.eval(value_list[0], context)
		# evaluate expr_op, is nullable!
		expr_op = context.eval(value_list[1], context)
		if term != None:	
			term +=  expr_op
		return term


	def eval_expr_op(value_list, context):
		'''
		EXPR_OP :[ADD, TERM, EXPR_OP]
			| [SUB, TERM, EXPR_OP] 
			| [EPSILON]
		'''
		term = None
		if len(value_list) > 0 and value_list[0] != None:
			tag_token = value_list[0] # mul or div token
			term = context.eval(value_list[1], context)
			expr_op = context.eval(value_list[2], context)
			if tag_token[0] == 'SUB':
					term = 0-term 
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
		#if numerical
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
			if factor != None:
				if tag[0] == 'DIV':
					factor = 1/factor
				# multiply factor with term operation
				if term_op != None:
					 factor *= term_op
		return factor

	def eval_factor(value_list, context):
		'''
		 FACTOR : [NUM] 
			| [ID, FUNC_CALL]
			| [L_PAREN, EXPR, R_PAREN]  
		'''
		value = None
		factor = value_list[0] # get first token from value list
		if factor[0] == 'NUM':
			value = float(factor[1])
		elif factor[0] == 'L_PAREN':
			value = context.eval(value_list[1], context) # eval expr, 2nd value in list

		return value

