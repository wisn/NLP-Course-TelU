"""
Simple Rule-Based Name Entitiy Recognizer
"""

class NameEntityRecognizer:
    file_paths = { 'test': '', 'train': '' }

    named_entities = { 'test': [], 'train': [] }
    postags = { 'test': [], 'train': [] }
    sentences = { 'test': [], 'train': [] }

    def is_all_upper(self, words = ''):
        upper = True
        for word in words:
            if not upper:
                break

            upper &= word.isupper()

        return upper

    def trainsModel(self, file_path):
        file_object = open(file_path, 'r')
        lines = file_object.readlines()

        current_named_entity = []
        current_postag = []
        current_sentence = []

        for line in lines:
            if len(line) == 1:
                self.named_entities['train'].append(current_named_entity)
                self.postags['train'].append(current_postag)
                self.sentences['train'].append(current_sentence)

                current_named_entity.clear()
                current_postag.clear()
                current_sentence.clear()
            else:
                line = line.rstrip('\n')
                parts = line.split(' ')

                named_entity = parts[2]
                postag = parts[1]
                words = parts[0]

                current_named_entity.append(named_entity)
                current_postag.append(postag)
                current_sentence.append(words)
    
    def recognizeTokensByPostags(self, tokens = [], postags = []):
        named_entities = []

        last_postag = ''
        last_named_entity = ''

        for token in tokens:
            N = len(named_entities)

            if len(named_entities) > 0:
                last_postag = postags[N - 1]
                last_named_entity = named_entities[N - 1]

            if token[0].isupper():
                if self.is_all_upper(token):
                    if postags[N] == 'NN' or postags[N] == 'NNP':
                        if last_named_entity == 'B-ORG' or last_named_entity == 'I-ORG':
                            named_entities.append('I-ORG')
                        else:
                            named_entities.append('B-ORG')
                    else:
                        named_entities.append('O')
                else:
                    if last_postag == 'IN':
                        if token[0].isupper():
                            named_entities.append('B-LOC')
                        else:
                            named_entities.append('O')
                    else:
                        if last_named_entity == 'B-LOC' or last_named_entity == 'I-LOC':
                            named_entities.append('I-LOC')
                        else:
                            if postags[N] == 'NNP':
                                if last_named_entity == 'B-PER' or last_named_entity == 'I-PER':
                                    named_entities.append('I-PER')
                                else:
                                    named_entities.append('B-PER')
                            else:
                                named_entities.append('O')
            else:
                named_entities.append('O')

        return named_entities

lines = []
with open('kalimat_POSTag.txt', 'r') as f:
    lines = f.readlines()

NER = NameEntityRecognizer()

current_postag = []
current_token = []

for line in lines:
    if len(line) == 1:
        current_named_entity = NER.recognizeTokensByPostags(current_token, current_postag)

        for i in range(len(current_token)):
            named_entity = current_named_entity[i]
            postag = current_postag[i]
            token = current_token[i]

            print(token, postag, named_entity)

        print()

        current_postag.clear()
        current_token.clear()
    else:
        line = line.rstrip('\n')
        parts = line.split(' ')

        postag = parts[1]
        token = parts[0]

        current_postag.append(postag)
        current_token.append(token)
