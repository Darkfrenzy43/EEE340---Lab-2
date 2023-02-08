"""
When used as a parse tree Listener on a valid Throbac parse tree, creates a
translation to C for each node and and stores this in the `self.c_translation`
dictionary. The complete program translation will be for the root of the
tree, which is the `ScriptContext` node.

Author: OCdt Aaron Brown and OCdt Liethan Velasco

Notes:
    - check in with prof about zero-terminated strings. The code
    that was given to us does not utilize them at all. 

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

        # TODO Don't we want to put a zero terminator here? ^^

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
        ID = ctx.ID()
        expr = self.c_translation[ctx.expr()]
        self.c_translation[ctx] = f'{ID} = {expr};'

    def exitWhile(self, ctx: ThrobacParser.WhileContext):
        expr = self.c_translation[ctx.expr()]
        block = self.c_translation[ctx.block()]

        # using double { escapes. print('{{') = '{'
        self.c_translation[ctx] = f'while ({expr}) {{\n{block}\n}}'

    def exitIf(self, ctx: ThrobacParser.IfContext):
        print("\nExiting exitIf ")

    def exitPrintNumber(self, ctx: ThrobacParser.PrintNumberContext):
        print("\nExiting print number")

    def exitPrintString(self, ctx: ThrobacParser.PrintStringContext):
        print("\nExiting Print String ")

    def exitPrintBool(self, ctx: ThrobacParser.PrintBoolContext):

        # Retrieving expr value
        this_expr = self.c_translation[ctx.expr()];

        StrResult = "true" if this_expr == "true" else "false";

        # Setting translation
        self.c_translation[ctx] = f'printf("%s", "{StrResult}");';

    def exitReturn(self, ctx: ThrobacParser.ReturnContext):

        # Account for no expr added in return statement
        if ctx.expr() is None:
            self.c_translation[ctx] = f"return;"
        else:
            this_expr = self.c_translation[ctx.expr()];
            self.c_translation[ctx] = f"return {this_expr};"

    def exitFuncCallStmt(self, ctx: ThrobacParser.FuncCallStmtContext):
        print("\nexitFuncCallStmt")

    def exitParens(self, ctx: ThrobacParser.ParensContext):
        self.c_translation[ctx] = f'({self.c_translation[ctx.expr()]})'

    def exitNegation(self, ctx: ThrobacParser.NegationContext):

        # Getting expr translation
        expr_text = self.c_translation[ctx.expr()];
        this_op = ctx.op.text;

        # Do following if op is 'NI':
        if this_op == 'NI':

            # Setting translation as needed
            self.c_translation[ctx] = ("true"
                                       if expr_text == "false"
                                       else "false");

        # Otherwise, do following if op is 'NEGANS':
        elif this_op == 'NEGANS':

            # If translation already negative, return just number portion.
            # If was positive, return number with negative sign.
            self.c_translation[ctx] = (expr_text[1:]
                                       if expr_text[0] == "-"
                                       else "-" + expr_text);

    def exitCompare(self, ctx: ThrobacParser.CompareContext):
        # Might need to check if it is a number first
        # i.e. type NUMERUS
        left = self.c_translation[ctx.expr(0)]
        right = self.c_translation[ctx.expr(1)]

        # IDK if is this is really a cleaner way to do it ¯\_(ツ)_/¯
        self.c_translation[ctx] = (f'{left} == {right}'
                                   if ctx.op.text == 'IDEM'
                                   else (f'{left} != {right}'
                                         if ctx.op.text == 'NI.IDEM'
                                         else (f'{left} < {right}'
                                               if ctx.op.text == 'INFRA'
                                               else (f'{left} <= {right}'
                                                     if ctx.op.text == 'INFRA.IDEM'
                                                     else (f'{left} > {right}'
                                                           if ctx.op.text == 'SUPRA'
                                                           else f'{left} >= {right}')))))

    def exitConcatenation(self, ctx: ThrobacParser.ConcatenationContext):

        """

        # Extracting child expressions. They're not zero-terminated though??
        left_expr = self.c_translation[ctx.expr(0)];
        right_expr = self.c_translation[ctx.expr(1)];

        # Concatenating and setting translation.
        # Don't forget to account for the inner quotations and ZERO-TERMINATORS???
        self.c_translation[ctx] = left_expr[:-1] + right_expr[1:-1] + '"';

        """


        left = self.c_translation[ctx.expr(0)]
        right = self.c_translation[ctx.expr(1)]
        self.c_translation[ctx] = f'__throbac_cat({left}, {right})'

    def exitBool(self, ctx: ThrobacParser.BoolContext):
        throbac_bool = ctx.getText()
        self.c_translation[ctx] = ("true"
                                   if throbac_bool == "VERUM"
                                   else "false")

    def exitVariable(self, ctx: ThrobacParser.VariableContext):
        self.c_translation[ctx] = ctx.getText()

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

        # ID IS A LEXICAL TOKEN! DOESN'T HAVE A C_TRANSLATION??
        this_id = ctx.ID().getText();

        # Getting the expressions in a string
        exprList = [self.c_translation[this_expr] for this_expr in ctx.expr()];
        exprStr = ', '.join(exprList);

        # Setting translation
        self.c_translation[ctx] = f'{this_id}({exprStr})';
