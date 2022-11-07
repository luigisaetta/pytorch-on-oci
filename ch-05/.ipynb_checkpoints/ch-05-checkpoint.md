# Deploying Models

## Introduzione.

Dopo aver sviluppato, validato e testato il modello ML, basato su rete neurale vi è da compiere l'importante passo successivo: metterlo in produzione, in modo che il modello possa essere utilizzato per effettuare le previsioni su nuovi dati.

La messa in produzione non è sempre un'operazione semplice. E l'operazione in passato era complicata dal fatto che si doveva tener traccia delle librerie, e relative versioni, utilizzate in fase di sviluppo. Inoltre, framework differenti utilizzano formati differenti per salvare (serializzare) il modello.

Una soluzione che si può adottare per semplificare è di utilizzare **ONNX**.


## ONNX

ONNX: Open Neural Network Exchange : https://onnx.ai/

ONNX è un formato **aperto**, nato per rappresentare modelli di Machine Learning.

E' uno standard nato per supportare l'interoperabilità e consentire di mettere in produzione modelli di ML in un formato indipendente dal framework utilizzato per sviluppare.

In sintesi: l'obiettivo di ONNX è di consentire di sviluppare un modello con il proprio framework preferito (TensorFlow, PyTorch, etc) e poi di metterlo in produzione utilizzando un formato indipendente ed unificato.

ONNX mette a disposizione:
* un comune formato di file, per la serializzazione del modello
* un set comune di operatori che consenono di definire la struttura di una qualsiasi rete neurale.

##


