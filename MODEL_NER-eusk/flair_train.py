from flair.data import Corpus
from flair.datasets import NER_BASQUE
from flair.embeddings import TokenEmbeddings, WordEmbeddings, StackedEmbeddings, FlairEmbeddings, PooledFlairEmbeddings, BertEmbeddings, CharacterEmbeddings
from typing import List

# 1. get the corpus
corpus : Corpus = NER_BASQUE()
print(corpus)

# 2. what tag do we want to predict?
tag_type = 'ner'

# 3. make the tag dictionary from the corpus
tag_dictionary = corpus.make_tag_dictionary(tag_type=tag_type)
print(tag_dictionary.idx2item)

# initialize embeddings
embedding_types: List[TokenEmbeddings] = [

    #fastText official embeddings for Basque
    CharacterEmbeddings(),
    WordEmbeddings('eu'),
    
    # contextual string embeddings, forward
    FlairEmbeddings('eu-forward'),
    #PooledFlairEmbeddings('eu-forward'),
  
    # contextual string embeddings, backward
    FlairEmbeddings('eu-backward'),
    #PooledFlairEmbeddings('eu-backward'),

]

embeddings: StackedEmbeddings = StackedEmbeddings(embeddings=embedding_types)

# initialize sequence tagger
from flair.models import SequenceTagger

tagger: SequenceTagger = SequenceTagger(hidden_size=256,
                                        embeddings=embeddings,
                                        tag_dictionary=tag_dictionary,
                                        tag_type=tag_type,
                                        use_crf=True)

# initialize trainer
from flair.trainers import ModelTrainer

trainer: ModelTrainer = ModelTrainer(tagger, corpus)
"""
for i in range(5):
    trainer.train('poolftchar0' + str(i), train_with_dev=False, max_epochs=150)
"""
trainer.train('../../database/txt/from_pdf',
              learning_rate=0.1,
              mini_batch_size=32,
              max_epochs=150,
              embeddings_storage_mode='gpu')

