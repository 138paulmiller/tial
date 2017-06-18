# github.com/138paulmiller
# CopyLeft :)

# ASIL lexer
# This is a basic lexer implementation. All tokens are defined as tuples (lexeme, tag)
# input
#     token_exprs ::= (match, tag)
#           match ::= regular expression string (regex match) 
#           tag   ::= categorical identifier defined by lexer 
#     token       ::= (lexeme, tag)
#          lexeme ::= string representation of the token 
#          tag    ::= categorical identifier defined by lexer
# The regular expression, tag pairings are then tokenized by eat.py module.
import re
import sys
# lex 
# input ::= raw source code 
# returns token list
# where lexeme is string representation 
# A token is a tuple (lexeme, tag) 
def lex(input, token_exprs):
    tokens = [] # list of tokens where a token = (lexeme, tag)
    i = 0
    while i < len(input):
        regex_match = None # regex match object

        for token_expr in token_exprs: ## iterate through each token expressions

            regex_pattern, token_tag = token_expr # get the pattern aqnd tag of token expression
            regex_obj = re.compile(regex_pattern) # compile match obj

            # try to match one of the token expressions to the string of input starting at position i
            regex_match = regex_obj.match(input, i)
            if regex_match: # if match is not none
                lexeme = regex_match.group(0) # grab the capture group

                if token_tag: # if the tag is valid token, not whitespace, comments, etc
                    tokens.append((lexeme, token_tag))
                break #found token
        # end of token expression check, check if any of the
        # token expr matched the symbol string at i,
        # if so, move i to the end of the match characters
        if regex_match:
            j = regex_match.end(0)
            if i is j: 
                  # did not advance, repeating same match, break loop
                  break 
            else:
                  i = j 
        else:
            sys.stderr.write("Lexer Error: Invalid symbol" + input[i])
            break
    return tokens
