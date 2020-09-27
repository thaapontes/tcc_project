
from google.cloud import translate_v2 as translate
import json, jsonlines
from multiprocessing import Pool


def create_translated_json(file_name, translated_samples):
    # Essa função cria o arquivo .json traduzido pro inglês
    with open(file_name, 'w', encoding='utf-8') as output_file:
        json.dump(translated_samples, output_file, ensure_ascii=False)


def load_samples_from_jsonl(file_name):
    # Essa função lê os "esquemas" do WINOGRANDE do .jsonl e coloca em samples

    with jsonlines.open(file_name) as file:
        result = []
        for obj in file:
            result.append(obj)

    return result


def translate_batches(sample):
    # Essa função faz a tradução de um esquema/amostravdo WINOGRANDE

    sample_replaced = sample['sentence'].replace('_', '[_]')
    
    portuguese_winogrande = {}
    portuguese_winogrande['qID'] = sample['qID']
    portuguese_winogrande['sentence'] = translate_text_to_portuguese(sample_replaced)
    portuguese_winogrande['option1'] = translate_text_to_portuguese(sample['option1'])
    portuguese_winogrande['option2'] = translate_text_to_portuguese(sample['option2'])
    portuguese_winogrande['answer'] = sample['answer']
    portuguese_winogrande['sentence'] = portuguese_winogrande['sentence'].replace('[_]','[MASK]')
    print(portuguese_winogrande['sentence'])
    return portuguese_winogrande
    

def translate_text_to_portuguese(text, target='pt'):
    """
    Target must be an ISO 639-1 language code.
    https://cloud.google.com/translate/docs/languages
    """
    translate_client = translate.Client()
    result = translate_client.translate(
        text,
        target_language=target)

    return result['translatedText']


def main():

    batch_one_winogrande = load_samples_from_jsonl('train_xs.jsonl')


    with Pool(5) as p:
       portuguese_winogrande_one = p.map(translate_batches, batch_one_winogrande)


    create_translated_json('portuguese_winogrande.json', portuguese_winogrande_one)


if __name__ == "__main__":
    main()