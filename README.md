## tial
Tial Is Another Language. It is also easy to customize :)
This repository comes with the ll1 package. This package contains is used to construct an LL(1) parser to return a corresponding
parse tree. Each node is a list such that the first element is the symbol tag, and the remaining elements are roots to other 
nodes that correspond to one of the grammar production rules. 

### Building a Custom Language
This project bridges the gap between the grammar definition and evaluation stage.
The modules within this repository generate a custom parser based on the given 
grammar. Parsing the raw source code will return the root of a parse tree.
The parse tree is generated to validate the syntax of the input. 
#### Parse Tree
	* The parsed nodes are lists containing [symbol, values]
  	- Symbol is the string literal of the nonterminal
  	- Values is a list of parse nodes that correspond to the 	
  		nonterminals production rule
  	
### LL1 Grammar File Syntax
	<symbol> = <nonterminal_symbol | terminal_symbol>
	- Single Production:
		 <nonterminal_symbol> := <symbol1> <SPACE> <symbol2> ... <symbolN> $    		
	- Multiple Productions:
		 <nonterminal_symbol> := <symbol1> <SPACE> <symbol2> ... <symbolN> 
		 						| <symbol1> <SPACE> <symbol2> ... <symbolM> 
		 						...
		  						$    		
	- Terminal Definitions
		<terminal_symbol>   := '<regular expression>' $


#### Example Grammar 
The following grammar can parse arithmetic expressions.
Note:
-	Terminals used in the grammar are defined as nonterminals with regular expressions
- 	The NONE keyword prevents lexer from tokenizing any matching input

*ex_grammar.ll1
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


#### Parse tree
	#The ll1 load grammar takes in the file containing grammar, and the start 
	# and epsilon values used in grammar
    ll1_parser = ll1_load_grammar('grammar.ll1','START', 'EPSILON')    

##### Traversing Tree
The parse tree generated follows the production rules for each tag. Each root is a tag, value pairing. The following is an example parse tree generated.
Input: 5*9-4*7;
Parse_Tree:
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

* Note that the value list in (symbol, value_list) corresponds to the possible productions
START   =	['START', 	[BODY]]
BODY    =	['BODY', 	[EXPR, BODY]]
EXPR    =	['EXPR', 	[TERM, EXPR_OP]]
EXPR_OP = 	['EXPR_OP, 	[ADD, TERM, EXPR_OP] 
						| [SUB, TERM, EXPR_OP] 
						| [None]]
TERM    = 	['TERM',  	[FACTOR, TERM_OP]]
TERM_OP =   ['TERM_OP', [MUL, FACTOR, TERM_OP] |
						| [DIV, FACTOR, TERM_OP] |
						| [None]] 
FACTOR  =   ['FACTOR',  [NUM] 
						| [SUB, NUM]
						| [L_PAREN, EXPR, R_PAREN]]

NUM     = ['NUM', <LEXEME>]
ADD     = ['ADD', '+']
SUB     = ['SUB', '-']
MUL     = ['MUL', '*']
DIV     = ['DIV', '/']