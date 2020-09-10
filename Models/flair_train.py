from flair.data import Corpus
from flair.datasets import NER_BASQUE, TREC_6, ColumnCorpus
from flair.embeddings import TokenEmbeddings, WordEmbeddings, StackedEmbeddings, FlairEmbeddings, PooledFlairEmbeddings, BertEmbeddings, CharacterEmbeddings, TransformerWordEmbeddings, TransformerDocumentEmbeddings
from typing import List

from flair.models import SequenceTagger, TextClassifier
from flair.trainers import ModelTrainer

from torch.optim.adam import Adam
import torch

def train_FLAIR(path, lr, batch, epochs):
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
      CharacterEmbeddings(), # azkarrago egiteko entrenamendua
      WordEmbeddings('eu'),
      
      # contextual string embeddings, forward
      FlairEmbeddings('eu-forward'),
      #PooledFlairEmbeddings('eu-forward'),

      # contextual string embeddings, backward
      FlairEmbeddings('eu-backward'),
      #PooledFlairEmbeddings('eu-backward'),
    ]
    
    embeddings: StackedEmbeddings = StackedEmbeddings(#mini_batch_chunk_size=4, # optionally set this if transformer is too much for your machine
                                                      embeddings=embedding_types)
    
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
    trainer.train(path,
                learning_rate = lr,
                mini_batch_size = batch,
                max_epochs = epochs,
                embeddings_storage_mode='gpu')
    
def train_TRFM(path, lr, batch, epochs):

    # 1. get the corpus
    corpus: Corpus = NER_BASQUE()
    print(corpus)

    # 2. create the label dictionary
    label_dict = corpus.make_label_dictionary()
    print(label_dict)

    # 2.2 what tag do we want to predict?
    tagType = 'ner'

    # 3. initialize transformer document embeddings (many models are available)
    # models: https://huggingface.co/transformers/pretrained_models.html
    # xlm-roberta-base , bert-base-multilingual-uncased , 
    embeddings = TransformerWordEmbeddings('xlm-roberta-base', fine_tune=True)
    
    # 4. create the text classifier
    classifier = SequenceTagger(hidden_size=256,
                                embeddings=embeddings,
                                tag_dictionary=label_dict,
                                tag_type=tagType)

    # 5. initialize the text classifier trainer with Adam optimizer
    trainer = ModelTrainer(classifier, corpus, optimizer=Adam)

    # 6. start the training
    trainer.train(path,
            learning_rate = lr,
            mini_batch_size = batch,
            max_epochs = epochs,
            embeddings_storage_mode='gpu')

def train_flair_time(path, lr, batch, epochs):

    # 1. get the corpus
    corpus_folder = '/content/drive/My Drive/Practicas/Database/timetag'
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
    
    #torch.cuda.empty_cache()

    # 6. initialize trainer

    trainer: ModelTrainer = ModelTrainer(tagger, corpus)

    # 7. start training
    trainer.train(path,
                learning_rate = lr,
                mini_batch_size = batch,
                max_epochs = epochs,
                embeddings_storage_mode='gpu')

def train_flair_chunk(path, lr, batch, epochs):
    # 1. get the corpus
    corpus_folder = '/content/drive/My Drive/Practicas/Database/chunk'
    columns = {0: "text", 1: "parts", 2: "chunk"}
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

    trainer.train(path,
                learning_rate = lr,
                mini_batch_size = batch,
                max_epochs = epochs,
                embeddings_storage_mode='gpu')

if "__main__" == __name__: # hay que actualizar las carpetas, abajo y en las funciones

    train_FLAIR('/content/drive/My Drive/Practicas/Training_models/Flair', lr = 0.2, batch = 32, epochs = 150) #OK

    #train_flair_time('/content/drive/My Drive/Practicas/Training_models/Time', lr = 5e-2, batch = 8, epochs = 100) # OK

    #train_flair_chunk('/content/drive/My Drive/Practicas/Training_models/chunk', lr = 0.1, batch = 16, epochs = 150) #OK

    #train_TRFM('/content/drive/My Drive/Practicas/Training_models/TRFM', lr = 3e-5, batch = 16, epochs = 5) #OK (problema al usar el modelo)

    #import torch
    #torch.cuda.empty_cache()
