# two references for one document
from nltk.translate.bleu_score import sentence_bleu
from numpy import mean, median
import json


def load_samples_from_json(file_name):
    # Essa função lê os .json e coloca em samples
    with open(file_name, 'r', encoding='utf-8') as file:
        samples = json.load(file)
    return samples


def create_json(file_name, translated_samples):
    # Essa função cria o arquivo .json com a comparação e os score Bleu
    with open(file_name, 'w', encoding='utf-8') as output_file:
        json.dump(translated_samples, output_file, ensure_ascii=False)


original_samples = load_samples_from_json(
    '../original_english_wsc.json')  # Reference
translated_samples = load_samples_from_json('../english_wsc.json')  # Candidate

scores_samples = []
scores = []

for i in range(0, len(original_samples)):

    references = original_samples[i]['sentence'].split()
    candidates = translated_samples[i]['schema'].split()

    score_sample = {}
    score_sample['original'] = original_samples[i]['sentence']
    score_sample['candidate'] = translated_samples[i]['schema']
    score_sample['score 1-gram'] = sentence_bleu(
        [references], candidates, weights=(1, 0, 0, 0))
    score_sample['score 2-gram'] = sentence_bleu(
        [references], candidates, weights=(0, 1, 0, 0))
    score_sample['score 3-gram'] = sentence_bleu(
        [references], candidates, weights=(0, 0, 1, 0))
    score_sample['score 4-gram'] = sentence_bleu(
        [references], candidates, weights=(0, 0, 0, 1))

    scores_samples.append(score_sample)

create_json('bleu_data.json', scores_samples)
