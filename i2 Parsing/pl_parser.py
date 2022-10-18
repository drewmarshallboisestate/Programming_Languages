#!/usr/bin/env python

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

    def parseAssn(self):
        id = self.curr()
        self.match('id')
        self.match('=')
        num = self.curr()
        self.match('num')
        node = NodeAssn(id.lex(), num.lex())
        return node

    def parseStmt(self):
        nodeAssn = self.parseAssn()
        node = NodeStmt(nodeAssn)
        return node


    def parseBlock(self):
        nodeStmt = self.parseStmt()
        node = NodeBlock(nodeStmt, 'None')
        if self.curr().lex() == ';':
            self.match(';')
            nodeStmtRepeat = self.parseBlock()
            node = NodeBlock(nodeStmt, nodeStmtRepeat)    
        return node

    def parse(self, program):
        """ generated source for method parse """
        if program == '': return None
        self.scanner = Scanner(program)
        self.scanner.next()
        return self.parseBlock()

