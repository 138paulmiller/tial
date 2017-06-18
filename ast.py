# Paul Miller 2016
# All rights reserved


# Parse tree node definitions that define the Abstract Syntax Tree
# Expression is the base node inherited by all internal nodes in ast. 
# Each expression is superceded by inherited class which defines following grammer.
# All expressions contain tags to identify the superceded class.
# __repr__ is the overridden method used by parser 
class Expr:
    def __init__(self):
        self.tag = None
        return

# Error 
# Expression returned 
class ErrorExpr(Expr):
    def __init__(self, value, tag="ERROR"):
        self.value = value
        self.tag = tag

    def __repr__(self):
        return "Error(%s)" % self.value


class IntExpr(Expr):  # integer ast node
    def __init__(self, value, tag='INT'):
        self.value = value
        self.tag = tag

    def __repr__(self):
        return "Int(%d)" % int(self.value)


class IdentifierExpr(Expr):  # variable ast node
    def __init__(self, value, tag='ID'):
        self.value = value
        self.tag = tag

    def __repr__(self):
        return "Id(%s)" % self.value


class StringExpr(Expr):  # string ast node
    def __init__(self, value, tag='STRING'):
        self.value = value
        self.tag = tag

    def __repr__(self):
        return "String(%s)" % self.value

class OperatorExpr(Expr):  # operator ast node
    def __init__(self, value, tag='OPERATOR'):
        self.value = value
        self.tag = tag

    def __repr__(self):
        return "Op(%s)" % self.value


class ArithmeticExpr(Expr):
    def __init__(self, left, op, right, tag='ARITHMETIC'):
        self.op = op
        self.left = left
        self.right = right
        self.tag = tag

    def __repr__(self):
        return "[ArithmeticExpr(%s %s %s)]" % (self.left, self.op, self.right)


# base class for boolean expressions
class BoolExpr(Expr):
    pass


# relational expr such as x < y.
class RelationalExpr(BoolExpr):
    def __init__(self, left, op, right, tag='RELATIONAL'):
        self.op = op
        self.left = left
        self.right = right
        self.tag = tag

    def __repr__(self):
        return "[RelationalExpr(%s %s %s)]" % (self.left, self.op, self.right)


# statements are the base case for combined expressions
class Statement:
    def __init__(self):
        return


class AssignStatement(Statement):
    def __init__(self, name, expr, tag='ASSIGN'):
        self.name = name
        self.expr = expr
        self.tag = tag

    def __repr__(self):
        return "[AssignStmt(%s = %s)]" % (self.name, self.expr)


class IfStatement(Statement):
    def __init__(self, boolean_expr, true_statement, false_statement, tag = 'IF'):
        self.boolean_expr = boolean_expr
        self.true_statement = true_statement
        self.false_statement = false_statement
        self.tag = tag


    def __repr__(self):
        return "[IfStmt(%s: \n\t%s Else:\n\t%s)]" % (self.boolean_expr, self.true_statement, self.false_statement)


class WhileStatement(Statement):
    def __init__(self, boolean_expr, body, tag = 'WHILE'):
        self.boolean_expr = boolean_expr
        self.body = body
        self.tag = tag


    def __repr__(self):
        return "[WhileStmt(%s :%s)]" % (self.boolean_expr, self.body)
