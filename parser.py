# Paul Miller 2016
# All rights reserved

import lexer
import ast
import tok

# LL1 Parser 
# - Uses a grammer map such that each symbol maps to a list of production rules.
#   Each rule is an in order list of terminal and nonterminals.
#   Terminals are node that do not exist as a key in the grammer map. 
#   Each production 
# 

# Symbols
START = 'START'
STATMENT   = 'STATEMENT'
EXPRESSION = 'EXPRESSION' # expressions grouped with adders
EXPRESSION_OP = 'EXPRESSION_OP'# operation with expression
TERM = 'TERM'       #expressions grouped by multipliers
TERM_OP = 'TERM_OP' # operation with term
FACTOR = 'FACTOR' # basic unit of expression
EPSILON = 'EPSILON'
EOI = 'EOI' # end of input

# grammer uses the token tags as terminals and parse tree nodes as nonterminals or symbols
#   Grammer is a map of symbols. Each symbols matches to a precedence ordered rule list where 
#   each rule is a list of terminals and nonterminals that define symbol 
grammer = { START : [[STATMENT, EOI]],
            STATMENT :     [[EXPRESSION, tok.TERMINATOR]],     # statement rule 1

            EXPRESSION : [[TERM, EXPRESSION_OP]],
            EXPRESSION_OP : [[tok.PLUS, TERM, EXPRESSION_OP], 
                            [tok.MINUS, TERM, EXPRESSION_OP],
                            [EPSILON]],

            TERM : [[FACTOR, TERM_OP]],
            TERM_OP : [[tok.MULTIPLY, FACTOR, TERM_OP], 
                        [tok.DIVIDE, FACTOR, TERM_OP], 
                        [EPSILON]],

            FACTOR:   [[tok.NUMBER], # expression rule 1
                        [tok.IDENTIFIER],
                        [tok.LEFT_PAREN, EXPRESSION, tok.RIGHT_PAREN]]
        }

# returns list of possible symbols that are the first symbol in the rule
def first_set(symbol):
    firsts = []
    if symbol in grammer: ## if symbols rules exits
        rule_set = grammer[symbol]
        # get the first of the first possible rule, avoid first of self 
        for rule in rule_set: # check each rule. Rule is list of inorder symbols
            # if rule has symbols and first symbol is not the same as root.
            if len(rule) > 0 and (rule[0] != symbol): 
                firsts  = firsts + first_set(rule[0]) # concat first sets
    else: # no rules
        # the symbol is a terminal, so return it as is
        firsts.append(symbol)
    return firsts


#returns list of possible following symbols that can follow the given symbol
def follow_set(symbol):
    follows  = []
    if  symbol not in grammer: #terminal
        return [symbol]
    # search for symbol in every rule of every other symbol
    for rule_symbol in grammer.keys():  # each symbol contains a rule set,  
        for rule in grammer[rule_symbol]:  # iterate through each rule in set for each symbol
            i = 0
            while i <  len(rule):     # check every symbol in rule
                if rule[i] == symbol:# if rule symbol is equal to symbol and not epsilon
                    if i+1 < len(rule): # try to get the following symbol in the rule
                        if  rule[i+1] not in grammer and rule[i+1] not in follows: # if terminal
                            follows.append(rule[i+1]) # append rule symbol if terminal
                        else: # if nonterminal, union nonterminal's firsts into follow
                            for first in first_set(rule[i+1]):
                                if first is not EPSILON:
                                    if first not in follows: # cannot exist in follows and must not be epsilon
                                        follows.append(first) # get the first terminal of symbol
                                else: # if epsilon is a first, append parent symbol's follow set
                                    follows = set(follows).union(follow_set(rule_symbol))
                    elif rule_symbol is not symbol: # if at the end of rule, append the follow set of the parent rule symbol
                        follows = set(follows).union(follow_set(rule_symbol))
                i = i + 1 
    return follows

def parse(input):
    # returns tokens as (lexeme, tag) 
    tokens =  lexer.lex(input, tok.definitions) 
    print "TOKENS: ", tokens
    # Table[SYMBOL][terminal]   returns production rule
    table = {}
    for symbol in grammer.keys():
        table[symbol] = {} # allocate map for symbol

        print "SYMBOL: ", symbol
        firsts = first_set(symbol)
        print "\t\tFirst_Set:", firsts
        print "\t\tFollow_Set:", follow_set(symbol)
        for first in firsts:
            # add rule whose first matches first
            for rule in grammer[symbol]:
                if rule[0] is first:
                    table[symbol][first] = rule
                    break # added rule, found first

    ##print table
    stack = [START] # start with statement
