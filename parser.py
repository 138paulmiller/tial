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
ST   = 'STMT'
E = 'EXPR' # expressions grouped with adders
E_OP = 'EXPR_OP'# operation with expression
T = 'TERM'       #expressions grouped by multipliers
T_OP = 'TERM_OP' # operation with term
F = 'FACTOR' # basic unit of expression
EPSILON = 'EPSILON'
EOI = 'EOI' # end of input

# grammer uses the token tags as terminals and parse tree nodes as nonterminals or symbols
#   Grammer is a map of symbols. Each symbols matches to a precedence ordered rule list where 
#   each rule is a list of terminals and nonterminals that define symbol 
grammer = {
           
            E    : [[T, E_OP]],
            E_OP : [[tok.ADD, T, E_OP], 
                            [tok.SUB, T, E_OP],
                            [EPSILON]],

            T          : [[F, T_OP]],
            T_OP       : [[tok.MUL, F, T_OP], 
                            [tok.DIV, F, T_OP], 
                            [EPSILON]],

            F        : [[tok.NUM], # expression rule 1
                            [tok.ID],
                            [tok.L_PAREN, E, tok.R_PAREN]]
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
    # search for symbol in every rule of every other symbol
    for rule_symbol in grammer.keys():  # each symbol contains a rule set,  
        for rule in grammer[rule_symbol]:  # iterate through each rule in set for each symbol
            i = 0
            while i <  len(rule):     # check every symbol in rule
                if rule[i] == symbol:# if rule symbol is equal to symbol
                    if i+1 < len(rule): # try to get the next following symbol in the rule
                        if rule[i+1] not in grammer: # if terminal
                            follows.append(rule[i+1]) # append rule symbol if terminal
                        else: # if nonterminal, union nonterminal's firsts into follow
                            for first in first_set(rule[i+1]):
                                if first is EPSILON: # concat follow of parent rule
                                    follows = follows + [x for x in iter(follow_set(rule_symbol)) if x not in follows]
                                elif first not in follows: # add first if it doesnt already exist
                                    follows.append(first)
                    elif rule_symbol is not symbol: # if at the end of rule, append the follow set of the parent rule symbol
                        follows = follows + [x for x in iter(follow_set(rule_symbol)) if x not in follows]
                i = i + 1 
    return follows

def initParseTable():
    table = {}
    nonterminals = []
    for symbol in grammer.keys():
        table[symbol] = {} # allocate map for symbol
        print "SYMBOL: ", symbol
        firsts = first_set(symbol)
        follows = follow_set(symbol)
        print "\t\tFirst_Set:", firsts
        print "\t\tFollow_Set:", follows
        for first in firsts:
            if first not in nonterminals:
                nonterminals.append(first)
            # add rule whose first matches first
            for rule in grammer[symbol]:
                if first in first_set(rule[0]):

                    if first not in table[symbol]: # if symbol, first rule has not been added 
                        if first is EPSILON: # get follow of parent symbol
                            # for each follow, assign epsilon
                            for follow in follows:
                                table[symbol][follow] = [first] # make epsilon a rule list
                        else:
                            table[symbol][first] = rule
                    else:
                        sys.stderr.write('Parse Table Error: Duplicate Rules for ' + symbol + ',' + first)
        # for first in table[symbol].keys():
        #     print  '\t', first, '\t', table[symbol][first]

    # print table

    for symbol in table.keys():
        print symbol + ':\n'
        for first in table[symbol].keys():
            rule = ''
            line = '\t' + '{:<10}'.format(first+ ':')
            for r in table[symbol][first]:
                rule += r + ' ' 
            print  line + '[' + rule + ']'

    

def parse(input):
    initParseTable()
    # returns tokens as (lexeme, tag) 
    tokens =  lexer.lex(input, tok.definitions) 
    print "TOKENS: ", tokens
    # Table[SYMBOL][terminal]   returns production rule
    return "parse return"
