'''github.com/138paulmiller
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS 
OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN 
AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH 
THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
''' 

import lexer
import log
import ast

'''LL(1) Parser 
- Uses a grammer map such that each symbol maps to a list of production rules.
  Each rule is an in order list of terminal and nonterminals.
  Terminals are token tags that do not exist as a key in the grammer map. 
  
- Symbols : the tag used to identify token tags(terminals) and rule tags (nonterminals)
   
'''


#predefined parsing symbols each self.grammer must use
START = 'START'
EPSILON = 'EPSILON'
EOI = 'EOI' # end of input


class ll1:
    def __init__(self, grammer, definitions):
        self.grammer = grammer
        self.table = {} 
        self.definitions = definitions
        self.init_table()
        # print table
        self.print_table()

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
        if symbol == START: 
            follows.append(EOI) 
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
                                    if first == EPSILON:    # if the first is epsilon
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

    # Table[SYMBOL][terminal]   returns production rule
    def init_table(self):
        for symbol in self.grammer.keys():
            self.table[symbol] = {} # allocate map for symbol
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
                        if first not in self.table[symbol]: # if symbol, first rule has not been added 
                            if first == EPSILON: # get follow of parent symbol if first is epsilon
                                # for each follow, assign epsilon
                                for follow in follows:
                                    self.table[symbol][follow] = [first] # make epsilon symbol a rule (list)
                            else:
                                self.table[symbol][first] = rule
                        else:
                            log.error('Parse Table Error: Duplicate Rules for ' + symbol + ',' + first)


    def print_table(self):
        print 'Parse Table'
        for symbol in self.table.keys():
            print symbol + ':\n'
            for first in self.table[symbol].keys():
                rule = ''
                line = '\t' + '{:<10}'.format(first+ ':')
                for r in self.table[symbol][first]:
                    rule += r + ' ' 
                print  line + '[' + rule + ']'

    def parse_token_action(self,  token_stack, tokens, index):
        print 'action:', token_stack[-1]
        print 'stack :', token_stack
        token_stack.pop()
        
        raw_input('action...')
    
    def print_tree(self, root, i=0):
        print_str = ''
        tab = ''
        j = 0
        while j <= i:
            tab += '   '
            j+=1
        if root != None :
            value = None
            if len(root) > 1: 
                tag = root[0]
                values = root[1]
                print_str = '{:<}:'.format(tag)
                if values != None and len(values) >= 1:
                    for value in values: # print value
                        print_str += self.print_tree(value, i+1)
                else: # value is not a list of values, 
                    print_str += '{:<}'.format(values)
            else:
                print_str += '{:<}'.format(root)
            # green tree
            return '\n\033[32m' +tab + print_str # show tag and values
        return '\033[32m ' + EPSILON # null

                

    def parse_token(self,  root, tokens):
        log.write('TOKENS: ' + str(tokens) + '\n')
        log.write('ROOT:')
        print self.print_tree(root)
        if len(tokens) <= 0: return root # done
        if root != None: 
            if root[0] == tokens[0][0]: # roots tag matches token tag, generated a match to terminal
                root[1] = tokens[0][1] # assign value
                tokens.pop(0)
            elif root[0] in self.table and tokens[0][0]  in self.table[root[0]]: # if root is nonterminal and current token has rules with nonterminal 
                # parse according to rules
                value = []
                if self.table[root[0]][tokens[0][0]] == None:
                    log.error('PARSER ERROR: No Rule for ROOT:' + str(root[0]))
                    log.error('ROOT:' + self.print_tree(root))
                    log.error('TOKENS: ' + str( tokens))

                    return None
                for rule in self.table[root[0]][tokens[0][0]]:
                    if rule != EPSILON:
                        token_value = self.parse_token([rule, None], tokens)
                        if token_value != None and len(token_value) > 1:
                            if token_value[1] != None and token_value[0] == rule: # if the parsed token tag matches rule tag
                                log.write('RULE PARSED: ' + str(rule) + '\nVALUE:')
                                print self.print_tree(token_value)
                                value.append(token_value)
                            else:
                                log.error('PARSER ERROR: Parsing ' + root[0] + ' for Rule: ' + str(rule) + ' RETURNED None')
                                log.error( self.print_tree(token_value))
                                return None    
                        else:
                            log.error('PARSER ERROR: Could not parse RULE:' + str(rule))
                            log.error('TOKENS: ' + str( tokens))
                            return None
                    else:
                        value.append(None)

                root[1] = value
                    
        return root
            
        
    def parse(self, input):
        tokens =  lexer.lex(input, self.definitions)
        tokens.append((EOI, None)) # append end of input token to end of input 
        if len(tokens) <= 0:
            log.error('Parser: No TOKENS')
            return None
        self.validate(tokens)
        root = self.parse_token([START, None], tokens)
        log.write('PARSED TREE:')
        if root:
            print self.print_tree(root)
        else:
            print root
        return root

    # the top of the stack will contain all
    def validate(self, tokens):
        # nonterminal tokens contain null values 
        token_stack = [(EOI, None), (START, None)] # push eoi and start on stack
        index = 0 # current token index
        valid = True
        # token stack contains currently parsed
        while len(token_stack ) > 0 and valid:  
            top_token = token_stack[-1]
            if top_token[0] in self.grammer.keys(): # if top of stack is nonterminal 
            # get rule to do given symbol and token tag (token[1])
                if tokens[index ][0] in self.table[top_token[0]]: # if theres a rule for symbol
                    # copy rule, as to not affect table's rule when popping rule symbols
                    rule = [] # rule symbol list
                    for symbol in self.table[top_token[0]][tokens[index ][0]]:    
                        rule.append(symbol) # add single symbol 
                    # pop stack for both epsilon and non epsilon cases 
                    #self.parse_token_action(token_stack, tokens, index)
                    token_stack.pop() # pop symbol and replace if not epsilon
                    if rule[0] != EPSILON: # if not epsilon
                        # add rule symbols in reverse order into stack
                        while len(rule) > 0:
                            # append null tokens that are used for their tags
                            token_stack.append((rule[-1], None))
                            rule.pop()
                else: # no rule for symbol
                    valid = False # reject input

            if top_token[0] == tokens[index ][0]: # generated a match 
                # take action by calling current token's action function
                #self.parse_token_action(token_stack, tokens, index)
                token_stack.pop()
                index += 1

        # end parse loop
        if valid:
            log.debug('PARSER VALIDATION: SUCCESS')
        else:
            log.error('PARSER VALIDATION: FAILED, No RULE in TABLE[next_token][top_token]')
            log.error('\nTOKEN STACK: ' + str(token_stack))
            log.error('\nNEXT TOKENS: ' + str(tokens[index:-1]) + '\n')

        return valid