def adapt_json_to_txt(sample):
    template_output = ("{}\n"
                       "[MASK]\n"
                       "{}, {}\n"
                       "{}")
    replaced_schema = replace_last_pronoun(sample['schema'], sample['pronoun'])
    substitution_a = sample['substitution_a']
    substitution_b = sample['substitution_b']
    if sample['correct_answer'] == 'A':
        correct_answer = substitution_a
    else:
        correct_answer = substitution_b

    return template_output.format(replaced_schema, substitution_a,
                                  substitution_b, correct_answer)


def replace_last_pronoun(schema, pronoun):
    '''Replace last pronoun in sentence with [MASK]'''
    replaced = []
    reversed_split_sentence = schema.split()
    reversed_split_sentence.reverse()
    already_replaced = False
    for word in reversed_split_sentence:
        if word == pronoun and not already_replaced:
            word_to_replace = '[MASK]'
            already_replaced = True
        else:
            word_to_replace = word
        replaced.append(word_to_replace)
    replaced.reverse()
    return ' '.join(replaced)
