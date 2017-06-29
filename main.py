'''github.com/138paulmiller
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS 
OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN 
AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH 
THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
''' 
import sys
import grammar # Symbols, definitions and grammar 
import actions
from cli import *
from ll1 import ll1_init #Inits LL(1) parser 



def main():
    # create root context for session
    ll1_parser = ll1_init(grammar.rule_map, grammar.START, grammar.EPSILON, grammar.definitions)
    root_context = context.context(actions.eval_map)
    argc = len(sys.argv)
    if argc == 1:  # if only script is called, use as realtime parsing interpter
        input = raw_input('>')
        while input != 'quit': # while quit command is not entered    
            interpret(ll1_parser, root_context, input)
            input = raw_input(">")
    elif argc == 2:  # interpret file
        interpret_source_file(ll1_parser, root_context, sys.argv[1])


if __name__ == "__main__":
    main()





