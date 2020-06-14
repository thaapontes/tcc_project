import unittest
from adapters import replace_last_pronoun, adapt_json_to_txt


class TestReplaceLastPronoun(unittest.TestCase):

    def test_function_only_replaces_last_pronoun(self):
        pronoun = 'he'
        schema = ('George got free tickets for the play, but he gave them to Eric, '
                  'even though he was particularly interested in watching it.')
        expected = ('George got free tickets for the play, but he gave them to Eric, '
                    'even though [MASK] was particularly interested in watching it.')
        self.assertEqual(replace_last_pronoun(schema, pronoun), expected)

    def test_function_doesnt_replace_if_pronoun_not_found(self):
        pronoun = 'she'
        schema = ('George got free tickets for the play, but he gave them to Eric, '
                  'even though he was particularly interested in watching it.')
        expected = schema
        self.assertEqual(replace_last_pronoun(schema, pronoun), expected)


class TestAdaptJsonToTxt(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_function_works(self):
        sample = {
            "schema": "Carol believed that Rebecca suspected that she had stolen the watch.",
            "snippet": "she had stolen the watch.",
            "pronoun": "she",
            "correct_answer": "A",
            "substitution_a": "Carol",
            "substitution_b": "Rebecca",
            "translated": True
        }
        expected = ("Carol believed that Rebecca suspected that [MASK] had stolen the watch.\n"
                    "[MASK]\n"
                    "Carol, Rebecca\n"
                    "Carol")
        result = adapt_sample_json_to_txt(sample)
        self.assertEqual(result, expected)
