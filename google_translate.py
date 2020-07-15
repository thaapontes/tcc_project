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

    pronouns = ["he", "her", "him", "his", "it", "she", "them", "they", "your"]

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
    translated_snippet = translated_sample['snippet'].replace("&quot;", " '")
    translated_snippet = translated_snippet.replace(".", " .")
    split_translated_snippet = translated_snippet.split()
    print(split_translated_snippet)

    pronoun_in_snippet = ""
    first_pronoun = 0
    for i in range(0, len(split_translated_snippet)):
        if split_translated_snippet[i].lower() in pronouns and first_pronoun == 0:
            pronoun_in_snippet = split_translated_snippet[i].lower()
            first_pronoun = 1
    print(pronoun_in_snippet)

    translated_sample['pronoun_from_snippet'] = pronoun_in_snippet

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
