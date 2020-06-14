def adapt_json_to_txt(schema):
    pass

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
    
