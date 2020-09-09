# NLP-praktika
Dentro de NLP, se centrara principalmente en NER (Named Entity Recognition), haciendo uso de flair, transformers, etc.

# Download models
Each model's size is around 600MB. Too much for git repository. Use this link to download the model you want manually:

https://drive.google.com/drive/folders/1JR_HsXVbD1nCnrHytpLc3bYkhIEbbBZM?usp=sharing

The model ("*.pt") must be inside an specific folder. The path of that folder is  "/Models/trained_models/(ALG)/(TAG)/(LAN)/" 

Where:
- (ALG) = Algorithm -> {'Flair', 'Transformer'}
- (TAG) = Tagger -> {'ner', 'pos', 'chunk'}
- (LAN) = Languague -> {'en', 'es', 'eu', 'ca', 'gl'}

# Version de Python usada 3.7.2
