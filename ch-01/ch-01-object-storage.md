# Object Storage

## Introduzione.

Il posto migliore dove collocare un insieme di files (es: immagini), per salvare in modo affidabile una copia e condividerla 
con tutti i membri del nostro team di lavoro, è **l'Object Storage**.

L'Object Storage ha tutta una serie di vantaggi:
* il costo per GB è estremamente basso
* Lo storage è ridondato
* E' possibile accedere ai bucket da più Notebook Session e quindi condividere i file

## Trasferimento dei file.

Ovviamente, se dobbiamo addestrare una Rete Neurale ed elaborare migliaia di immagini conviene effettuare una copia locale, 
nello storage della Notebook Session, e lavorare sulla copia locale.

Per semplificare il lavoro dei Data Scientist, nel file [utils.py](./utils.py) ho collocato alcune funzioni che rendono semplice
la copia da/per l'Object Storage.

Nel Notebook [files_and_object_storage.ipynb](./files_and_object_storage.ipynb) mostro come utilizzare queste funzioni.

## Impiego di Ocifs.

TODO

