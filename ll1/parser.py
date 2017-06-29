from ll1 import log 
from ll1 import lexer

class ll1_parser(object):
    def __init__(self, token_definitions, parse_table):
        self.table = parse_table
        self.token_definitions = token_definitions 
    '''  Parse 
        input - raw input string to tokenize and parse
            tokenizes input string into list of tokens, returned by lexer 
                token - (symbol_tag, value) with value = (symbol_tag, value)
                symbol_tag - terminal or nonterminal identifier
                value - list of tokens that are in order according to production rule for symbol
        returns - parse tree's root token
    '''
    def parse(self, input):
        tokens =  lexer.lex(input, self.token_definitions)
        if len(tokens) <= 0:
            log.error('No TOKENS')
            return None
        # append EOI to token queue
        tokens.append((self.table.EOI, None)) # append end of input token to end of input 
        self.validate(tokens)
        # begin by parsing the start token
        root = self.parse_token([self.table.START, None], tokens)
        return root

    '''
        Parse token
            Parses the root token from the given tokens.
            If the root symbol matches the current token's symbol
            then assign the roots value to the token's value and remove it.
            Otherwise, check to see if the current token has a production rule from the root
            symbol. If no production rule in the table exists

            root - tag, value pair to be parsed
            tokens - remaining input tokens

            returns parsed root pair 
    '''
    def parse_token(self,  root, tokens):
        if len(tokens) <= 0: return root # done, no tokens
        # tokens[0] is next token with its symbol tag tokens[0][0]  and its value at tokens[0][1] 
        if root != None: 
            if root[0] == tokens[0][0]: # roots tag matches token tag, generated a match to terminal
                root[1] = tokens[0][1] # assign value
                tokens.pop(0)
            elif root[0] in self.table and tokens[0][0]  in self.table[root[0]]: # if root is nonterminal and current token has rules with nonterminal 
                value = []
                if self.table[root[0]][tokens[0][0]] == None: # no production rule in table from root symbol to next token 
                    log.error('ERROR: No Rule for ROOT:' + str(root[0]))
                    return None
                # else, for each symbol in rule 

                for rule_symbol in self.table[root[0]][tokens[0][0]]:
                    # parse the remaining tokens for the rule
                    if rule_symbol != self.table.EPSILON:
                        # if not epsilon, attempt to parse the remaining tokens for the given symbol in the rule
                        rule_token = self.parse_token([rule_symbol, None], tokens)
                        # if rule token parsed is valid and is a token pair(tag, value)
                        if rule_token != None and len(rule_token) > 1:
                            # if the parsed token tag matches rule tag
                            if rule_token[1] != None and rule_token[0] == rule_symbol: 
                                value.append(rule_token)
                            else: # could not parse a value for rule_token
                                log.error('ERROR: Parsing ' + root[0] + ' for Rule: ' + str(rule_symbol) + ' RETURNED None')
                                return None    
                        else: # else, rule_symbol could not be parsed
                            log.error('Could not parse RULE:' + str(rule_symbol) + '\n\tTOKENS: ' + str( tokens))
                            return None
                    else:
                        value.append(None)
                root[1] = value # update roots value to the parsed value
        return root
            

    # validates syntax using mehod where symbols are popped and rules are pushed onto stack 
    # until all symbols, terminal, are are matched
    def validate(self, tokens):
        # nonterminal tokens contain null values 
        token_stack = [(self.table.EOI, None), (self.table.START, None)] # push eoi and start on stack
        index = 0 # current token index
        valid = True
        # token stack contains currently parsed
        while len(token_stack ) > 0 and valid:  
            top_token = token_stack[-1]
            if top_token[0] == tokens[index ][0]: # generated a match 
                # take action by calling current token's action function
                token_stack.pop()
                index += 1            
            # get rule to do given symbol and token tag (token[1])
            elif tokens[index ][0] in self.table[top_token[0]]: # if theres a rule for symbol(nonterminal)
                # copy rule, as to not affect table's rule when popping rule symbols
                rule = [] # rule symbol list
                for symbol in self.table[top_token[0]][tokens[index ][0]]:    
                    rule.append(symbol) # add single symbol 
                # pop stack for both epsilon and non epsilon cases 
                token_stack.pop() # pop symbol and replace if not epsilon
                if rule[0] != self.table.EPSILON: # if not epsilon
                    # add rule symbols in reverse order into stack
                    while len(rule) > 0:
                        # append null tokens that are used for their tags
                        token_stack.append((rule[-1], None))
                        rule.pop()
            else: # no rule for symbol
                valid = False # reject input


        # end parse loop
        if valid:
            log.debug('VALIDATION: SUCCESS')
        else:
            log.error('VALIDATION: FAILED, No RULE in TABLE[next_token][top_token]')
            log.error('TOKEN STACK: ' + str(token_stack))
            log.error('NEXT TOKENS: ' + str(tokens[index:-1]) + '\n')

        return valid

    
    def print_tree(self, root):
        print self.print_tree_str(root)

    def print_tree_str(self, root, i=0):
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
                        print_str +=  self.print_tree_str(value, i+1)
                else: # value is not a list of values, 
                    print_str += '{:<}'.format(values)
            else:
                print_str += '{:<}'.format(root)
            # green tree
            return '\n\033[32m' +tab + print_str # show tag and values
        return '\033[32m EPSILON' 

