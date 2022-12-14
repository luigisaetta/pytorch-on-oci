# PyTorch Lightning

## Introduzione.

Come **semplificare** lo sviluppo di modelli AI basati su PyTorch.

In PyTorch si deve spesso scrivere del codice che di fatto è codice ripetuto (boilerplate).

Per superare questa situazione, è stato introdotto PyTorch **Lightning**, un framework per **Deep Learning**, basato su PyTorch, che ha rapidamente catturato l'interesse di tantissime persone. 

Infatti, il suo [repository GitHub](https://github.com/Lightning-AI/lightning) ha più di 20000 stars e conta più di 750 contributors.

## Perchè usare Lightning

PyTorch consente di controllare completamente il codice del training loop. 

Ciò da una parte consente di comprendere bene come è strutturato un training loop, ma ha uno svantaggio: nei vari progetti gran parte del codice si ripete e ciò da un lato è una noiosa ripetizione e dall'altro comporta il richio di errori.

Lightning consente di strutture il codice in modo da evitare la ripetizione del codice.

I vantaggi:
* molta parte del codice "ripetitivo" (boilerplate) è eseguito in modo trasparente dal framework
* sono definite le funzioni in cui collocare le operazioni (training_step, validation_step)
* il logging e la gestione della progress bar sono semplificati
* è semplice eseguire su GPU (non ci si deve preoccupare di spostare i tensori...)

Esaminiamo i vari punti:

1. Scriviamo soltanto il codice per il singolo training_step ed il validation_step (elaborazione di un singolo batch)

2. Non dobbiamo preoccuparci di spostare i vari tensori sulla GPU

3. Gestiamo in modo semplice la scrittura di loss (ed altre metriche) sulla progress bar usando self.log

4. Per salvare la storia delle metriche possiamo usare il CSVLogger


## Argomenti trattari [WIP]
* come strutturare un progetto utilizzando PyTorch Lightning: [first_fc_lightning.ipynb](./first_fc_lightning.ipynb)
* impiego del CSVLogger: [first_fc_lightning.ipynb](./first_fc_lightning.ipynb) 
* calcolo del migliore LR: [first_fc_lightning_best_lr.ipynb](./first_fc_lightning_best_lr.ipynb)
* impiego di un LR Scheduler [multi_input_nn.ipynb](./multi_input_nn.ipynb)
* come implementare una rete **multi-input** [multi_input_nn.ipynb](./multi_input_nn.ipynb)
* il classico esempio: CNN su MNIST dataset [lightning_mnist_cnn.ipynb](./lightning_mnist_cnn.ipynb)
* Salvare il modello nel **Model Catalog** utilizzando ADS [pytorch_model_catalog.ipynb](./pytorch_model_catalog.ipynb)
* Come utilizzare un modello pre-trained avanzato (EfficientNet V2)








