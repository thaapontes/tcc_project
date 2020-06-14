import unittest
from adapters import replace_last_pronoun

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
    
    
