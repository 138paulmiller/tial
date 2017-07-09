'''github.com/138paulmiller
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS 
OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN 
AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH 
THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
''' 
import sys
from ll1 import * # LL(1) parser 


def main():

    ll1_parser = ll1_load_grammar('ex_grammar.ll1','START', 'EPSILON')    
    argc = len(sys.argv)

    if argc == 1:  # if only script is called, use as realtime parsing interpter
        source_code = raw_input('>')

        while source_code != 'quit': # while quit command is not entered    
            parse_root =  ll1_parser.parse(source_code)    
            ll1_parser.print_tree(parse_root)
            source_code = raw_input(">")
            
    elif argc == 2:  # get_ast file
        source = open(sys.argv[1])
        code = source.read()
        print code[:-1]
        parse_root =  ll1_parser.parse(source_code)     
        ll1_parser.print_tree(parse_root)
            
if __name__ == "__main__":
    main()





