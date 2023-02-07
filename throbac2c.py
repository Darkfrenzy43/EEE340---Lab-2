"""
When used as a parse tree Listener on a valid Throbac parse tree, creates a
translation to C for each node and and stores this in the `self.c_translation`
dictionary. The complete program translation will be for the root of the
tree, which is the `ScriptContext` node.

Author: OCdt Aaron Brown and OCdt Liethan Velasco

Version: February 9 2023.
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
        print("\nexitScript")

    def exitFuncDef(self, ctx: ThrobacParser.FuncDefContext):
       print("\nexitFuncDef")

    def exitMain(self, ctx: ThrobacParser.MainContext):
       print("\nexitMain")

    def exitBody(self, ctx: ThrobacParser.BodyContext):
       print("\nexitBody")

    def exitVarDec(self, ctx: ThrobacParser.VarDecContext):
       print("\nexitVarDar")

    def exitNameDef(self, ctx: ThrobacParser.NameDefContext):
       print("\nexitNameDef")

    def exitVarBlock(self, ctx: ThrobacParser.VarBlockContext):
       print("\nexitVarBlock")

    def exitBlock(self, ctx: ThrobacParser.BlockContext):
        print("\nexitBlock")

    def exitAssignment(self, ctx: ThrobacParser.AssignmentContext):
        print("\nexitAssignment")

    def exitWhile(self, ctx: ThrobacParser.WhileContext):
        print("\nexitWhile")

    def exitIf(self, ctx: ThrobacParser.IfContext):
        print("\nExiting exitIf ")

    def exitPrintNumber(self, ctx: ThrobacParser.PrintNumberContext):
        print("\nExiting print number")

    def exitPrintString(self, ctx: ThrobacParser.PrintStringContext):
        print("\nExiting Print String ")

    def exitPrintBool(self, ctx: ThrobacParser.PrintBoolContext):
        print("\nExiting PrintBool ")

    def exitReturn(self, ctx: ThrobacParser.ReturnContext):
        print("\nExiting Return")

    def exitFuncCallStmt(self, ctx: ThrobacParser.FuncCallStmtContext):
        print("\nexitFuncCallStmt")

    def exitParens(self, ctx: ThrobacParser.ParensContext):
        print("\nExiting Parens ")

    def exitNegation(self, ctx: ThrobacParser.NegationContext):
        print("\nExiting Negation ")

    def exitCompare(self, ctx: ThrobacParser.CompareContext):
        print("\nExiting Compare ")

    def exitConcatenation(self, ctx: ThrobacParser.ConcatenationContext):
        print("\nExiting Concatenation")

    def exitBool(self, ctx: ThrobacParser.BoolContext):
        throbac_bool = ctx.getText()
        self.c_translation[ctx] = ("true"
                                   if throbac_bool == "VERUM"
                                   else "false")

    def exitVariable(self, ctx: ThrobacParser.VariableContext):
        print("\nExiting Variable. ")

    def exitAddSub(self, ctx: ThrobacParser.AddSubContext):

        # Retrieve translations of left and right children
        left = self.c_translation[ctx.expr(0)]
        right = self.c_translation[ctx.expr(1)]

        # Greg helped out on this one.
        self.c_translation[ctx] = (f'{left} + {right}'
                                   if ctx.op.text == 'ADDO'
                                   else f'{left} - {right}')

    def exitFuncCallExpr(self, ctx: ThrobacParser.FuncCallExprContext):

        print("\nExiting Func Call Expr. ")

    def exitMulDiv(self, ctx: ThrobacParser.MulDivContext):
        # gets the values of the left and right node
        left = self.c_translation[ctx.expr(0)]
        right = self.c_translation[ctx.expr(1)]

        # Creates the C text
        self.c_translation[ctx] = (f'{left} * {right}'
                                   if ctx.op.text == 'CONGERO'
                                   else f'{left} / {right}')

    def exitFuncCall(self, ctx: ThrobacParser.FuncCallContext):
        #expresionList = [].append(self.c_translation[ctx.expr(n)] for n in ctx.expr())
        # for testing perpous only
        #print(expresionlist)
        #print("\n")
        identifier = ctx.ID()
        expresionStr = ','.join(self.c_translation[ctx.expr(n)] for n in ctx.expr())
        self.c_translation[ctx] = f'{identifier}({expresionStr})'
        print("\nExiting Func Call");
