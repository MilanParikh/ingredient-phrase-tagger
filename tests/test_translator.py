import unittest

from ingredient_phrase_tagger.training import translator


class TranslatorTest(unittest.TestCase):

    def test_translates_row_with_simple_phrase(self):
        row = {
            'index': 162,
            'input': '2 cups flour',
            'name': 'flour',
            'qty': 2.0,
            'range_end': 0.0,
            'unit': 'cup',
            'comment': '',
        }

        self.assertMultiLineEqual("""
2\tI1\tL4\tNoCAP\tNoPAREN\tB-QTY
cups\tI2\tL4\tNoCAP\tNoPAREN\tB-UNIT
flour\tI3\tL4\tNoCAP\tNoPAREN\tB-NAME
""".strip(),
                                  translator.translate_row(row).strip())

    def test_translates_row_with_simple_fraction(self):
        row = {
            'index': 161,
            'input': '1/2 cup yellow cornmeal',
            'name': 'yellow cornmeal',
            'qty': 0.5,
            'range_end': 0.0,
            'unit': 'cup',
            'comment': '',
        }

        self.assertMultiLineEqual("""
1/2\tI1\tL8\tNoCAP\tNoPAREN\tB-QTY
cup\tI2\tL8\tNoCAP\tNoPAREN\tB-UNIT
yellow\tI3\tL8\tNoCAP\tNoPAREN\tB-NAME
cornmeal\tI4\tL8\tNoCAP\tNoPAREN\tI-NAME
""".strip(),
                                  translator.translate_row(row).strip())

    def test_translates_row_with_complex_fraction(self):
        row = {
            'index': 158,
            'input': '1 1/2 teaspoons salt',
            'name': 'salt',
            'qty': 1.5,
            'range_end': 0.0,
            'unit': 'teaspoon',
            'comment': '',
        }

        self.assertMultiLineEqual("""
1$1/2\tI1\tL4\tNoCAP\tNoPAREN\tB-QTY
teaspoons\tI2\tL4\tNoCAP\tNoPAREN\tB-UNIT
salt\tI3\tL4\tNoCAP\tNoPAREN\tB-NAME
""".strip(),
                                  translator.translate_row(row).strip())

    def test_translates_row_with_comment(self):
        row = {
            'index': 412,
            'input': 'Half a vanilla bean, split lengthwise, seeds scraped',
            'name': 'vanilla bean',
            'qty': 0.5,
            'range_end': 0.0,
            'unit': '',
            'comment': 'split lengthwise, seeds scraped',
        }

        self.assertMultiLineEqual("""
Half\tI1\tL12\tYesCAP\tNoPAREN\tOTHER
a\tI2\tL12\tNoCAP\tNoPAREN\tOTHER
vanilla\tI3\tL12\tNoCAP\tNoPAREN\tB-NAME
bean\tI4\tL12\tNoCAP\tNoPAREN\tI-NAME
,\tI5\tL12\tNoCAP\tNoPAREN\tB-COMMENT
split\tI6\tL12\tNoCAP\tNoPAREN\tI-COMMENT
lengthwise\tI7\tL12\tNoCAP\tNoPAREN\tI-COMMENT
,\tI8\tL12\tNoCAP\tNoPAREN\tI-COMMENT
seeds\tI9\tL12\tNoCAP\tNoPAREN\tI-COMMENT
scraped\tI10\tL12\tNoCAP\tNoPAREN\tI-COMMENT
""".strip(),
                                  translator.translate_row(row).strip())
