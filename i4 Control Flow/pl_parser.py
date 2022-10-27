#!/usr/bin/env python

from pickle import NONE
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
        """ generated source for method parseMulop """
        if self.curr() == Token("*"):
            self.match("*")
            return NodeMulop(self.pos(), "*")
        if self.curr() == Token("/"):
            self.match("/")
            return NodeMulop(self.pos(), "/")
        return None

    def parseAddop(self):
        """ generated source for method parseAddop """
        if self.curr() == Token("+"):
            self.match("+")
            return NodeAddop(self.pos(), "+")
        if self.curr() == Token("-"):
            self.match("-")
            return NodeAddop(self.pos(), "-")
        return None

    def parseFact(self):
        """ generated source for method parseFact """
        if self.curr() == Token("("):
            self.match("(")
            expr = self.parseExpr()
            self.match(")")
            return NodeFactExpr(expr)
        if self.curr() == Token("-"):
            self.match("-")
            fact = self.parseFact()
            return NodeFactFact(fact)
        if self.curr() == Token("id"):
            nid = self.curr()
            self.match("id")
            return NodeFactId(self.pos(), nid.lex())
        num = self.curr()
        self.match("num")
        return NodeFactNum(num.lex())

    def parseTerm(self):
        """ generated source for method parseTerm """
        fact = self.parseFact()
        mulop = self.parseMulop()
        if mulop == None:
            return NodeTerm(fact, None, None)
        term = self.parseTerm()
        term.append(NodeTerm(fact, mulop, None))
        return term

    def parseExpr(self):
        """ generated source for method parseExpr """
        term = self.parseTerm()
        addop = self.parseAddop()
        if addop == None:
            return NodeExpr(term, None, None)
        expr = self.parseExpr()
        expr.append(NodeExpr(term, addop, None))
        return expr

    def parseAssn(self):
        """ generated source for method parseAssn """
        nid = self.curr()
        self.match("id")
        self.match("=")
        expr = self.parseExpr()
        assn = NodeAssn(nid.lex(), expr)
        return assn

    def parseWr(self):
        """ generated source for method parseWr """
        self.match("wr")
        expr = self.parseExpr()
        wr = NodeWr(expr)
        return wr
    
    def parseRd(self):
        """ generated source for method parseRd """
        self.match("rd")
        _id = self.curr()
        self.match("id")
        return NodeRd(_id.lex())

    def parseBegin(self):
        """ generated source for method parseBegin"""
        self.match("begin")
        block = self.parseBlock()
        self.match("end")
        return NodeBeginEnd(block)

    def parseIf(self):
        """ generated source for method parseIf """
        self.match("if")
        boolExpr = self.parseBoolExpr()
        self.match("then")
        stmt = self.parseStmt()
        stmt2 = NONE
        if self.curr() == Token("else"):
            self.match("else")
            stmt2 = self.parseStmt()
        return NodeIf(boolExpr, stmt, stmt2)

    def parseWhile(self):
        """ generated source for method parseWhile """
        self.match("while")
        boolExpr = self.parseBoolExpr()
        self.match("do")
        stmt = self.parseStmt()
        return NodeWhile(boolExpr, stmt)

    def parseBoolExpr(self):
        """ generated source for method parseBoolExpr """
        exprOne = self.parseExpr()
        relop = self.parseRelop()
        exprTwo = self.parseExpr()
        return NodeBoolExpr(exprOne, relop, exprTwo)

    def parseRelop(self):
        """ generated source for method parseRelop """
        if self.curr() == Token("<"):
            self.match("<")
            return NodeRelop(self.pos(), "<")  
        if self.curr() == Token("<="):
            self.match("<=")
            return NodeRelop(self.pos(), "<=")
        if self.curr() == Token(">="):
            self.match(">=")
            return NodeRelop(self.pos(), ">=")
        if self.curr() == Token(">"):
            self.match(">")
            return NodeRelop(self.pos(), ">")
        if self.curr() == Token("=="):
            self.match("==")
            return NodeRelop(self.pos(), "==")
        if self.curr() == Token("<>"):
            self.match("<>")
            return NodeRelop(self.pos(), "<>")

    def parseStmt(self):
        """ generated source for method parseStmt """
        if self.curr() == Token("wr"):
            wr = self.parseWr()
            return NodeStmt(wr)
        if self.curr() == Token("rd"):
            rd = self.parseRd()
            return NodeStmt(rd) 
        if self.curr() == Token("begin"):
            begin = self.parseBegin()
            return NodeStmt(begin);        
        if self.curr() == Token("if"):
            _if = self.parseIf()
            return NodeStmt(_if)
        if self.curr() == Token("while"):
            _while = self.parseWhile()
            return NodeStmt(_while)
        if self.curr() == Token("id"):
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
        #if not self.scanner.done(): 
        #    raise SyntaxException(self.pos, self.curr(), 'end')
        block = NodeBlock(stmt, rest)
        return block


    def parse(self, program):
        """ generated source for method parse """
        self.scanner = Scanner(program)
        self.scanner.next()
        return self.parseBlock()

