# Generated from /Users/phillips/Sync/courses/EEE340/code/lab 2 start/Throbac.g4 by ANTLR 4.11.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .ThrobacParser import ThrobacParser
else:
    from ThrobacParser import ThrobacParser

# This class defines a complete generic visitor for a parse tree produced by ThrobacParser.

class ThrobacVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by ThrobacParser#script.
    def visitScript(self, ctx:ThrobacParser.ScriptContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThrobacParser#funcDef.
    def visitFuncDef(self, ctx:ThrobacParser.FuncDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThrobacParser#main.
    def visitMain(self, ctx:ThrobacParser.MainContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThrobacParser#body.
    def visitBody(self, ctx:ThrobacParser.BodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThrobacParser#varDec.
    def visitVarDec(self, ctx:ThrobacParser.VarDecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThrobacParser#nameDef.
    def visitNameDef(self, ctx:ThrobacParser.NameDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThrobacParser#varBlock.
    def visitVarBlock(self, ctx:ThrobacParser.VarBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThrobacParser#block.
    def visitBlock(self, ctx:ThrobacParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThrobacParser#assignment.
    def visitAssignment(self, ctx:ThrobacParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThrobacParser#while.
    def visitWhile(self, ctx:ThrobacParser.WhileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThrobacParser#if.
    def visitIf(self, ctx:ThrobacParser.IfContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThrobacParser#printNumber.
    def visitPrintNumber(self, ctx:ThrobacParser.PrintNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThrobacParser#printString.
    def visitPrintString(self, ctx:ThrobacParser.PrintStringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThrobacParser#printBool.
    def visitPrintBool(self, ctx:ThrobacParser.PrintBoolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThrobacParser#return.
    def visitReturn(self, ctx:ThrobacParser.ReturnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThrobacParser#funcCallStmt.
    def visitFuncCallStmt(self, ctx:ThrobacParser.FuncCallStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThrobacParser#number.
    def visitNumber(self, ctx:ThrobacParser.NumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThrobacParser#parens.
    def visitParens(self, ctx:ThrobacParser.ParensContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThrobacParser#negation.
    def visitNegation(self, ctx:ThrobacParser.NegationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThrobacParser#compare.
    def visitCompare(self, ctx:ThrobacParser.CompareContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThrobacParser#concatenation.
    def visitConcatenation(self, ctx:ThrobacParser.ConcatenationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThrobacParser#string.
    def visitString(self, ctx:ThrobacParser.StringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThrobacParser#bool.
    def visitBool(self, ctx:ThrobacParser.BoolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThrobacParser#variable.
    def visitVariable(self, ctx:ThrobacParser.VariableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThrobacParser#addSub.
    def visitAddSub(self, ctx:ThrobacParser.AddSubContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThrobacParser#funcCallExpr.
    def visitFuncCallExpr(self, ctx:ThrobacParser.FuncCallExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThrobacParser#mulDiv.
    def visitMulDiv(self, ctx:ThrobacParser.MulDivContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThrobacParser#funcCall.
    def visitFuncCall(self, ctx:ThrobacParser.FuncCallContext):
        return self.visitChildren(ctx)



del ThrobacParser