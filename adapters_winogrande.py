import json
from adapters_portuguese import load_samples_from_json 

def transform_file_json_to_txt_winogrande(file_name, output_name):
    samples = load_samples_from_json(file_name)
    replaced_samples = []
    for sample in samples:
        replaced_samples.append(adapt_sample_json_to_txt_winogrande(sample))
    with open(output_name, "w", encoding="utf-8") as output_file:
        for sample in replaced_samples:
            output_file.write(sample)
            output_file.write("\n\n")


def adapt_sample_json_to_txt_winogrande(sample):
    template_output = "{}\n" "[MASK]\n" "{}, {}\n" "{}"
    replaced_schema = sample['sentence']
    option1 = sample["option1"]
    option2 = sample["option2"]
    if sample["answer"] == "1":
        answer = option1
    else:
        answer = option2

    return template_output.format(
        replaced_schema, option1, option2, answer
    )


if __name__ == "__main__":
    #transform_file_json_to_txt_winogrande("portuguese_winogrande.json", "batch_one_winogrande.txt")
    transform_file_json_to_txt_winogrande("portuguese_winogrande_three.json", "batch_three_winogrande.txt")