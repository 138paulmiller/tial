'''github.com/138paulmiller
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS 
OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN 
AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH 
THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
''' 


'''LL(1) Parser 
- Uses a grammer map such that each symbol maps to a list of production rules.
  Each rule is an in order list of terminal and nonterminals.
  Terminals are token tags that do not exist as a key in the grammer map. 
  
- Symbols : the tag used to identify token tags(terminals) and rule tags (nonterminals)
   
'''
import log 
import parser
import parse_table

__all__ = ['log', 'parser', 'parse_table']