'''github.com/138paulmiller
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS 
OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN 
AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH 
THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
''' 

'''
lexer
 Tokenizes input string into tokens(tag, lexeme). With each string literal 
 is paired with a definition
 Each tag is paired with a regular expression, and the corresponding
   lexeme is the matched string from input string
 input
     token_definitions ::= (regex, tag)
           regex ::= regular expression string  
           tag   ::= categorical identifier defined by lexer 
     token       ::= (lexeme, tag)
          lexeme ::= string representation of the token 
          tag    ::= categorical identifier defined by lexer
'''
import re
from ll1 import log
# lex 
# input ::= raw source code 
# returns token list
# where lexeme is string representation 
# A token is a tuple (tag, lexeme) 
def lex(input, token_definitions):
    tokens = []
    i = 0
    while i < len(input):
        regex_match = None # regex match object
        for token_expr in token_definitions: ## iterate through each token definition

            token_tag, regex_pattern = token_expr # get the pattern and tag of token expression
            regex_obj = re.compile(regex_pattern) # compile match obj
            # try to match one of the token expressions to the string of input starting at position i
            regex_match = regex_obj.match(input, i)
            if regex_match: # if match is not none
                lexeme = regex_match.group(0) # grab the capture group
                if token_tag != None: # if the tag is valid token, not whitespace, comments, etc
                    tokens.append((token_tag, lexeme))
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
            log.error("Lexer Error: Invalid symbol: " + input[i])
            raw_input('...')
            break
    return tokens
