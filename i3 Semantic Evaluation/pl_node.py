#!/usr/bin/env python
""" generated source for module Node """

#  (C) 2013 Jim Buffenbarger
#  All rights reserved.
from pl_evalexception import EvalException
# from pl_parser import expr


class Node(object):
    """ generated source for class Node """
    pos = 0

    def __str__(self):
        """ generated source for method toString """
        result = ""
        result += str(self.__class__.__name__)
        result += " ( "
        fields = self.__dict__
        for field in fields:
            result += "  "
            result += str(field)
            result += str(": ")
            result += str(fields[field])
        result += str(" ) ")
        return result

    def eval(self, env):
        """ generated source for method eval """
        raise EvalException(self.pos, "cannot eval() node!")

class NodeAssn(Node):
    """ generated source for class NodeAssn """

    def __init__(self, id, expr):
        """ generated source for method __init__ """
        super(NodeAssn, self).__init__()
        self.id = id
        self.expr = expr
 
    def eval(self, env):
        """ generated source for method eval """
        return env.put(self.id, self.expr.eval(env))
    

class NodeBlock(Node):
    """ generated source for class NodeBlock """

    def __init__(self, stmt, block):
        """ generated source for method __init__ """
        super(NodeBlock, self).__init__()
        self.stmt = stmt
        self.block = block

    def eval(self, env):
        r = self.stmt.eval(env)
        if self.block is not None:
            r = self.block.eval(env)
        return r

class NodeStmt(Node):
    """ generated source for class NodeStmt """

    def __init__(self, stmt):
        """ generated source for method __init__ """
        super(NodeStmt, self).__init__()
        self.stmt = stmt

    def eval(self, env):
        return self.stmt.eval(env)
        

class NodeWr(Node):
    """ generated source for class NodeWr """

    def __init__(self, expr):
        """ generated source for method __init__ """
        super(NodeWr, self).__init__()
        self.expr = expr

    def eval(self, env):
        val =  self.expr.eval(env)
        print(val)
        return val

class NodeExpr(Node):
    """ generated source for class NodeExpr """
    
    def __init__(self, term, addop, expr):
        """ generated source for method __init__ """
        super(NodeExpr, self).__init__()
        self.term = term
        self.addop = addop
        self.expr = expr

    def append(self, expr):
        if self.expr is None:
            self.addop = expr.addop
            self.expr = expr
            expr.addop = None
        else:
            self.expr.append(expr)

    def eval(self, env):
        t = self.term.eval(env)
        if self.addop is not None:
            op = self.addop.eval(env)
            if op == "+":
                t = t + self.expr.eval(env)
            elif op == "-":
                t = self.expr.eval(env) - t 
        return t
   

class NodeAddop(Node):
    """ generated source for class NodeAddop """

    def __init__(self, operator):
        super(NodeAddop, self).__init__()
        self.operator = operator

    def eval(self, env):
        return self.operator

class NodeMulop(Node):
    """ generated source for class NodeAddop """

    def __init__(self, operator):
        super(NodeMulop, self).__init__()
        self.operator = operator

    def eval(self, env):
        return self.operator
        

class NodeTerm(Node):
    """ generated source for class NodeTerm """

    def __init__(self, fact, mulop, term):
        super(NodeTerm, self).__init__()
        self.fact = fact
        self.mulop = mulop
        self.term = term
        

    def append(self, term):
        if self.term is None:
            self.mulop = term.mulop
            self.term = term
            term.mulop = None
        else:
            self.term.append(term)
            
    #     #return the child env.term and then check if mulop is not none
    #     #then gets the next env.term and does the calculation
    def eval(self, env):
        f = self.fact.eval(env)
        if self.mulop is not None:
            op = self.mulop.eval(env)
            if op == "*":
                f = f * self.term.eval(env)
            elif op == "/":
                f = self.term.eval(env) / f
        return f

class NodeFact(Node):
    """ generated source for class NodeFact """
    def __init__(self, id, num, expr):
        super(NodeFact, self).__init__()
        self.id = id
        self.num = num 
        self.expr = expr

    def eval(self, env):
        if self.id is not None:
            
            val = env.get(self.pos, self.id)
            #val = env.get(self.pos, self.id)
        if self.num is not None:
            val = self.num
        if self.expr is not None:
            val = self.expr.eval(env)
        return val


