# Paul Miller 2016
# All rights reserved

import re
import sys

# EAT - Essentially A Tokenizer
# - a regex based tokenizer module that accepts a characters of code and returns
#   a list of tokens such that a token is a tuple where token = (lexeme, tag)
# symbols - the string of characters used to generate a list of tokens
# tok_exprs, a list of token expressions where token expression = (regex_pattern, tag)

def tokenize(symbols, tok_exprs):
    tokens = [] # list of tokens where a token = (lexeme, tag)
    i = 0
    while i < len(symbols):
        regex_match = None # regex match object

        for tok_expr in tok_exprs: ## iterate through each token expressions

            regex_pattern, tok_tag = tok_expr # get the pattern aqnd tag of token expression
            regex_obj = re.compile(regex_pattern)

            # try to match one of the token expressions to the string of symbols starting at position i
            regex_match = regex_obj.match(symbols, i)
            if regex_match: # if match is not none
                lexeme = regex_match.group(0) # grab the capture group

                if tok_tag: # if the tag is valid token, not whitespace, comments, etc
                    tokens.append((lexeme, tok_tag))
                break
        # end of token expression check, check if any of the
        # token expr matched the symbol string at i,
        # if so, move i to the end of the match characters
        if regex_match:
            i = regex_match.end(0)
        else:
            sys.stderr.write("Lexer Error: Invalid symbol" + symbols[i])
            break

    return tokens
