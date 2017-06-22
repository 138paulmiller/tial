'''github.com/138paulmiller
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS 
OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN 
AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH 
THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
''' 
import sys
import lexer
from grammar import * # Symbols, definitions and grammar 
from ll1 import * #LL(1) parser package



# Init 
#   Initalizes and returns a ll1 parser
#   the grammar, start, epsilon, eoi symbols and token definitions
def init(grammar, start_sym, epsilon_sym, eoi_sym, definitions):

    table = parse_table.ll1_parse_table(grammar, start_sym, epsilon_sym, eoi_sym)
    print table
    return parser.ll1_parser(table) # create ll1 parser from ll1 table
    

ll1 = init(grammar.rule_map, grammar.START, grammar.EPSILON, grammar.EOI, t.definitions)

def tokenize(input): # tokenize input string. 
    tokens =  lexer.lex(input, t.definitions)
    if len(tokens) <= 0:
        log.error('Parser: No TOKENS')
        return None
    return tokens

def parse_source_code(file_path):
    source = open(file_path)
    code = source.read()
    print code
    root = ll1.parse(tokenize(code))
     


def main():
    argc = len(sys.argv)
    if argc == 1:  # if only script is called, use as realtime parsing interpter
        command = raw_input('>')
        lines = []
        while command != 'quit': # while quit command is not entered
            if command == 'run': # if run command, prompt for file
                parse_source_code((raw_input('File:'))) 
            else:
                lines.append(ll1.parse(tokenize(command)))
            log.write(lines[-1])
            command = raw_input(">")
    elif argc == 2:  # source file is passed
        parse_source_code(sys.argv[1])


if __name__ == "__main__":
    main()





