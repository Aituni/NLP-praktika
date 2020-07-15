from flair.data import Corpus
from flair.datasets import NER_BASQUE, ColumnCorpus, CONLL_2000
from flair.embeddings import TokenEmbeddings, WordEmbeddings, StackedEmbeddings, FlairEmbeddings, PooledFlairEmbeddings, BertEmbeddings, CharacterEmbeddings, TransformerDocumentEmbeddings
from typing import List
from torch.optim.adam import Adam #optimizer

from flair.models import SequenceTagger
from flair.trainers import ModelTrainer

def train_flair_ner():
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
    print(corpus)

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
    trainer = ModelTrainer(tagger, corpus)

    # 6. start the training
    
    trainer.train('trained_models/Transformer/NER/eu',
                  learning_rate=3e-5, # use very small learning rate
                  mini_batch_size=16,
                 # mini_batch_chunk_size=4, # optionally set this if transformer is too much for your machine
                  max_epochs=5, # terminate after 5 epochs
                  embeddings_storage_mode='cpu'
                  )
    
def train_flair_time():

    # 1. get the corpus
    corpus_folder = '../../database/Timetags'
    columns = {0: "text", 1: "time"}
    corpus : Corpus = ColumnCorpus(corpus_folder, columns,
                               train_file='EN_train.tsv',
                               test_file='EN_test.tsv'
                               )
    print(corpus)

    # 2. what tag do we want to predict?
    tag_type = 'time'

    # 3. make the tag dictionary from the corpus
    #tag_dictionary = [b'<unk>', b'O', b'B-TIME', b'I-TIME', b'<START>', b'<STOP>']
    tag_dictionary = corpus.make_tag_dictionary(tag_type=tag_type)
    print(tag_dictionary)

    # 4. initialize embeddings
    embedding_types = [

    #WordEmbeddings('glove'),

    # comment in this line to use character embeddings
    # CharacterEmbeddings(),

    # comment in these lines to use flair embeddings
    FlairEmbeddings('en-forward'),
    FlairEmbeddings('en-backward'),
    ]

    embeddings: StackedEmbeddings = StackedEmbeddings(embeddings=embedding_types)

    # 5. initialize sequence tagger
    tagger: SequenceTagger = SequenceTagger(hidden_size=256,
                                        embeddings=embeddings,
                                        tag_dictionary=tag_dictionary,
                                        tag_type=tag_type,
                                        use_crf=True)

    # 6. initialize trainer
    trainer: ModelTrainer = ModelTrainer(tagger, corpus)

    # 7. start training
    trainer.train('./trained_models/Flair/time',
              learning_rate=0.1,
              mini_batch_size=32,
              max_epochs=150,
              embeddings_storage_mode='cpu')

def train_flair_chunk():
    # 1. get the corpus
    corpus_folder = '../../database/chunk'
    columns = {0: "text", 1: "_", 2: "chunk"}
    corpus : Corpus = ColumnCorpus(corpus_folder, columns,
                               train_file='train.tsv',
                               test_file='test.tsv'
                               )
    #corpus: MultiCorpus = MultiCorpus([UD_ENGLISH(), UD_GERMAN()])
    #corpus: Corpus = CONLL_2000()
    print(corpus)

    # 2. what tag do we want to predict?
    tag_type = 'chunk'

    # 3. make the tag dictionary from the corpus
    tag_dictionary = corpus.make_tag_dictionary(tag_type=tag_type)
    print(tag_dictionary)

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

    trainer.train('trained_models/Flair/chunk/eu',
                learning_rate=0.1,
                mini_batch_size=32,
                max_epochs=1,
                embeddings_storage_mode='gpu')

if "__main__" == __name__:

    #train_TRFM()

    #train_flair_ner()
    
    #train_flair_time()

    train_flair_chunk()


    #import torch
    #torch.cuda.empty_cache()
