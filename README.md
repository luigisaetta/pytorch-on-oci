# PyTorch on Oracle Cloud
This repository supports all the work I have done to prepare a set of tutorials and trainings aimed to show how to easily use PyTorch on OCI.

For now, all the chapters are written in Italian. It is possible that, in a near future, I'll translate it.

## Stato: WIP.
Il lavoro è iniziato a **fine ottobre 2022** e, malgrado il mio entusiasmo, posso dedicarvi soltanto la parte di tempo libero che non dedico alle mie due figlie, alla corsa ed al triathlon.

Ma, prometto che aggiornerò e renderò via via più ricchi i contenuti, con ragionevole regolarità. L'obiettivo è: ogni volta che mi verrà l'idea di un esempio, di un concetto da sviluppare, lo includerò.

## Perchè PyTorch.
E' una lunga storia. In origine, tutti i miei studi sul **Deep Learning** sono stati basati su **Keras**. Ma, mi sono via via reso conto che il mondo dei ricercatori ed i contributi da parte delle aziende che lavorano sull'Open Source vanno sempre più nella direzione di un'adozione di PyTorch.

Si deve sempre essere pronti a cambiare idea. Oggi, quando posso, io preferisco utilizzare PyTorch.

Ad esempio, nel campo del NLP se si vuole utilizzare i modelli distribuiti su **Hugging Face Hub**, è molto utile conoscere e saper utilizzare correttamente PyTorch.

## Capitoli
[Ch-01: creazione di un ambiente PyTorch e primi test](./ch-01/ch-01.md)
* [Sicurezza](./ch-01/security.md)
* [Object Storage](./ch-01/ch-01-object-storage.md)

[Ch-02: lavorare con i dataset](./ch-02/ch-02.md)

[Ch-03: un primo esempio di rete Fully Connected](./ch-03/ch-03.md)
* [Utilizzare TensorBoard in OCI Data Science](./ch-03/tensorboard.md)

[Ch-04: PyTorch Lightning](./ch-04/ch-04.md)
* [CNN con Lightning per il MNIST dataset](./ch-04/lightning_mnist_cnn.ipynb)
* [Salvare un modello PyTorch nel Model Catalog](./ch-04/pytorch_model_catalog.ipynb)

[Ch-05: distribuire i modelli](./ch-05/ch-05.md)
* [CNN con Lightning per il MNIST dataset: formato ONNX](./ch-05/lightning_to_onnx.ipynb)

[Ch-MLflow: integrazione con MLflow](./ch-mlflow.mc)
* [Integrare Lightning con MLflow](./ch-mlflow/lightning_mnist_cnn_mlflow.ipynb)
