import json, csv

def load_samples_from_json(file_name):
    # Essa função lê os 284 "esquemas" ou "amostras" do .json e coloca em samples
    with open(file_name, 'r', encoding='utf-8') as file:
        samples = json.load(file)
    return samples

def create_json(file_name, translated_samples):
    # Essa função cria o arquivo .json traduzido pro inglês
    with open(file_name, 'w', encoding='utf-8') as output_file:
        json.dump(translated_samples, output_file, ensure_ascii=False)

def create_csv(file_name, translated_samples):
    # Essa função cria o arquivo .csv de esquemas traduzido pro inglês
    with open(file_name, 'w', encoding='utf-8', newline='') as output_file:
        writer = csv.writer(output_file, delimiter=',')
        writer.writerow(translated_samples)


samples = load_samples_from_json('english_wsc.json')

only_schema_samples = []
i = 0
for sample in samples:
    i = i+1
    only_schema_samples.append(sample['schema'])

create_csv('english_wsc_only_schemas.csv', only_schema_samples)
create_json('english_wsc_only_schemas.json', only_schema_samples)