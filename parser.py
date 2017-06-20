# Paul Miller 2016
# All rights reserved

import lexer
import log
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
STMT   = 'STMT'
EXPR = 'EXPR' # expressions grouped with adders
EXPR_OP = 'EXPR_OP'# operation with expression
TERM = 'TERM'       #expressions grouped by multipliers
TERM_OP = 'TERM_OP' # operation with term
FACTOR = 'FACTOR' # basic unit of expression
EPSILON = 'EPSILON'
EOI = 'EOI' # end of input

# grammer uses the token tags as terminals and parse tree nodes as nonterminals or symbols
#   Grammer is a map of symbols. Each symbols matches to a precedence ordered rule list where 
#   each rule is a list of terminals and nonterminals that define symbol 
grammer = {
            START : [[EXPR]],
            EXPR    : [[TERM, EXPR_OP]],
            EXPR_OP : [[tok.ADD, TERM, EXPR_OP], 
                            [tok.SUB, TERM, EXPR_OP],
                            [EPSILON]],

            TERM          : [[FACTOR, TERM_OP]],
            TERM_OP       : [[tok.MUL, FACTOR, TERM_OP], 
                            [tok.DIV, FACTOR, TERM_OP], 
                            [EPSILON]],

            FACTOR        : [[tok.NUM], # expression rule 1
                            [tok.ID],
                            [tok.L_PAREN, EXPR, tok.R_PAREN]]
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
    if symbol == START: # End of input follows start by default, 
                        # because start will not appear in any other rules
        follows.append(EOI) 
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
                                if first == EPSILON: # concat follow of parent rule
                                    follows = follows + [x for x in iter(follow_set(rule_symbol)) if x not in follows]
                                
                                elif first not in follows: # add first if it doesnt already exist
                                    follows.append(first)
                    elif rule_symbol != symbol: # if at the end of rule, append the follow set of the parent rule symbol
                        follows = follows + [x for x in iter(follow_set(rule_symbol)) if x not in follows]
                i = i + 1 
    return follows

# Table[SYMBOL][terminal]   returns production rule
def init_table():
    table = {} 
    for symbol in grammer.keys():
        table[symbol] = {} # allocate map for symbol
        print "SYMBOL: ", symbol
        # find first and follow set
        firsts = first_set(symbol)
        follows = follow_set(symbol)
        print "\t\tFirst_Set:", firsts
        print "\t\tFollow_Set:", follows
        for first in firsts:
            # add rule whose first matches first of rule
            for rule in grammer[symbol]: # for each rule in symbols rule list
                if first in first_set(rule[0]): # if the first matches the first of the rule
                    if first not in table[symbol]: # if symbol, first rule has not been added 
                        if first == EPSILON: # get follow of parent symbol if first is epsilon
                            # for each follow, assign epsilon
                            for follow in follows:
                                table[symbol][follow] = [first] # make epsilon symbol a rule (list)
                        else:
                            table[symbol][first] = rule
                    else:
                        log.error('Parse Table Error: Duplicate Rules for ' + symbol + ',' + first)

    return table


def print_table(table):
    print 'Parse Table'
    for symbol in table.keys():
        print symbol + ':\n'
        for first in table[symbol].keys():
            rule = ''
            line = '\t' + '{:<10}'.format(first+ ':')
            for r in table[symbol][first]:
                rule += r + ' ' 
            print  line + '[' + rule + ']'


def parse(input):
    table = init_table()
    # print table
    raw_input('\n....')
    print_table(table)
    # returns tokens as (lexeme, symbol_tag) 
    tokens =  lexer.lex(input, tok.definitions)
    tokens.append((0,EOI)) # append end of input token to end of input 
    print "TOKENS: ", tokens
    if len(tokens) <= 0:
        log.error('\nParser: No TOKENS')
        return None
    stack = [EOI, START] # push eoi and start on stack
    t_i = 0 # current token index
    valid = True
    while len(stack) > 0 and valid:        
        print 'tokens', tokens[t_i]
        print 'stack: ', stack
        if stack[-1] in table: 
            print 'rules', table[stack[-1]]
        else:
            print 'no rules'
        if stack[-1] in grammer.keys(): # if top of stack is nonterminal 
        # get rule to do given symbol and token tag (token[1])
            if tokens[t_i][1] in table[stack[-1]]: # if theres a rule for symbol
                # copy rule, as to not affect table's rule when calling pop
                rule = [] # character list
                for symbol in table[stack[-1]][tokens[t_i][1]]:    
                    rule.append(symbol)
                # pop stack if epsilon
                print stack[-1], ',', tokens[t_i][1], 'rule:',rule
                stack.pop() # pop symbol and replace if if not epsilon
                if rule[0] != EPSILON:
                    # add rule symbols in reverse order into stack
                    while len(rule) > 0:
                        stack.append(rule[-1])
                        rule.pop()
            else: # no rule for symbol
                valid = False # reject input

        if stack[-1] == tokens[t_i][1]: # generated a match 
            print 'Matched Token ',  tokens[t_i][0], 'with ', stack[-1], '...'
            # pop symbol and move to next token
            stack.pop()
            t_i += 1

        raw_input('...')
    
    if valid:
        print "parser accepted input"   
    else:
        log.error('Parsing Failed: Could not get rule for token:\t'+ str(tokens[t_i]) )
        log.error('Stack: ' + str(stack))

    return valid