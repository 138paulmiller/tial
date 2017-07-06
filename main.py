'''github.com/138paulmiller
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS 
OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN 
AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH 
THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
''' 
import sys
import grammar # Symbols tags
import evaluator
import session
from ll1 import * # LL(1) parser 
DEBUG = True
# Defines what function will process each tag
# The eval map is used by the context to allow the user to define a function how to evaluate at each given 
# step by just using the contexts eval that will map it to the function   
evaluation_map = {
            grammar.START   : evaluator.eval_start,
            grammar.FUNC_DEF : evaluator.eval_func_def,
            grammar.FUNC_CALL : evaluator.eval_func_call,
            grammar.ARGS  : evaluator.eval_args,
            grammar.BODY    : evaluator.eval_body,
            grammar.STMT    : evaluator.eval_stmt,
            grammar.EXPR    : evaluator.eval_expr,
            grammar.EXPR_LIST  : evaluator.eval_expr_list,
            grammar.EXPR_OP : evaluator.eval_expr_op, 
            grammar.TERM    : evaluator.eval_term,
            grammar.TERM_OP : evaluator.eval_term_op,
            grammar.FACTOR  : evaluator.eval_factor
            }


def interpret(parser, context, code, debug=False):
    root =  parser.parse(code)
    if debug:
        parser.print_tree(root)
    context = context.eval(root, context) # the start rule returns an evaluation context
    if debug:
        context.print_vars()
    return context


def interpret_source_file(parser, context, file_path,  debug=False):
    source = open(file_path)
    code = source.read()
    print code[:-1]
    return interpret(parser, context, code)


def main():
    ll1_parser = ll1_load_grammar('grammar.ll1',grammar.START, grammar.EPSILON)
    # create root context for session
    #ll1_parser = ll1_init(grammar.rule_map, grammar.START, grammar.EPSILON, grammar.lexemes)
    context = session.context(evaluation_map)
    argc = len(sys.argv)
    if argc == 1:  # if only script is called, use as realtime parsing interpter
        input = raw_input('>')
        while input != 'quit': # while quit command is not entered    
            context = interpret(ll1_parser, context, input, DEBUG)
            print 'SESSION CONTEXT:'
            context.print_vars()
            input = raw_input(">")
            
    elif argc == 2:  # interpret file
        context = interpret_source_file(ll1_parser, context, sys.argv[1], DEBUG)
        print 'SESSION CONTEXT:'
        context.print_vars()
        
if __name__ == "__main__":
    main()





