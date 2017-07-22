## tial
Tial Is Another Language. It is also an LL(1) parser generator.
This repository comes with the ll1 package. 
This package is used to construct an LL(1) parser from a grammar
and will generate corresponding parse tree from input source. 

#### Building a Custom Language
This project bridges the gap between the grammar definition and evaluation stage.
The modules within this repository generate a custom parser based on the given 
grammar. Parsing the raw source code will return the root of a parse tree.

#### Parse Node
 Each node is list comprised of a [symbol, value_list] pairing
- Symbol 	: a string literal representation of symbol
- Value_list 	: a list of parse nodes that are in order of production rule
		If the node is a nonterminal, the node contains [symbol, lexeme]
#### Parse Tree
The parse tree is the root node where the symbol is equal to the start symbol in the grammar. 
To traverse the parse tree, recursively descent down the value_lists of each node. The nodes in the value_list
will be in order to the given production rule if the node is a nonterminal.

#### Usage
	'''
	The ll1 load grammar takes in the file containing grammar
	and the start and epsilon values used in grammar
	'''
	ll1_parser = ll1_load_grammar('ex_grammar.ll1','START', 'EPSILON')   
	parse_root =  ll1_parser.parse(source_code)    
	ll1_parser.print_tree(parse_root)
 
#### LL1 Grammar File Syntax
The parse generated the parser from an ll1 grammar file.
- Note that symbol can either be a nonterminal or terminal symbol

###### Single Production:
	<nonterminal_symbol> 	:= <symbol1> <SPACE> <symbol2> ... <symbolN> $    		

###### Multiple Productions:
	 <nonterminal_symbol> 	:= <symbol1> <SPACE> <symbol2> ... <symbolN> 
				| <symbol1> <SPACE> <symbol2> ... <symbolM> 
				| ... $
###### Terminal Definitions
	<terminal_symbol>   	:= '<regular expression>' $
	If terminal_symbol is None, then the parser will ignore any tokens with the given regular expression
	

##### Example Grammar 
The following grammar can parse arithmetic expressions.
Found in File: ex_grammar.ll1

	START 	:= BODY 
		$

	BODY 	:= EXPR BODY
	        | EPSILON
	        $

	EXPR 	:= TERM EXPR_OP SEMICOLON   
	        $

	EXPR_OP := ADD TERM EXPR_OP 
		| SUB TERM EXPR_OP
		| EPSILON
		$

	TERM 	:=  FACTOR TERM_OP
		$

	TERM_OP :=  MUL FACTOR TERM_OP  
		| DIV FACTOR TERM_OP  
		| EPSILON
		$

	FACTOR	:= NUM
		| SUB NUM
		| L_PAREN EXPR R_PAREN
		$

	L_PAREN   := '\('              $
	R_PAREN   := '\)'              $
	MUL       := '\*'              $
	DIV       := '/'               $
	ADD       := '\+'              $
	SUB       := '\-'              $
	SEMICOLON := ';'               $
	NUM 	  := '[0-9]*\.?[0-9]+' $
	NONE      := '[ \t\n]+'        $


##### Input: 	
	5*9-4*7;
#####  Generated Tree
	   START:
	      BODY:
	         EXPR:
	            TERM:
	               FACTOR:
	                  NUM 5
	               TERM_OP:
	                  MUL *
	                  FACTOR:
	                     NUM 9
	                  TERM_OP:None
	            EXPR_OP:
	               SUB -
	               TERM:
	                  FACTOR:
	                     NUM 4
	                  TERM_OP:
	                     MUL *
	                     FACTOR:
	                        NUM 7
	                     TERM_OP:None
	               EXPR_OP:None
	            SEMICOLON ;
	         BODY:None

##### Parse Tree Traversal
	ROOT    =	['START', 	[BODY]]
	BODY    =	['BODY', 	[EXPR, BODY]]
	EXPR    =	['EXPR', 	[TERM, EXPR_OP]]
	EXPR_OP = 	['EXPR_OP, 	[ADD, TERM, EXPR_OP] 
					| [SUB, TERM, EXPR_OP] 
					| [None]]
	TERM    = 	['TERM',  	[FACTOR, TERM_OP]]
	TERM_OP =   	['TERM_OP', 	[MUL, FACTOR, TERM_OP] 
					| [DIV, FACTOR, TERM_OP] 
					| [None]] 
	FACTOR  =   	['FACTOR',  	[NUM] 
					| [SUB, NUM]
					| [L_PAREN, EXPR, R_PAREN]]
	NUM     = 	['NUM', <lexeme>]
	ADD     = 	['ADD', '+']
	SUB     = 	['SUB', '-']
	MUL     = 	['MUL', '*']
	DIV     = 	['DIV', '/']
