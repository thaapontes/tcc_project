import json


def transform_file_json_to_txt(file_name, output_name):
    samples = load_samples_from_json(file_name)
    replaced_samples = []
    for sample in samples:
        replaced_samples.append(adapt_sample_json_to_txt(sample))
    with open(output_name, 'w', encoding='utf-8') as output_file:
        for sample in replaced_samples:
            output_file.write(sample)
            output_file.write("\n\n")


def adapt_sample_json_to_txt(sample):
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


def load_samples_from_json(file_name):
    # Essa função lê os 284 "esquemas" ou "amostras" do .json e coloca em samples
    with open(file_name, 'r', encoding='utf-8') as file:
        samples = json.load(file)
    return samples


if __name__ == "__main__":
    transform_file_json_to_txt('english_wsc.json', 'english_wsc.txt')
