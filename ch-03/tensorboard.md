# Utilizzare TensorBoard in OCI Data Science

## Introduzione

Durante o al termine di una session di training, è importante esaminare l'andamento, nel corso delle epochs, di
una serie di metriche (loss, validation_loss, ...) per capire se l'apprendimento procede, se vi sono segnali di overfitting.

Con PyTorch, ed in particolare (vedi cap. 4) con PyTorch Lightning, è abbastanza semplice salvare i valori di tali metriche in un file di log.

Uno strumento che è spesso utilizzato, in combinazione con PyTorch, per visualizzare l'andamento delle metriche è **TensorBoard**.

Tuttavia, l'utilizzo di una Notebook Session per l'addestramento comporta una complicazione: non è possibile eseguire Tensorboard all'interno della NB session, come faremmo all'interno di una normale VM, perchè la NB session non consente l'accesso alla porta su cui il server di TensorBoard è in ascolto.

Dalla versione **2.6.8** di ADS vi è una soluzione praticabile, descritta nella documentazione ufficiale di ADS.

La soluzione, in sintesi, prevede:
* il salvataggio dei logs prodotti nel ciclo di training in un bucket dell'Object Storage
* l'esecuzione di Tensorboard sulla propria workstation (od anche in una VM Linux su OCI Cloud)
* l'accesso ai log salvati nel bucket


## La documentazione

La documentazione ufficiale di PyTorch per configurare l'impiego di TensorBoard è disponibile [qui](https://pytorch.org/tutorials/recipes/recipes/tensorboard_with_pytorch.html).

La documentazione per utilizzare TensorBoard insieme ad OCI Data Science è disponibile [qui](https://docs.oracle.com/en-us/iaas/tools/ads-sdk/latest/user_guide/model_training/tensorboard/tensorboard.html).

