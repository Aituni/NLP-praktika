from flair.data import Corpus
from flair.datasets import NER_BASQUE
from flair.embeddings import TokenEmbeddings, WordEmbeddings, StackedEmbeddings, FlairEmbeddings, PooledFlairEmbeddings, BertEmbeddings, CharacterEmbeddings, TransformerDocumentEmbeddings
from typing import List

from flair.models import SequenceTagger
from flair.trainers import ModelTrainer

USE_TRANSFORMER = True

def train_FLAIR():
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
      CharacterEmbeddings(), # comentar para entrenar más rapido
      WordEmbeddings('eu'),  #  "
      
      # contextual string embeddings, forward
      FlairEmbeddings('eu-forward'),
      #PooledFlairEmbeddings('eu-forward'),

      # contextual string embeddings, backward
      FlairEmbeddings('eu-backward'),
      #PooledFlairEmbeddings('eu-backward'),

    ]

    embeddings: StackedEmbeddings = StackedEmbeddings(embeddings=embedding_types)

    # initialize sequence tagger
    tagger: SequenceTagger = SequenceTagger(hidden_size=256,
                                          embeddings=embeddings,
                                          tag_dictionary=tag_dictionary,
                                          tag_type=tag_type,
                                          use_crf=True)

    # initialize trainer
    trainer: ModelTrainer = ModelTrainer(tagger, corpus)
    """
    for i in range(5):
      trainer.train('poolftchar0' + str(i), train_with_dev=False, max_epochs=150)
    """
    trainer.train('trained_models/Flair/NER/eu',
                learning_rate=0.1,
                mini_batch_size=32,
                max_epochs=150,
                embeddings_storage_mode='gpu')

def train_TRFM():
    # 1. get the corpus
    corpus: Corpus = NER_BASQUE()

    # 2.1. what tag do we want to predict?
    tag_type = 'ner'

    # 2.2. make the tag dictionary from the corpus
    tag_dictionary = corpus.make_tag_dictionary(tag_type=tag_type)

    # 3. initialize transformer document embeddings (many models are available)
    embeddings = TransformerDocumentEmbeddings('distilbert-base-uncased', fine_tune=True)

    # 4. create the text tagger
    tagger: SequenceTagger = SequenceTagger(hidden_size=256,
                                      embeddings=embeddings,
                                      tag_dictionary=tag_dictionary,
                                      tag_type=tag_type,
                                      use_crf=True)

    # 5. initialize the text tagger trainer with Adam optimizer
    trainer = ModelTrainer(tagger, corpus, optimizer=Adam)

    # 6. start the training
    trainer.train('trained_models/Transformer/NER/eu',
                  learning_rate=3e-5, # use very small learning rate
                  mini_batch_size=16,
                 # mini_batch_chunk_size=4, # optionally set this if transformer is too much for your machine
                  max_epochs=5, # terminate after 5 epochs
                  embeddings_storage_mode='gpu'
                  )

if USE_TRANSFORMER:
    train_TRFM()
else:
    train_FLAIR()