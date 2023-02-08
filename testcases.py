"""
Test cases for the Throbac to C transpiler

Author: TODO: your names here

Version: TODO: submission date here
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

    # parentheses
    ('(6)', '(.VI.)', 'expr'),
    ('(true)', '(VERUM)', 'expr'),
    ('(false)', '(FALSUM)', 'expr'),
    ('(6 * 8)', '(.VI. CONGERO .VIII.)', 'expr'),

    # concatenation
    ('__throbac_cat("HELLO.WORLD", "ISHERE")', '^HELLO.WORLD^ IUNGO ^ISHERE^', 'expr'),
    ('__throbac_cat(__throbac_cat("WHYARE", "YOU"), "SCREAMING.\\nSTOP.")', '^WHYARE^ IUNGO ^YOU^ IUNGO ^SCREAMING.+STOP.^', 'expr'),
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
    # --> add more here

    # multiply and divide
    ('8 * 13', '.VIII. CONGERO .I.III.', 'expr'),
    ('5 / 9', '.V. PARTIO .IX.', 'expr'),

    # negation
    ('true', 'NI FALSUM', 'expr'),
    ('false', 'NI NI NI VERUM', 'expr'),
    ('true', 'NI NI NI NI NI FALSUM', 'expr'),
    ('-7', 'NEGANS .NIL.NIL.VII.', 'expr'),
    ('7', 'NEGANS NEGANS .NIL.NIL.VII.', 'expr'),

    # function call
    ('countdown(10, announce)', 'APUD .I.NIL., announce VOCO countdown', 'funcCall'),

    # function call expression
    ('outerfunc(countdown(10, announce)) + 1', 'APUD APUD .I.NIL., announce VOCO countdown VOCO outerfunc ADDO .I.', 'expr'),

    # function call statement
    ('result = countdown(10, announce);', 'result APUD .I.NIL., announce VOCO countdown VALORUM', 'statement'),

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



    # block ME
    # ('printf("HELLOWORLD"); return 2;', '^HELLO^ LOCUTIO.IMPRIMO .II. REDEO', 'block'),

    # block
    #('printf("HELLOWORLD"); return 2;', '^HELLO^ LOCUTIO.IMPRIMO .II. REDEO', 'block'),
    ('var = "HELLO";\nreturn 77 + 6;', 'var ^HELLO^ VALORUM .VII.VII. ADDO .VI. REDEO', 'block'),


    # while


    # print bool
    ('printf("%s", "true");', 'VERUM VERITAS.IMPRIMO', 'statement'),
    ('printf("%s", "false");', 'NI VERUM VERITAS.IMPRIMO', 'statement'),
    ('printf("%s", "false");', 'NI NI FALSUM VERITAS.IMPRIMO', 'statement'),

    # block
    #('printf("%s", "HELLOWORLD"); return 2;', '^HELLO^ LOCUTIO.IMPRIMO .II. REDEO', 'block'),
    ('var = "HELLO";\nreturn 77 + 6;', 'var ^HELLO^ VALORUM .VII.VII. ADDO .VI. REDEO', 'block'),

    # while
    #('while (current > 0) {\ncurrent = displayanddecrement(current);\n}',
     #'current SUPRA .NIL. DUM >\ncurrent APUD current VOCO displayanddecrement VALORUM\n<', 'statement'),
    ('while (x > 10) {\nx = x + 2;\n}', 'x SUPRA .I.NIL. DUM >x x ADDO .II. VALORUM<', 'statement'),

    # if

    # nameDef
    ('int anid', 'anid : NUMERUS', 'nameDef'),
    ('bool anbooleanyep', 'anbooleanyep : VERITAS', 'nameDef'),
    ('char* somethingcool', 'somethingcool : LOCUTIO', 'nameDef'),

    #('if (count == 3) {\n printf("%s", "GET.READY\\n");\n} else {\nprintf("%s","\\n");\n}',
     #'count IDEM .III. SI >\n^+GET.READY+^ LOCUTIO.IMPRIMO\n< ALUID >^+^ LOCUTIO.IMPRIMO\n<', 'statement'),
    ('if (test >= x) {\nreturn test;\n} else {\nreturn x;\n}',
     'test SUPRA.IDEM x SI >test REDEO< ALUID >x REDEO<', 'statement'),
    # nameDef

    # varDec
    ('int someint = 0;', 'someint : NUMERUS MUTABILIS', 'varDec'),
    ('char* somestr = NULL;', 'somestr : LOCUTIO MUTABILIS', 'varDec'),
    ('bool somebool = false;', 'somebool : VERITAS MUTABILIS', 'varDec'),

    # varBlock
    ('int someint = 0;\nchar* somestr = NULL;', 'someint : NUMERUS MUTABILIS somestr : LOCUTIO MUTABILIS', 'varBlock')
    # body
    # main


    # funcdef <-- todo last
    # script
]


class TranslationTest(unittest.TestCase):

    def test_all_cases(self):
        self.maxDiff = None
        for c, throbac, rule in TEST_CASES:
            with self.subTest(c=c,
                              throbac=throbac,
                              rule=rule):
                self.assertEqual(c, as_c(throbac, rule))
