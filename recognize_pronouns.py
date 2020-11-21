import json

def load_samples_from_json(file_name):
    # Essa função lê os 284 "esquemas" ou "amostras" do .json e coloca em samples
    with open(file_name, 'r', encoding='utf-8') as file:
        samples = json.load(file)

    pronouns = ["he", "her", "him", "his", "it", "she", "them", "they", "your"]
    for sample in samples:
        sentença = sample['sentence']
        split = sentença.split()
        for i in range(0, len(split)):
            if split[i].lower() in pronouns:
                pronoun = split[i]
        print(pronoun)

def main():
    load_samples_from_json('original_english_wsc.json')

if __name__ == "__main__":
    main()