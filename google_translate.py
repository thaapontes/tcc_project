#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Translates text into the target language.

Target must be an ISO 639-1 language code.
See https://g.co/cloud/translate/v2/translate-reference#supported_languages
"""
from google.cloud import translate_v2 as translate
import json


def create_translated_json(file_name, translated_samples):
    # Essa função cria o arquivo .json traduzido pro inglês
    with open(file_name, 'w', encoding='utf-8') as output_file:
        json.dump(translated_samples, output_file, ensure_ascii=False)


def load_samples_from_json(file_name):
    # Essa função lê os 284 "esquemas" ou "amostras" do .json e coloca em samples
    with open(file_name, 'r', encoding='utf-8') as file:
        samples = json.load(file)
    return samples


def translate_sample(sample):
    # Essa função faz a tradução de um esquema/amostra

    # Lógica para adicionar marcação do pronome no snippet

    # Corrected snippet faz com que ponto final seja considerado uma outra palavra
    corrected_snippet = sample['snippet'].replace(".", " .")

    # No caso em que o pronome possui hífen, ele conta como uma palavra separada
    corrected_snippet = corrected_snippet.replace("-", " -")
    split_snippet = corrected_snippet.split()
    print(split_snippet)

    # Para garantir que pronoun_position_in_snippet tenha algum valor, colocaremos como menos -1 e caso não tenha sido alterado, será convertido em zero.
    pronoun_position_in_snippet = -1
    for j in range(0, len(split_snippet)):
        if sample['pronoun'] == split_snippet[j]:
            pronoun_position_in_snippet = j
            print(pronoun_position_in_snippet)

    if pronoun_position_in_snippet == -1:
        pronoun_position_in_snippet = 0

    translated_sample = {}
    translated_sample['schema'] = translate_text(sample['schema'])
    translated_sample['snippet'] = translate_text(sample['snippet'])
    translated_sample['pronoun'] = translate_text(sample['pronoun'])
    translated_sample['correct_answer'] = sample['correct_answer']
    translated_sample['substitution_a'] = translate_text(
        sample['substitution_a'])
    translated_sample['substitution_b'] = translate_text(
        sample['substitution_b'])
    translated_sample['translated'] = sample['translated']

    # A função replace é utilizada para que, no caso em que ocorra contrações na tradução, o "'s" seja considerado com uma palavra. Mesma coisa para o ponto final
    translated_snippet = translated_sample['snippet'].replace("&#39;", " '")
    translated_snippet = translated_snippet.replace(".", " .")
    split_translated_snippet = translated_snippet.split()
    print(split_translated_snippet)

    # Caso a frase em português tenha mais palavras que a inglês, e o pronome for nessas palavras adicionais, o pronome vai ser a última palavra do snippet em inglês
    if len(split_translated_snippet) - 1 < pronoun_position_in_snippet:
        pronoun_position_in_snippet = len(split_translated_snippet) - 1
    print(split_translated_snippet[pronoun_position_in_snippet].lower() + "\n")

    translated_sample['pronoun_from_snippet'] = split_translated_snippet[pronoun_position_in_snippet].lower()

    return translated_sample


def translate_text(text, target='en'):
    """
    Target must be an ISO 639-1 language code.
    https://cloud.google.com/translate/docs/languages
    """
    translate_client = translate.Client()
    result = translate_client.translate(
        text,
        target_language=target)

    return result['translatedText']


samples = load_samples_from_json('portuguese_wsc.json')

translated_samples = []
i = 0
for sample in samples:
    print(i)
    i = i+1
    translated_samples.append(translate_sample(sample))

create_translated_json('english_wsc.json', translated_samples)
