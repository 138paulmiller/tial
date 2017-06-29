import grammar
import evaluator
# Defines what function will process each tag
eval_map = {
			grammar.START 	: evaluator.eval_start,
			grammar.BODY 	: evaluator.eval_body,
			grammar.STMT 	: evaluator.eval_stmt,
			grammar.EXPR  	: evaluator.eval_expr,
			grammar.EXPR_OP : evaluator.eval_expr_op, 
			grammar.TERM 	: evaluator.eval_term,
			grammar.TERM_OP : evaluator.eval_term_op,
			grammar.FACTOR 	: evaluator.eval_factor
			}