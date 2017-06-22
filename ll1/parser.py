from ll1 import log 


class ll1_parser(object):
    def __init__(self, parse_table):
        self.table = parse_table


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
        return '\033[32m ' + self.table.EPSILON # null

    def parse_token(self,  root, tokens):
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
                    if rule != self.table.EPSILON:
                        token_value = self.parse_token([rule, None], tokens)
                        if token_value != None and len(token_value) > 1:
                            if token_value[1] != None and token_value[0] == rule: # if the parsed token tag matches rule tag
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
            
    # returns ast root
    def parse(self, tokens):
        # append EOI to token queue
        tokens.append((self.table.EOI, None)) # append end of input token to end of input 
        self.validate(tokens)
        root = self.parse_token([self.table.START, None], tokens)
        log.write('PARSED TREE:')
        if root:
            print self.print_tree(root)
        else:
            print root
        return root

    # the top of the stack will contain all
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
                #self.parse_token_action(token_stack, tokens, index)
                token_stack.pop()
                index += 1            
            # get rule to do given symbol and token tag (token[1])
            elif tokens[index ][0] in self.table[top_token[0]]: # if theres a rule for symbol(nonterminal)
                # copy rule, as to not affect table's rule when popping rule symbols
                rule = [] # rule symbol list
                for symbol in self.table[top_token[0]][tokens[index ][0]]:    
                    rule.append(symbol) # add single symbol 
                # pop stack for both epsilon and non epsilon cases 
                #self.parse_token_action(token_stack, tokens, index)
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
            log.debug('PARSER VALIDATION: SUCCESS')
        else:
            log.error('PARSER VALIDATION: FAILED, No RULE in TABLE[next_token][top_token]')
            log.error('\nTOKEN STACK: ' + str(token_stack))
            log.error('\nNEXT TOKENS: ' + str(tokens[index:-1]) + '\n')

        return valid