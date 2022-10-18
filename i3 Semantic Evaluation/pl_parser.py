#!/usr/bin/env python

from ast import keyword
from pl_syntaxexception import SyntaxException
from pl_node import *
from pl_scanner import Scanner
from pl_token import Token

class Parser(object):
    """ generated source for class Parser """
    def __init__(self):
        self.scanner = None

    def match(self, s):
        """ generated source for method match """
        self.scanner.match(Token(s))

    def curr(self):
        """ generated source for method curr """
        return self.scanner.curr()

    def pos(self):
        """ generated source for method pos """
        return self.scanner.position()


    def parseMulop(self):
        if self.curr() == Token("*"):
            multiply = self.curr()
            self.match("*") 
            return NodeMulop(multiply.lex())
        elif self.curr() == Token("/"):
            divide = self.curr()
            self.match("/")
            return NodeMulop(divide.lex())

    def parseAddop(self):
        if self.curr() == Token("+"):
            plus = self.curr()
            self.match("+")
            return NodeAddop(plus.lex())
        elif self.curr() == Token("-"):
            minus = self.curr()
            self.match("-")
            return NodeAddop(minus.lex())

    def parseFact(self):
        if self.curr() == Token("id"):
            id = self.curr()
            self.match("id") 
            return NodeFact(id.lex(), None, None)
        if self.curr() == Token("num"):
            num = int(self.curr().lex())
            self.match("num")
            return NodeFact(None, num, None)
        if self.curr() == Token("("):
            self.match("(")
            expr = self.parseExpr()
            self.match(")")
            return NodeFact(None, None, expr)

    def parseTerm(self):
        """ generated source for method parseTerm """
        fact = self.parseFact()
        mulop = None
        if self.curr() == Token("*") or self.curr() == Token("/"):
            mulop = self.parseMulop()
        if mulop == None:
            return NodeTerm(fact, None, None)
        term = self.parseTerm()
        term.append(NodeTerm(fact, mulop, None))
        return term
        

    def parseExpr(self):
        """ generated source for method parseExpr """
        term = self.parseTerm()
        addop = None
        if self.curr() == Token("+") or self.curr() == Token("-"):
            addop = self.parseAddop()
        if addop == None:
            return NodeExpr(term, None, None)
        expr = self.parseExpr()
        expr.append(NodeExpr(term, addop, None))
        return expr
        

    def parseAssn(self):
        """ generated source for method parseAssn """
        id = self.curr()
        self.match("id")
        self.match("=")
        expr = self.parseExpr()
        assn = NodeAssn(id.lex(), expr)
        return assn

    def parseWr(self):
        self.match("wr")
        expr = self.parseExpr()
        return NodeWr(expr)

    def parseStmt(self):
        """ generated source for method parseStmt """
        value = self.curr()
        if value == Token("wr"):
            wr = self.parseWr()
            return NodeStmt(wr)
        if value == Token("id"):
            assn = self.parseAssn()
            return NodeStmt(assn)
        

        return None

    def parseBlock(self):
        """ generated source for method parseBlock """
        stmt = self.parseStmt()
        rest = None
        if self.curr() == Token(";"):
            self.match(";")
            rest = self.parseBlock()
        block = NodeBlock(stmt, rest)
        return block


    def parse(self, program):
        """ generated source for method parse """
        if program == '': return None
        self.scanner = Scanner(program)
        self.scanner.next()
        return self.parseBlock()

