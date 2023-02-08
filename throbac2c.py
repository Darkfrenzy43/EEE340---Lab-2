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


    def exitScript(self, ctx: ThrobacParser.ScriptContext):
        # TODO need to test
        funcDefList = [self.c_translation[this_dec] for this_dec in ctx.funcDef()]
        self.c_translation[ctx] = '\n'.join(funcDefList)
        self.c_translation[ctx] += f'{self.c_translation[ctx.main()]}{ctx.EOF()}'


    def exitFuncDef(self, ctx: ThrobacParser.FuncDefContext):

        # Unpack the namedefs
        if ctx.nameDef != None:
            nameDef_list = [self.c_translation[n] for n in ctx.nameDef()];
            nameDef_str = ', '.join(nameDef_list);
        else:
            nameDef_str = '';

        # Get ID token
        this_id = ctx.ID().getText();

        # Get the body translation
        this_body = self.c_translation[ctx.body()];

        # return for TYPE could be none
        if ctx.TYPE() != None:
            this_return = ctx.TYPE().getText();
        else:
            this_return = "void";

        # Setting translation
        self.c_translation[ctx] = f'{this_return} {this_id}({nameDef_str}) > {this_body} <';


    def exitMain(self, ctx: ThrobacParser.MainContext):
        # TODO need to test
        body = "\t".join(self.c_translation[ctx.body()])
        self.c_translation[ctx] = f'int main() {{\n{body}\n\treturn 0;}}'


    def exitBody(self, ctx: ThrobacParser.BodyContext):
        # TODO need to test

        # Unpack varblock and block
        this_vblock = self.c_translation[ctx.varBlock()];
        this_block = self.c_translation[ctx.block()];

        # Set translation
        self.c_translation[ctx] = f'{this_vblock}\n{this_block}';


    def exitVarDec(self, ctx: ThrobacParser.VarDecContext):

        # Finding initial assignment value
        this_type = ctx.nameDef().TYPE().getText();
        ass_str = ("= 0" if this_type == "NUMERUS" else
                   "= NULL" if this_type == "LOCUTIO" else
                   "= false")

        # Getting translation of namedef
        this_nameDef = self.c_translation[ctx.nameDef()];

        # Setting translation
        self.c_translation[ctx] = f'{this_nameDef} {ass_str};';


    def exitNameDef(self, ctx: ThrobacParser.NameDefContext):

        # Getting lexical tokens
        this_id = ctx.ID().getText();
        this_type = ctx.TYPE().getText();

        # Determining strings
        str_id = ('int' if this_type == "NUMERUS" else
                    'char*' if this_type == "LOCUTIO"
                        else 'bool');


        # Setting the translation todo - temporary form
        self.c_translation[ctx] = f'{str_id} {this_id}';


    def exitVarBlock(self, ctx: ThrobacParser.VarBlockContext):
        decList = [self.c_translation[this_dec] for this_dec in ctx.varDec()]
        self.c_translation[ctx] = '\n'.join(decList)


    def exitBlock(self, ctx: ThrobacParser.BlockContext):
        statementList = [self.c_translation[this_statement] for this_statement in ctx.statement()]
        self.c_translation[ctx] = '\n'.join(statementList)


    def exitAssignment(self, ctx: ThrobacParser.AssignmentContext):

        # TODO IDK if this is a legit way to get the ID but it seems to work
        ID = ctx.ID().getText();
        expr = self.c_translation[ctx.expr()]
        self.c_translation[ctx] = f'{ID} = {expr};'


    def exitWhile(self, ctx: ThrobacParser.WhileContext):
        expr = self.c_translation[ctx.expr()]
        block = self.c_translation[ctx.block()]

        # using double { escapes. print('{{') = '{'
        self.c_translation[ctx] = f'while ({expr}) {{\n{block}\n}}'


    def exitIf(self, ctx: ThrobacParser.IfContext):
        expr = self.c_translation[ctx.expr()]
        block1 = self.c_translation[ctx.block(0)]

        self.c_translation[ctx] = f'if ({expr}) {{\n{block1}\n}}'
        # If there is an else statement
        if ctx.block(1) != None:
            block2 = self.c_translation[ctx.block(1)]
            self.c_translation[ctx] = f'{self.c_translation[ctx]} else {{\n{block2}\n}}'


    def exitPrintNumber(self, ctx: ThrobacParser.PrintNumberContext):

        # Retrieving expr value
        this_expr = self.c_translation[ctx.expr()];

        # Setting translation
        self.c_translation[ctx] = f'printf("%d", {this_expr});';


    def exitPrintString(self, ctx: ThrobacParser.PrintStringContext):

        # Retrieving expr value
        this_expr = self.c_translation[ctx.expr()];

        # Setting translation
        self.c_translation[ctx] = f'printf("%s", {this_expr});';


    def exitPrintBool(self, ctx: ThrobacParser.PrintBoolContext):

        # Retrieving expr value
        this_expr = self.c_translation[ctx.expr()]

        # Setting translation
        self.c_translation[ctx] = f'printf("%s", "{this_expr}");';


    def exitReturn(self, ctx: ThrobacParser.ReturnContext):

        # Account for no expr added in return statement
        if ctx.expr() is None:
            self.c_translation[ctx] = f"return;"
        else:
            this_expr = self.c_translation[ctx.expr()]
            self.c_translation[ctx] = f"return {this_expr};"


    def exitFuncCallStmt(self, ctx: ThrobacParser.FuncCallStmtContext):

        # Literally just the function call, but with ';'
        self.c_translation[ctx] = self.c_translation[ctx.funcCall()] + ';';


    def exitParens(self, ctx: ThrobacParser.ParensContext):
        self.c_translation[ctx] = f'({self.c_translation[ctx.expr()]})'


    def exitNegation(self, ctx: ThrobacParser.NegationContext):

        # Getting expr translation
        expr_text = self.c_translation[ctx.expr()]
        this_op = ctx.op.text

        # Do following if op is 'NI':
        if this_op == 'NI':

            # Setting translation as needed
            self.c_translation[ctx] = ("true"
                                       if expr_text == "false"
                                       else "false")

        # Otherwise, do following if op is 'NEGANS':
        elif this_op == 'NEGANS':

            # If translation already negative, return just number portion.
            # If was positive, return number with negative sign.
            self.c_translation[ctx] = (expr_text[1:]
                                       if expr_text[0] == "-"
                                       else "-" + expr_text)


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

        # Literally just the function call
        self.c_translation[ctx] = self.c_translation[ctx.funcCall()];


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
        this_id = ctx.ID().getText()

        # Getting the expressions in a string
        exprList = [self.c_translation[this_expr] for this_expr in ctx.expr()]
        exprStr = ', '.join(exprList)

        # Setting translation
        self.c_translation[ctx] = f'{this_id}({exprStr})'
