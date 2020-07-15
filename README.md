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

Results(ner_eu):
- F1-score (micro) 0.8222
- F1-score (macro) 0.7069

Results(chunk_eu):
- F1-score (micro) 0.9412
- F1-score (macro) 0.6315

# Uso

Añadir los parametros deseados en Tagger/main.py, a la llamada de la función main(...) que se encuentra en la parte inferior del archivo, guardar los cambios y ejecutar este mismo archivo.

Comando de ejecución: 
```sh
	$ python main.py
```

Por defecto el directorio para el documento de entrada es: "../tests/Input/" 
Por defecto el directorio para el documento de salida, donde se guardaran los resultados es: "../tests/Output/" 
Ambos estan definidos en el propio archivo main.py mediante variables globales al comienzo del archivo.

Para más informacion acerca de los parametros de esta función, en este mismo archivo estan todas las funciones documentadas. En especifico, la documentación que habría que mirar es la de la función main() situada en la parte inferior del archivo.

# Version de Python usada 3.7.2
