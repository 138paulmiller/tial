'''github.com/138paulmiller
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS 
OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN 
AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH 
THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
''' 
import sys
from ir import *
from ll1 import * # LL(1) parser 
from ctypes import CFUNCTYPE, c_int

DEBUG = False
# Defines what function will process each tag
# The eval map is used by the context to allow the user to define a function how to evaluate at each given 
# step by just using the contexts eval that will map it to the function   



def generate_module(builder, parser, code, show_parse_tree=False):
    parse_root =  parser.parse(code)
    start_ir = None
    if show_parse_tree:
        parser.print_tree(parse_root)
    if parse_root != None and parse_root[0] == 'START':# if start!
       ir_parse.start_ir(parse_root, builder) # the start rule returns an evaluation context
    else:
        print 'Parse Tree root must be START symbol! Parse_root:', parse_root 
    return builder.module;


def main():

    ll1_parser = ll1_load_grammar('grammar.ll1','START', 'EPSILON')    
    argc = len(sys.argv)
    builder = ir_builder()
    binder = ir_binder()
    module = None
    if argc == 1:  # if only script is called, use as realtime parsing interpter
        input = raw_input('>')

        while input != 'quit': # while quit command is not entered    
            module = generate_module(builder, ll1_parser, input, DEBUG)
            print 'IR:\n', module
            input = raw_input('>')

            
    elif argc == 2:  # get_ast file
        source = open(sys.argv[1])
        code = source.read()
        print code[:-1]
        module = generate_module(builder, ll1_parser, code, DEBUG)
        print 'IR:\n', module

    if module != None:    
        binder.compile(module, sys.argv[1].replace('.tial','.o'))
        # Run the start function via ctypes
        func_ptr = binder.get_func_ptr('start')
        cfunc = CFUNCTYPE(c_int)(func_ptr)
        print 'RETURNED: ', cfunc(10)
            

if __name__ == "__main__":
    main()





