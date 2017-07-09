from ll1 import log 
from ll1 import lexer

class ll1_parser(object):
    def __init__(self, lexemes, parse_table):
        self.table = parse_table
        self.lexemes = lexemes 
    '''  Parse 
        input - raw input string to tokenize and parse
            tokenizes input string into list of tokens, returned by lexer 
                token - (symbol_tag, value) with value = (symbol_tag, value)
                symbol_tag - terminal or nonterminal identifier
                value - list of tokens that are in order according to production rule for symbol
        returns - parse tree's root token
    '''
    def parse(self, input):
        tokens =  lexer.lex(input, self.lexemes)
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
            root_tag = root[0]
            root_value = root[1]
            next_token = tokens[0]
            next_tag = next_token[0]
            next_value = next_token[1]  
            if root_tag == next_tag: # roots tag matches token tag, generated a match to terminal
                tokens.pop(0) # move to the next token 
                return next_token# return matched token token value
            elif root_tag in self.table and next_tag in self.table[root[0]]: # if root is nonterminal and current token has rules with nonterminal 
                value = []
                if self.table[root_tag][next_tag] == None: # no production rule in table from root symbol to next token 
                    log.error('ERROR: No Rule for ROOT:' + str(root_tag))
                    return None
                # else, for each symbol in rule 
                for rule_tag in self.table[root_tag][next_tag]:
                    # parse the remaining tokens for the rule
                    if rule_tag != self.table.EPSILON:
                        # if not epsilon, attempt to parse the remaining tokens for the given symbol in the rule                        
                        rule_token = self.parse_token([rule_tag, None], tokens)
                        # if rule token parsed is valid and is a token pair(tag, value)
                        if rule_token != None and len(rule_token) > 1:
                            # if the parsed token tag matches rule tag     
                            value.append(rule_token)  
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
        token_stack = [(self.table.START, None)] # push eoi and start on stack
        index = 0 # current token index
        valid = True
        # token stack contains currently parsed
        while len(token_stack ) > 0 and valid:  
            top_token = token_stack[-1]
            if top_token[0] == tokens[index ][0]: # generated a match 
                # take action by calling current token's action function
                token_stack.pop()
                index += 1            
            # get rule to do given symbol and token tag (token[0])
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
            log.error('VALIDATION: FAILED, No RULE in TABLE[top_token][next_token]')
            log.error('TOP TOKEN: ' + str(top_token))
            log.error('NEXT TOKEN: ' + str( tokens[index]) + '\n')

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
            tag = root[0]
            value_list = root[1]
            if tag in self.table: # nonterminal, recursively print
                print_str = '{:<}:'.format(tag)
                if value_list != None:
                    for value in value_list: # print value
                        print_str +=  self.print_tree_str(value, i+1)
                else: # value is not a list of values, 
                    print_str += '{:<}'.format(value_list)
            else:
                print_str = tag + ' ' + str(value_list)
            # green tree
            return '\n\033[32m' +tab + print_str # show tag and values
        return 'None' 

