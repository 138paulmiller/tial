'''github.com/138paulmiller
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS 
OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN 
AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH 
THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
''' 
import sys
import evaluator
import grammar # Symbols, definitions and grammar 
from ll1 import ll1_init #Inits LL(1) parser 


ll1 = ll1_init(grammar.rule_map, grammar.START, grammar.EPSILON, grammar.definitions)

def parse_source_code(file_path):
    source = open(file_path)
    code = source.read()
    print code
    root = ll1.parse(code)
    evaluator.eval(root)


def main():
    argc = len(sys.argv)
    if argc == 1:  # if only script is called, use as realtime parsing interpter
        input = raw_input('>')
        lines = []
        while input != 'quit': # while quit command is not entered
            if input == 'run': # if run command, prompt for file
                parse_source_code((raw_input('File:'))) 
            else:
                lines.append(ll1.parse(input))
            evaluator.eval(lines[-1])
            input = raw_input(">")
    elif argc == 2:  # source file is passed
        parse_source_code(sys.argv[1])


if __name__ == "__main__":
    main()





