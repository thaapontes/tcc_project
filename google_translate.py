#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Translates text into the target language.

Target must be an ISO 639-1 language code.
See https://g.co/cloud/translate/v2/translate-reference#supported_languages
"""
from google.cloud import translate_v2 as translate
import json

def create_translated_json(file_name, translated_samples):
    #Essa função cria o arquivo .json traduzido pro inglês
    with open(file_name, 'w', encoding='utf-8') as output_file:
        json.dump(translated_samples, output_file, ensure_ascii=False)
    

def load_samples_from_json(file_name):
    #Essa função lê os 284 "esquemas" ou "amostras" do .json e coloca em samples
    with open(file_name, 'r', encoding='utf-8') as file:
        samples = json.load(file)
    return samples

def translate_sample(sample):
    #Essa função faz a tradução de um esquema/amostra 
    translated_sample = {}
    translated_sample['schema'] = translate_text(sample['schema'])
    translated_sample['snippet'] = translate_text(sample['snippet'])
    translated_sample['pronoun'] = translate_text(sample['pronoun'])
    translated_sample['correct_answer'] = sample['correct_answer']
    translated_sample['substitution_a'] = translate_text(sample['substitution_a'])
    translated_sample['substitution_b'] = translate_text(sample['substitution_b'])
    translated_sample['translated'] = sample['translated']
    return translated_sample

def translate_text(text,target='en'):
    """
    Target must be an ISO 639-1 language code.
    https://cloud.google.com/translate/docs/languages
    """
    translate_client = translate.Client()
    result = translate_client.translate(
        text,
        target_language=target)

    #print(u'Text: {}'.format(result['input']))
    #print(u'Translation: {}'.format(result['translatedText']))
    #print(u'Detected source language: {}'.format(result['detectedSourceLanguage']))
    return result

#example_text ='''A medalha não cabe na mala porque ela é grande'''
#translate_text(example_text, target='en')

samples = load_samples_from_json('portuguese_wsc.json')
translated_samples = []
for sample in samples:
    translated_samples.append(translate_sample(sample))

create_translated_json('english_wsc.json', translated_samples)

