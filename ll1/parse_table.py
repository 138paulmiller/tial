from ll1 import log


'''LL(1) Parse Table

# Constructs an LL(1) parse table from a given Grammer.
    The table is map of nonterminal maps. Table = { nonterminal : { first, rule} }
    Each nonterminal is mapped to a rule by one of it's firsts.
    Allows rules access as table[terminal][nonterminal]
    If terminal is not in table[nonterminal] then reject terminal
    
    Remember, if two distinct rules are mapped from table[nonterminal][terminal]
         then the grammer is not LL(1) !!

# Grammer : map with each nonterminal key is mapped to a list of production rules

# Rules : an in order list of terminals and nonterminals.
 
# Terminals : symbols that are not mapped to production rules

# Epsilon  :  a special terminal that allows nonterminal to terminal  
  
# Symbols : the tag used to identify token tags(terminals) and rule tags (nonterminals)
 
# First set : the set of possible first terminals that match with a production rule for a nonterminal.
              If a terminal parsed is a e, and e is also within the first set of S.
              For each rule for a nonterminal, each rule's first symbol
              If the first symbol is a terminal then add it to first set
              If the first symbol is a nonterminal and not equal to first set's nonterminal
                then union the nonterminals first into first set


# Follow set : the set of terminals that follow a nonterminal symbol in any given production rule.
                For a nonterminal in rule r.
                If the nonterminal has nothing following it or follows EPSILON in rule, 
                    then union the follow set of the nonterminal that is mapped to rule r,
                    the parent symbol, if it is not the same.
                If the following symbol in rule is a nonterminal, 
                    then union the follow set with the following nonterminal's first set. 
                    If one of the firsts is epsilon, then union the follow set of parent symbol 
                By default START is followed by EOI

# Example Grammer and Table Constructed
    Nonterminals : S, E
    Terminals    : a, +, EPSILON
    Grammer = 
    {
        E : [[T, A]],
        A : [[+, T, A],
             [EPSILON]
            ]
        T : [[a]]
    }
    
    first_set(E) = [a]              # first set of T
    first_set(A) = [+, EPSILON]     # + and  epsilon are terminal so add 
    first_set(T) = [a]              # a is terminal so add

    follow_set(E) = [EOI]           # is start so default follows EOI   
    follow_set(A) = [EOI]           # A follows nothing in each rule, so union the follow of rules symbol that is not A,
                                      so follow set of E  
    follow_set(T) = [+, EOI]        # T is followed by A, so follow first set of A, however, epsilon is in first so union
                                    # follow set of A

    Table =
    {
        E : { a : [T, A], }
        A : { + : [T, A], EOI : [EPSILON] }
        T : { a : [a] }
    }

        | a   |  +  | EOI
    ----------------------
    E   | T A |     |
    A   |     | T A | EPSILON
    T   |  a  |     |

'''

class ll1_parse_table(dict): 
    # Inherits dict to allow access to rule for table[nonterminal][terminal]
    def __init__(self, grammer, start_sym, epsilon_sym):
        self.grammer = grammer
        #predefined parsing symbols each self.grammer must use
        self.START = start_sym
        self.EPSILON = epsilon_sym
        self.EOI = 'EOI'# default end of input symbol
        self.construct()
    

    #returns string representation of table
    def __repr__(self):
        table = 'Parse Table\n'
        for symbol in self.keys():
            table += symbol + ':\n'
            for first in self[symbol].keys():
                rule = ''
                line = '\t' + '{:<10}'.format(first+ ':')
                for r in self[symbol][first]:
                    rule += r + ' ' 
                table +=  line + '[' + rule + ']\n'
        return table

    # Constructs the LL(1) parse table grammers rules. 
    def construct(self):
        for symbol in self.grammer.keys():
            self[symbol] = {} # allocate map for symbol
            # find first and follow set
            firsts = self.first_set(symbol)
            follows = self.follow_set(symbol)            
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
                            log.error('TABLE: Duplicate Rules for ' + symbol + ',' + first)

    # returns list of possible symbols that are the first symbol in the rule
    def first_set(self, symbol):
        firsts = []
        if symbol in self.grammer: ## if symbols rules exits
            rule_set = self.grammer[symbol]
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
                        # if at the end of rule(no next symbol), 
                        elif rule_symbol != symbol:#and parent symbol is not the same as current symbol
                            #union symbol's follow set with the follow set of the parent rule symbol
                            follows = follows + [x for x in iter(self.follow_set(rule_symbol)) if x not in follows]
                    i = i + 1 
        return follows # return follow set


