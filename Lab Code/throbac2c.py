"""
When used as a parse tree Listener on a valid Throbac parse tree, creates a
translation to C for each node and and stores this in the `self.c_translation`
dictionary. The complete program translation will be for the root of the
tree, which is the `ScriptContext` node.

Author: TODO: your names here

Version: TODO: submission date here
"""

from throbac.ThrobacListener import ThrobacListener
from throbac.ThrobacParser import ThrobacParser

DIGIT_MAP = {'NIL': '0', 'I': '1', 'II': '2', 'III': '3', 'IV': '4',
             'V': '5', 'VI': '6', 'VII': '7', 'VIII': '8', 'IX': '9'}


def c_block(node):
    """
    Given a parse tree node with a .c attribute, surrounds the text of the .c
    attribute with curly braces and indents each line by four spaces.
    """
    if node.c:
        lines = node.c.split('\n')
        indented_lines = [('    ' + line).rstrip() for line in lines]
        block = ('\n'.join(indented_lines))
        return f'{{\n{block}\n}}'
    else:
        return '{\n}'


class Throbac2CTranslator(ThrobacListener):

    def __init__(self):
        self.c_translation = {}

    # --- provided for you

    def exitNumber(self, ctx: ThrobacParser.NumberContext):
        throbac_number = ctx.getText()
        throbac_digits = throbac_number.strip('.').split('.')
        c_digits = [DIGIT_MAP[td] for td in throbac_digits]
        number = ''.join(c_digits)
        # str(int(...)) removes leading zeroes, since C doesn't permit them
        self.c_translation[ctx] = str(int(number))

    def exitString(self, ctx: ThrobacParser.StringContext):
        throbac = ctx.getText()
        c_with_pluses = f'"{throbac.strip("^")}"'
        self.c_translation[ctx] = c_with_pluses.replace('+', r'\n')  # note the raw string

    # --- TODO: yours to provide (not in this order - see `testcases.py`)

    def exitScript(self, ctx: ThrobacParser.ScriptContext):
        pass

    def exitFuncDef(self, ctx: ThrobacParser.FuncDefContext):
        pass

    def exitMain(self, ctx: ThrobacParser.MainContext):
        pass

    def exitBody(self, ctx: ThrobacParser.BodyContext):
        pass

    def exitVarDec(self, ctx: ThrobacParser.VarDecContext):
        pass

    def exitNameDef(self, ctx: ThrobacParser.NameDefContext):
        pass

    def exitVarBlock(self, ctx: ThrobacParser.VarBlockContext):
        pass

    def exitBlock(self, ctx: ThrobacParser.BlockContext):
        pass

    def exitAssignment(self, ctx: ThrobacParser.AssignmentContext):
        pass

    def exitWhile(self, ctx: ThrobacParser.WhileContext):
        pass

    def exitIf(self, ctx: ThrobacParser.IfContext):
        pass

    def exitPrintNumber(self, ctx: ThrobacParser.PrintNumberContext):
        pass

    def exitPrintString(self, ctx: ThrobacParser.PrintStringContext):
        pass

    def exitPrintBool(self, ctx: ThrobacParser.PrintBoolContext):
        pass

    def exitReturn(self, ctx: ThrobacParser.ReturnContext):
        pass

    def exitFuncCallStmt(self, ctx: ThrobacParser.FuncCallStmtContext):
        pass

    def exitParens(self, ctx: ThrobacParser.ParensContext):
        pass

    def exitNegation(self, ctx: ThrobacParser.NegationContext):
        pass

    def exitCompare(self, ctx: ThrobacParser.CompareContext):
        pass

    def exitConcatenation(self, ctx: ThrobacParser.ConcatenationContext):
        pass

    def exitBool(self, ctx: ThrobacParser.BoolContext):
        pass

    def exitVariable(self, ctx: ThrobacParser.VariableContext):
        pass

    def exitAddSub(self, ctx: ThrobacParser.AddSubContext):
        pass

    def exitFuncCallExpr(self, ctx: ThrobacParser.FuncCallExprContext):
        pass

    def exitMulDiv(self, ctx: ThrobacParser.MulDivContext):
        pass

    def exitFuncCall(self, ctx: ThrobacParser.FuncCallContext):
        pass
