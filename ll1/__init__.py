'''github.com/138paulmiller
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS 
OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN 
AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH 
THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
''' 


import log 
import parser
import parse_table
'''
 LL1 Init 
   Initalizes and returns a ll1 parser 
	grammar - 
	start_sym - the tag for the symbol in grammer used as start
	epsilon_sym the tag symbol in grammer used as epsilon 
	
	token_definitions - define the terminal symbols used in grammer, the individual tokens
						the parser will try to match in input string 
'''
def ll1_init(grammar, start_sym, epsilon_sym, token_definitions):
	table = parse_table.ll1_parse_table(grammar, start_sym, epsilon_sym)
	return parser.ll1_parser(token_definitions, table) # create ll1 parser from token_definitions ll1 table


