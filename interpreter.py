'''github.com/138paulmiller
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS 
OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN 
AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH 
THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
''' 
import sys
import parser


# Symbols (Nonterminals) 
import tok

STMT   = 'STMT'
EXPR = 'EXPR' # expressions grouped with adders
EXPR_OP = 'EXPR_OP'# operation with expression
TERM = 'TERM'       #expressions grouped by multipliers
TERM_OP = 'TERM_OP' # operation with term
FACTOR = 'FACTOR' # basic unit of expression


# grammer uses the token tags as terminals and parse tree nodes as nonterminals or symbols
#   Grammer is a map of symbols. Each symbols matches to a precedence ordered rule list where 
#   each rule is a list of terminals and nonterminals that define symbol 
grammer = {
            parser.START : [[EXPR]],
            EXPR    : [[TERM, EXPR_OP]],
            EXPR_OP : [[tok.ADD, TERM, EXPR_OP], 
                            [tok.SUB, TERM, EXPR_OP],
                            [parser.EPSILON]],

            TERM          : [[FACTOR, TERM_OP]],
            TERM_OP       : [[tok.MUL, FACTOR, TERM_OP], 
                            [tok.DIV, FACTOR, TERM_OP], 
                            [parser.EPSILON]],

            FACTOR        : [[tok.NUM], # expression rule 1
                            [tok.ID],
                            [tok.L_PAREN, EXPR, tok.R_PAREN]]
        }


ll1_parser = parser.ll1(grammer, tok.definitions)

def parse_source_code(file_path):
    source = open(file_path)
    code = source.read()
    print code
    root = ll1_parser.parse(code)
     


def main():
    argc = len(sys.argv)
    if argc == 1:  # if only script is called, use as realtime parsing interpter
        command = raw_input('>')
        lines = []
        while command != 'quit': # while quit command is not entered
            if command == 'run': # if run command, prompt for file
                parse_source_code((raw_input('File:'))) 
            else:
                lines.append(ll1_parser.parse(command))
            print lines[-1]
            command = raw_input(">")
    elif argc == 2:  # source file is passed
        parse_source_code(sys.argv[1])


if __name__ == "__main__":
    main()





