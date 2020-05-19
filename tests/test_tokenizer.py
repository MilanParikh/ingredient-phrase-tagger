import unittest

from ingredient_phrase_tagger.training import tokenizer


class TokenizerTest(unittest.TestCase):

    def test_tokenizer_splits_slash_separated_alternatives(self):
        pairs = [('2 tablespoons/30 milliliters milk or cream', [
            '2', 'tablespoons', '30', 'milliliters', 'milk', 'or', 'cream'
        ]), ('2 1/2 cups/300 grams all-purpose flour',
             ['2$1/2', 'cups', '300', 'grams', 'all-purpose', 'flour'])]
        for ingredient, tokens_expected in pairs:
            tokens_actual = tokenizer.tokenize(ingredient)
            self.assertEqual(tokens_expected, tokens_actual)

    def test_tokenizer_expands_unit_abbreviations(self):
        pairs = [
            ('100g melted chocolate', ['100', 'grams', 'melted', 'chocolate']),
            ('8oz diet coke', ['8', 'ounces', 'diet', 'coke']),
            ('15ml coconut oil', ['15', 'milliliters', 'coconut', 'oil']),
            ('15mL coconut oil', ['15', 'milliliters', 'coconut', 'oil']),
        ]
        for ingredient, tokens_expected in pairs:
            tokens_actual = tokenizer.tokenize(ingredient)
            self.assertEqual(tokens_expected, tokens_actual)
