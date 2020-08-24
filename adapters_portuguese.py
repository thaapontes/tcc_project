import json


def transform_file_json_to_txt(file_name, output_name):
    samples = load_samples_from_json(file_name)
    replaced_samples = []
    for sample in samples:
        replaced_samples.append(adapt_sample_json_to_txt(sample))
    with open(output_name, "w", encoding="utf-8") as output_file:
        for sample in replaced_samples:
            output_file.write(sample)
            output_file.write("\n\n")


def adapt_sample_json_to_txt(sample):
    template_output = "{}\n" "[MASK]\n" "{}, {}\n" "{}"
    replaced_schema = replace_last_pronoun(sample["schema"], sample["pronoun"])
    substitution_a = sample["substitution_a"]
    substitution_b = sample["substitution_b"]
    if sample["correct_answer"] == "A":
        correct_answer = substitution_a
    else:
        correct_answer = substitution_b

    return template_output.format(
        replaced_schema, substitution_a, substitution_b, correct_answer
    )


def replace_last_pronoun(schema, pronoun):
    """Replace last pronoun in sentence with [MASK]"""
    pronouns = [
        "eles",
        "ela",
        "ele",
        "os",
        "dela",
        "it",
        "o",
        "la",
        "lo",
        "a",
        "la",
        "las",
        "deles",
        "delas",
        "dele",
        "sua",
        "seu",
        "suas",
    ]

    replaced = []

    # Aqui substituo todas as marcações no texto por ela mesmo com espaço antes, pois senão o split faz com que a palavra contenha esse sinal nela
    # Com o espaço antes, no split() o sinal de pontuação vira uma palavra. Ex: Olá. -> ["Olá", "."]
    reversed_split_sentence = schema.replace("'", " '")
    reversed_split_sentence = reversed_split_sentence.replace('"', ' "')
    reversed_split_sentence = reversed_split_sentence.replace(".", " .")
    reversed_split_sentence = reversed_split_sentence.replace(",", " ,")
    reversed_split_sentence = reversed_split_sentence.replace("-", " - ")

    reversed_split_sentence = reversed_split_sentence.split()
    reversed_split_sentence.reverse()

    already_replaced = False
    for word in reversed_split_sentence:
        if word.lower() == pronoun.lower() and not already_replaced:
            word_to_replace = "[MASK]"
            already_replaced = True
        elif word.lower() == "lo" and pronoun.lower() == "-lo" and not already_replaced:
            word_to_replace = "[MASK]"
            already_replaced = True
        else:
            word_to_replace = word
        replaced.append(word_to_replace)

    # Caso o pronome do snippet não seja encontrado na frase.
    # Em português, não é para isso ocorrer, pois sempre o pronome do campo 'pronoun' vai ser encontrado
    # na frase, mas é importante manter, caso tenhamos algum problema
    if already_replaced == False:
        print("SEM PRONOME")
        replaced = []
        for word in reversed_split_sentence:
            # Neste caso, pegamos o primeiro pronome, de trás para frente, que está na lista de pronomes válidos do WSC
            if word.lower() in pronouns and not already_replaced:
                word_to_replace = "[MASK]"
                already_replaced = True
            else:
                word_to_replace = word
            replaced.append(word_to_replace)

    replaced.reverse()
    print(replaced)

    output = " ".join(replaced)

    # Aqui desfazemos aquela artimanha de adicionar espaço antes de pontuações, para que fique correto na frase final
    output = output.replace(" '", "'")
    output = output.replace(' "', '"')
    output = output.replace(" .", ".")
    output = output.replace(" ,", ",")
    output = output.replace(" - ", "-")

    return output


def load_samples_from_json(file_name):
    # Essa função lê os 284 "esquemas" ou "amostras" do .json e coloca em samples
    with open(file_name, "r", encoding="utf-8") as file:
        samples = json.load(file)
    return samples


if __name__ == "__main__":
    transform_file_json_to_txt("portuguese_wsc.json", "portuguese_wsc.txt")
