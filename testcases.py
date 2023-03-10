"""
Test cases for the Throbac to C transpiler

Author: OCdt Aaron Brown and OCdt Liethan Velasco

Version: February 8 2023
"""

import unittest

import generic_parser
from antlr4 import ParseTreeWalker
from throbac.ThrobacLexer import ThrobacLexer
from throbac.ThrobacParser import ThrobacParser
from throbac2c import Throbac2CTranslator


def as_c(source, start_rule):
    """
    Translates the given Throbac source string to C, using start_rule for parsing.
    """
    parse_tree = generic_parser.parse(source, start_rule, ThrobacLexer, ThrobacParser)
    walker = ParseTreeWalker()
    translator = Throbac2CTranslator()
    walker.walk(translator, parse_tree)
    if parse_tree in translator.c_translation:
        return translator.c_translation[parse_tree]
    else:
        return 'No generated C found'


"""
 `TEST_CASES` is a list of triples, where the first element is the expected
 C equivalent, the second is the Throbac source, and the third is the parser
 rule to be used to parse the Throbac. These are intended to be processed by
 the `test_all_cases` method in the `TranslationTest` class below.
 
For complex tests you may wish to write separate test cases, rather than using
the `TEST_CASES` approach.

The comments in `TEST_CASES` suggest a reasonable order in which to proceed with
implementation of your `Throbac2CTranslator`.
 """

TEST_CASES = [

    # numbers
    ('0', '.NIL.', 'expr'),
    ('7', '.NIL.NIL.VII.', 'expr'),  # trim leading zeroes
    ('1234567890', '.I.II.III.IV.V.VI.VII.VIII.IX.NIL.', 'expr'),


    # strings
    ('"HELLO.WORLD"', '^HELLO.WORLD^', 'expr'),
    ('""', '^^', 'expr'),
    (r'"YO\nYOYO\n\n"', '^YO+YOYO++^', 'expr'),  # Note the use of raw string to permit \n
    (r'"\n"', '^+^', 'expr'),
    # alternative would have been '"YO\\nYOYO\\n\\n"'


    # booleans
    ('true', 'VERUM', 'expr'),
    ('false', 'FALSUM', 'expr'),


    # variables
    ('test', 'test', 'expr'),
    ('somevar', 'somevar', 'expr'),
    ('abcdefghijklmnopqrstuvwxyz', 'abcdefghijklmnopqrstuvwxyz', 'expr'),


    # parentheses
    ('(6)', '(   .VI.      )', 'expr'),
    ('(true)', '(  VERUM  )', 'expr'),
    ('(false)', '(FALSUM )', 'expr'),
    ('(6 * 8)', '(.VI.     CONGERO .VIII.)', 'expr'),
    ('("HELLOWORLD")', '(^HELLOWORLD^)', 'expr'),
    ('(6 < 8 + 3)', '(.VI. INFRA .VIII. ADDO .III.)', 'expr'),


    # concatenation
    ('__throbac_cat("HELLO.WORLD", "ISHERE")', '^HELLO.WORLD^ IUNGO ^ISHERE^', 'expr'),
    ('__throbac_cat(__throbac_cat("WHYARE", "YOU"), "SCREAMING.\\nSTOP.")',
     '^WHYARE^ IUNGO ^YOU^ IUNGO ^SCREAMING.+STOP.^', 'expr'),
    (r'__throbac_cat(message, "\n")', 'message IUNGO ^+^ ', 'expr'),
    ('__throbac_cat("HELLO", "WORLD")', '^HELLO^ IUNGO ^WORLD^', 'expr'),


    # compare
    ('20 == 75', '.II.NIL. IDEM .VII.V.', 'expr'),
    ('31 != 23', '.III.I. NI.IDEM .II.III.', 'expr'),
    ('49 < 28', '.IV.IX. INFRA .II.VIII.', 'expr'),
    ('39 <= 1', '.III.IX. INFRA.IDEM .I.', 'expr'),
    ('5 > 87', '.V. SUPRA .VIII.VII.', 'expr'),
    ('12 >= 2', '.I.II. SUPRA.IDEM .II.', 'expr'),
    ('9 > 10', '.IX. SUPRA .I.NIL.', 'expr'),


    # add and subtract
    ('somevar + b', 'somevar ADDO b', 'expr'),
    ('2 + 16', '.II. ADDO .I.VI.', 'expr'),


    # multiply and divide
    ('8 * 13', '.VIII. CONGERO .I.III.', 'expr'),
    ('5 / 9', '.V. PARTIO .IX.', 'expr'),


    # negation
    ('!(false)', 'NI FALSUM', 'expr'),
    ('!(!(!(true)))', 'NI NI NI VERUM', 'expr'),
    ('!(!(!(!(!(false)))))', 'NI NI NI NI NI FALSUM', 'expr'),
    ('-7', 'NEGANS .NIL.NIL.VII.', 'expr'),
    ('-(-7)', 'NEGANS NEGANS .NIL.NIL.VII.', 'expr'),


    # function call
    ('countdown(10, announce)', 'APUD .I.NIL., announce VOCO countdown', 'funcCall'),
    ('substring("HELLO.WORLD\\n", 0, 5)', 'APUD ^HELLO.WORLD+^, .NIL., .V. VOCO substring', 'funcCall'),
    ('outer(inner(first, second), fourth + fifth)', 'APUD APUD first, second VOCO inner, fourth ADDO fifth VOCO outer', 'funcCall'),


    # function call expression
    ('outerfunc(countdown(10, announce)) + 1',
     'APUD APUD .I.NIL., announce VOCO countdown VOCO outerfunc ADDO .I.', 'expr'),
    ('cantstopthefunc(77 + 192) > 3', 'APUD .VII.VII. ADDO .I.IX.II. VOCO cantstopthefunc SUPRA .III.', 'expr'),


    # function call statement
    ('countdown(10, announce);', 'APUD .I.NIL., announce VOCO countdown', 'statement'),
    ('testfunc(true);', 'APUD VERUM VOCO testfunc', 'statement'),


    # assignment
    ('current = start;', 'current start VALORUM', 'statement'),
    ('x = 32;', 'x .III.II. VALORUM', 'statement'),
    ('string = "HELLO";', 'string ^HELLO^ VALORUM', 'statement'),
    ('current = start;', 'current start VALORUM', 'statement'),
    ('x = 32;', 'x .III.II. VALORUM', 'statement'),
    ('string = "HELLO";', 'string ^HELLO^ VALORUM', 'statement'),


    # return
    ('return count;', 'count REDEO', 'statement'),
    ('return 20 == 75;', '.II.NIL. IDEM .VII.V. REDEO', 'statement'),
    ('return "SOMESTRING";', '^SOMESTRING^ REDEO', 'statement'),
    ('return;', ' REDEO', 'statement'),
    ('return;', 'REDEO', 'statement'),
    ('return count;', 'count REDEO', 'statement'),
    ('return 84;', '.VIII.IV. REDEO', 'statement'),
    ('return 43 * 16;', '.IV.III. CONGERO .I.VI. REDEO', 'statement'),


    # print int
    ('printf("%d", 20);', '.II.NIL. NUMERUS.IMPRIMO', 'statement'),
    ('printf("%d", 70 + 2);', '.VII.NIL. ADDO .II. NUMERUS.IMPRIMO', 'statement'),
    ('printf("%d", 1234567890 * 3);', '.I.II.III.IV.V.VI.VII.VIII.IX.NIL. CONGERO .III. NUMERUS.IMPRIMO', 'statement'),


    # print string
    ('printf("%s", "SOMESTR");', '^SOMESTR^ LOCUTIO.IMPRIMO', 'statement'),
    ('printf("%s", __throbac_cat("STR", "ING"));', '^STR^ IUNGO ^ING^ LOCUTIO.IMPRIMO', 'statement'),


    # print bool
    ('printf("%s", "true");', 'VERUM VERITAS.IMPRIMO', 'statement'),
    ('printf("%s", "!(true)");', 'NI VERUM VERITAS.IMPRIMO', 'statement'),
    ('printf("%s", "!(!(false))");', 'NI NI FALSUM VERITAS.IMPRIMO', 'statement'),

    #
    # # block
    # ('printf("%s", "HELLOWORLD");\nreturn 2;', '^HELLOWORLD^ LOCUTIO.IMPRIMO .II. REDEO', 'block'),
    # ('var = "HELLO";\nreturn 77 + 6;', 'var ^HELLO^ VALORUM .VII.VII. ADDO .VI. REDEO', 'block'),
    # ('', '', 'block'),
    #
    #
    # # while
    # ('while (current > 0) {\n\tcurrent = displayanddecrement(current);\n}',
    #  'current SUPRA .NIL. DUM >\ncurrent APUD current VOCO displayanddecrement VALORUM\n<', 'statement'),
    # ('while (x > 10) {\n\tx = x + 2;\n}', 'x SUPRA .I.NIL. DUM >x x ADDO .II. VALORUM<', 'statement'),
    # ('while (true) {\n\twhile (true) {\n\t\twhile (true) {\n\t\t\tprintf("%s", "true");\n\t\t}\n\t}\n}', 'VERUM DUM > VERUM DUM > VERUM DUM > VERUM VERITAS.IMPRIMO < < <', 'statement'),
    #
    #
    # # if
    # ('if (count == 3) {\n\tprintf("%s", "\\nGET.READY\\n");\n} else {\n\tprintf("%s", "\\n");\n}',
    #  'count IDEM .III. SI >\n^+GET.READY+^ LOCUTIO.IMPRIMO\n< ALUID >^+^ LOCUTIO.IMPRIMO\n<', 'statement'),
    # ('if (test >= x) {\n\treturn test;\n} else {\n\treturn x;\n}',
    #  'test SUPRA.IDEM x SI >test REDEO< ALUID >x REDEO<', 'statement'),
    # ('if (false) {\n\tless = 10 + 10;\n}', 'FALSUM SI >less .I.NIL. ADDO .I.NIL. VALORUM<', 'statement'),
    #
    #
    # # nameDef
    # ('int anid', 'anid : NUMERUS', 'nameDef'),
    # ('bool anbooleanyep', 'anbooleanyep : VERITAS', 'nameDef'),
    # ('char* somethingcool', 'somethingcool : LOCUTIO', 'nameDef'),
    #
    #
    # # varDec
    # ('int someint = 0;', 'someint : NUMERUS MUTABILIS', 'varDec'),
    # ('char* somestr = NULL;', 'somestr : LOCUTIO MUTABILIS', 'varDec'),
    # ('bool somebool = false;', 'somebool : VERITAS MUTABILIS', 'varDec'),
    #
    #
    # # varBlock
    # ('int someint = 0;\nchar* somestr = NULL;', 'someint : NUMERUS MUTABILIS somestr : LOCUTIO MUTABILIS', 'varBlock'),
    # ('', '', 'varBlock'),
    #
    #
    # # body
    # ('int testint = 0;\ntestint = 30;\nreturn;', 'testint : NUMERUS MUTABILIS testint .III.NIL. VALORUM REDEO', 'body'),
    # ('', '', 'body'),
    #
    #
    # # main
    # ('int main() {\n\tint testint = 0;\n\ttestint = 30;\n\treturn;\n}',
    #  'testint : NUMERUS MUTABILIS testint .III.NIL. VALORUM REDEO', 'main'),
    # ('int main() {\n\tint testint = 0;\n\ttestint = 30;\n\treturn 0;\n}',
    #  'testint : NUMERUS MUTABILIS testint .III.NIL. VALORUM', 'main'),
    # ('', '', 'main'),
    #
    #
    # # funcdef
    # ('void countdown(int start, char* message) {\n\treturn count;\n}',
    #  'APUD start : NUMERUS, message : LOCUTIO DEFINITIO countdown > count REDEO <', 'funcDef'),
    # (('void countdown(int start, char* message) {\n\tint current = 0;\n\tcurrent = start;'
    #   '\n\twhile (current > 0) {\n\t\tcurrent = displayanddecrement(current);\n\t}'
    #   '\n\tprintf("%s", __throbac_cat(message, "\\n"));\n}'),
    #  ('APUD start: NUMERUS, message : LOCUTIO DEFINITIO countdown > current : NUMERUS MUTABILIS current start VALORUM '
    #   'current SUPRA .NIL. DUM > current APUD current VOCO displayanddecrement VALORUM < '
    #   'message IUNGO ^+^ LOCUTIO.IMPRIMO <'), 'funcDef'),
    # ('int stringlength(char* str) {\n\treturn 3;\n}',
    #  'APUD str : LOCUTIO DEFINITIO stringlength PRAEBET NUMERUS > .III. REDEO <', 'funcDef'),
    #
    #
    # # script
    # (('#include <stdio.h>\n#include <stdbool.h>\n#include "throbac.h"\n\nvoid testfunc(int thing);\n'
    #   'int main() {\n\tint someint = 0;\n\tif (20 < 40) {\n\t\tsomeint = 20;\n\t}\n\treturn 0;\n}\nvoid '
    #   'testfunc(int thing) {\n\treturn thing + 35;\n}'),
    #  ('APUD thing : NUMERUS DEFINITIO testfunc > thing ADDO .III.V. REDEO < someint : NUMERUS MUTABILIS '
    #   '.II.NIL. INFRA .IV.NIL. SI > someint .II.NIL. VALORUM <'), 'script'),
    # ('', '', 'script'),
]


class TranslationTest(unittest.TestCase):

    def test_all_cases(self):
        self.maxDiff = None
        for c, throbac, rule in TEST_CASES:
            with self.subTest(c=c,
                              throbac=throbac,
                              rule=rule):
                self.assertEqual(c, as_c(throbac, rule))
