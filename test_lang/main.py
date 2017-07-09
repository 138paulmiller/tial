'''github.com/138paulmiller
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS 
OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN 
AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH 
THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
''' 
import sys
import ir_gen
import ir_parse
from ll1 import * # LL(1) parser 
from ctypes import CFUNCTYPE, c_int

DEBUG = False
# Defines what function will process each tag
# The eval map is used by the context to allow the user to define a function how to evaluate at each given 
# step by just using the contexts eval that will map it to the function   



def generate_module(ir_builder, parser, code, show_parse_tree=False):
    parse_root =  parser.parse(code)
    start_ir = None
    if show_parse_tree:
        parser.print_tree(parse_root)
    if parse_root != None and parse_root[0] == 'START':# if start!
       ir_parse.start_ir(parse_root, ir_builder) # the start rule returns an evaluation context
    else:
        print 'Parse Tree root must be START symbol! Parse_root:', parse_root 
    return ir_builder.module;


def main():

    ll1_parser = ll1_load_grammar('grammar.ll1','START', 'EPSILON')    
    argc = len(sys.argv)
    ir_builder = ir_gen.ir_builder()
    ir_engine = ir_gen.ir_engine()

    if argc == 1:  # if only script is called, use as realtime parsing interpter
        input = raw_input('>')

        while input != 'quit': # while quit command is not entered    
            ir_module = generate_module(ir_builder, ll1_parser, input, DEBUG)
            print 'COMPILING...'
            ir_engine.compile(ir_module, 'start.o')
            # Run the start function via ctypes
            func_ptr = ir_engine.get_func_ptr('start')
            cfunc = CFUNCTYPE(c_int)(func_ptr)
            print 'RETURNED: ', cfunc(10)
            input = raw_input(">")
            
    elif argc == 2:  # get_ast file
        source = open(sys.argv[1])
        code = source.read()
        print code[:-1]
        ir_module = generate_module(ir_builder, ll1_parser, code, DEBUG)
        print 'IR MODULE:\n', str(ir_module)
            
    ir_engine.shut_down()
if __name__ == "__main__":
    main()





