# NLP-praktika
Dentro de NLP, se centrara principalmente en NER (Named Entity Recognition), haciendo uso de flair, transformers, etc.

Each model's size is around 600MB. Too much for git repository. Use this link to download the model you want:

https://drive.google.com/drive/folders/1JR_HsXVbD1nCnrHytpLc3bYkhIEbbBZM?usp=sharing

The model ("best-model.pt") must be inside an specific folder. The path of that folder is  "/Models/trained_models/(ALG)/(TAG)/(LAN)/" 

Where:
- (ALG) = Algorithm -> {'Flair', 'Transformer'}
- (TAG) = Tagger -> {'ner', 'pos'}
- (LAN) = Languague -> {'en', 'es', 'eu', 'ca', 'gl'}

Results(ner_eu):
- F1-score (micro) 0.8222
- F1-score (macro) 0.7069

# Uso

Añadir los parametros deseados en Tagger/main.py (variables globales, en la parte superior del archivo), y ejecutar este mismo archivo.
