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


def ll1_load_grammar(grammar_filename, start_sym, epsilon_sym):
	# 
	lexemes = []
	rule_map = {}
	file = open(grammar_filename)
	if file != None:
		i = 0
		lines = file.read().split('$') # split each production rule seperated by $
		for line in lines:
			pair = line.split(':=') # split symbol and rule
			if len(pair) == 2:
				symbol = pair[0].strip()
				rule_list = [] 
			 	has_rule = True
			   	for rules in pair[1].split('|'):
			  		rule = []
			  		rules = rules.strip()
			  		if rules[0] == '\'': # parse terminal regex
			 			definition = rules.split('\'')
			 			if len(definition) == 3: # regex literal must be wrapped by single quote
							if symbol.lower().strip() == 'none':
								symbol = None
							lexemes.append((symbol, str(definition[1])))
							has_rule = False
					else:
						for rule_symbol in rules.split(' '):
							if rule_symbol != '':
								rule.append(rule_symbol)
						rule_list.append(rule)
				if has_rule:
					rule_map[symbol] = rule_list
	else:
		print "Could not open Grammar File ", grammar_filename 
		return None

	return  ll1_init(rule_map, start_sym, epsilon_sym, lexemes)
    

