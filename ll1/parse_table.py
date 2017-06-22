from ll1 import log

# LL(1) Parse Table:
#   Given a grammer, start symbol, epsilon symbol, and eoi symbol
#   This class will initalize itself such that for every nonterminal 
#   is mapped to a rule by a terminal symbol
#   rule = self[nonterminal][terminal]
#   Where tnA are terminals, rn are rules, and A, B are nonterminals
#   A = { t1 : r1, t2 : r2 ..., tn : rn}
#   B = { t1 : r1, t2 : r2 ..., tn : rn}
#   # NOT every nonterminal contains every terminal, if none exists then no production rule
class ll1_parse_table(dict): # override dict functionality

    def __init__(self, grammer, start_sym, epsilon_sym, eoi_sym):
        self.grammer = grammer
        #predefined parsing symbols each self.grammer must use
        self.START = start_sym
        self.EPSILON = epsilon_sym
        self.EOI = eoi_sym# end of input
        self.init()
    
    
    #prints parse table
    def __repr__(self):
        table = 'Parse Table'
        for symbol in self.keys():
            table += symbol + ':\n'
            for first in self[symbol].keys():
                rule = ''
                line = '\t' + '{:<10}'.format(first+ ':')
                for r in self[symbol][first]:
                    rule += r + ' ' 
                table +=  line + '[' + rule + ']\n'
        return table

    # returns list of possible symbols that are the first symbol in the rule
    def first_set(self, symbol):
        firsts = []
        if symbol in self.grammer: ## if symbols rules exits
            rule_set = self.grammer[symbol]
            # get the first of the first possible rule, avoid first of self 
            for rule in rule_set: # check each rule. Rule is list of inorder symbols
                # if rule's first symbol is not the same as root. add the first set 
                #   of that symbol to this symbols first set
                if len(rule) > 0 and (rule[0] != symbol): 
                    firsts  = firsts + self.first_set(rule[0]) # concat first sets
        else: # no rules
            # the symbol is a terminal, so return it as is
            firsts.append(symbol)
        return firsts


    #returns list of symbols that can follow the given symbol
    def follow_set(self, symbol):
        follows  = [] # set of follow symbols
        # End of input follows start by default 
        if symbol == self.START: 
            follows.append(self.EOI) 
        ''' search for symbol in every rule of every other symbol and find next possible
            terminal symbol that can follow current symbol
            iterate through rule set from each symbol'''
        for rule_symbol in self.grammer.keys():  
            # iterate through each rule in rule set for each symbol
            for rule in self.grammer[rule_symbol]:
                i = 0   # index of the symbol in the rule
                # check every symbol in rule
                while i <  len(rule):   
                    if rule[i] == symbol:   # if rule symbol is equal to symbol
                        if i+1 < len(rule): # try to get the next following symbol in the rule
                            if rule[i+1] not in self.grammer:    # if next symbol is terminal 
                                    follows.append(rule[i+1])   # append rule symbol to follow set
                            else:   # else if next symbol is nonterminal, union nonterminal's firsts into follow
                                for first in self.first_set(rule[i+1]):  # for each first in the next symbols rule set 
                                    if first == self.EPSILON:    # if the first is epsilon
                                        # union symbol's follow set with the follow set of the parent rule symbol                                    
                                        follows = follows + [x for x in iter(self.follow_set(rule_symbol)) if x not in follows]
                                    elif first not in follows:  # if not epsilon and doesnt already exist in follow set
                                        follows.append(first)   # append symbol to follow set
                        # if at the end of rule(no next symbol)
                        elif rule_symbol != symbol:
                            #union symbol's follow set with the follow set of the parent rule symbol
                            follows = follows + [x for x in iter(self.follow_set(rule_symbol)) if x not in follows]
                    i = i + 1 
        return follows # return follow set

    # self[SYMBOL][terminal]  returns production rule
    def init(self):
        for symbol in self.grammer.keys():
            self[symbol] = {} # allocate map for symbol
            log.debug("SYMBOL: " + str(symbol))
            # find first and follow set
            firsts = self.first_set(symbol)
            follows = self.follow_set(symbol)
            
            log.debug("\t\tFirst_Set:")
            log.debug(str(firsts))
            log.debug("\t\tFollow_Set:")
            log.debug(str(follows))
            for first in firsts:
                # add rule whose first matches first of rule
                for rule in self.grammer[symbol]: # for each rule in symbols rule list
                    if first in self.first_set(rule[0]): # if the first matches the first of the rule
                        if first not in self[symbol]: # if symbol, first rule has not been added 
                            if first == self.EPSILON: # get follow of parent symbol if first is epsilon
                                # for each follow, assign epsilon
                                for follow in follows:
                                    self[symbol][follow] = [first] # make epsilon symbol a rule (list)
                            else:
                                self[symbol][first] = rule
                        else:
                            log.error('Parse Table Error: Duplicate Rules for ' + symbol + ',' + first)

