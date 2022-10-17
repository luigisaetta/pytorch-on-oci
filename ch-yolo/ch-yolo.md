# Object Detection in OCI Data Science: YOLO V5

## Introduzione.
Uno dei task che spesso devono essere attuati in ambito Computer Vision è la **Object Detection**.

Quando si parla di **Object Detection** si intende l'identificazione di specifici oggetti (auto, persone, etc) all'interno di un'immagine
e l'identificazione della loro localizzazione, ovvero del rettangolo minimo (Bounding Box Rectangle) che contiene l'oggetto.

TODO: inserire esempio di Object Detection qui.

Riconoscere oggetti all'interno di un'immagine non è un compito semplice. Dipende dagli oggetti. Ma oggi si può fare e non è molto difficile.

Ma, tutta una serie di applicazioni richiedono che l'Object Detection possa essere fatta **molto velocemente**, in tempo reale, in modo da poterla applicare ad esempio ad un video 
a 60 fps. Basta immaginare tutto lo sforzo che è fatto oggi per sviluppare i sistemi a guida autonoma.

Inoltre, se si vuole addestrare un modello custom, si vuole poterlo fare con elevata accuratezza anche senza disporre di un numero elevato di immagini per ciascuna delle classi.

**YOLO** è un acronimo che sta per: "You Only Look at Once". E' stato inventato, con la prima versione dell'algoritmo, per evidenziare la sua estrema velocità.

Su YouTube è disponibile un video, che se non erro fa riferimento alla versione V2, che mostra YOLO in azione su una [famosa scena di un film di azione](https://www.youtube.com/watch?v=VOC3huqHrss)

Le prime implementazioni di YOLO, basate su una Rete Neurale (Darknet) implementata in C++, non erano semplici da utilizzare.
Tuttavia, a partire dalla v. 5 un'azienda, **Ultralytics**, ha fatto un notevole sforzo per semplificare l'adozione di YOLO ed ha messo a disposizione codice e modelli su GitHub.
Il repository GitHUb di YOLO V5 è disponibile alla seguente [URL](https://github.com/ultralytics/yolov5)

Nei paragrafi seguenti io vi mostrerò, passo passo, quali sono le operazioni da compiere per effettuare il training di un modello custom, in **OCI Data Science**, e come utilizzare il modello per l'inferenza.

Ovviamente, per avere la velocità in fase di inferenza, è indispensabile utilizzare un'ambiente con GPU. INoltre, la GPU diviene indispensabile se si vuole effettuare il training di un modello custom, altrimenti il tempo per il training può essere molto lungo.

## Installazione di YOLO V5.
Abbiamo già a disposizione, dopo aver eseguito i passi descritti nel cap. 1, una Notebook Session con GPU P100. Adesso, i passi che dobbiamo compiere sono necessari per avere un **ambiente software completo** e, in particolare, disporre delle librerie comunemente utilizzate per la **Computer Vision**.

Innanzututto, conviene attivare un nuovo dedicato ambiente conda, a partire da un ambiente, messo a disposizione da OCI Data Science, specializzato per la Computer Vision.
L'ambiente da cui partiamo è: **Computer Vision for GPU on Python 3.7**.

Il comando che andiamo ad eseguire nel terminal è:
```
odsc conda install -s computervision_p37_gpu_v1
```
ed, al termine, eseguiamo il comando:
```
conda activate /home/datascience/conda/computervision_p37_gpu_v1
```
A questo punto, cloniamo nella Notebook Session il repository GitHub di Ultralytics
```
git clone https://github.com/ultralytics/yolov5
```
e, dopo esserci collocati nella directory yolov5
```
cd yolov5
```
effettuiamo gli upgrade richiesti da yolov5:
```
pip install -r requirements.txt
```
Al termine, se vogliamo essere super-precisi, rieseguiamo (utilizzando il kernel per la Computer Vision) il Notebook check_pytorch_and_gpu.

L'installazione è terminata e siamo pronti per utilizzare un modello pre-trained, disponibile sul PyTorch Hub.

## Un primo test di YOLO V5.
L'ambiente è pronto e, prima di lanciarci nell'avventura dell'addestramento di un modello custom, possiamo divertirci ad utilizzare un **modello pre-trained**.

Ovviamente, un modello pre-trained sarà in grado di identificare soltanto gli oggetti delle classi per cui è stato addestrato. Normalmente, YOLO è addestrato sul dataset
[COCO](https://cocodataset.org/#home).

Possiamo utilizzare le istruzioni di esempio fornite sul GitHub di Ultralytics.
```
import torch

# the model is loaded from the PyTorch HUB
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5n - yolov5x6, custom

# Image: we take an example from the Ultralytics site
img = 'https://ultralytics.com/images/zidane.jpg'

# Inference
results = model(img)

# Results: prints only text with number and type of Object detected
results.print()

# shows the image with BB rectangles
results.show()
```
Un mio Notebook con il codice è disponibile [qui](./yolo_inference_one.ipynb).

Nota: il modello pre-trained che abbiamo selezionato è il più "leggero" disponibile. Se vogliamo aumentare l'accuratezza e lavorare con immagini con risoluzione più alta, possiamo utilizzare gli altri modelli. Ovviamente, è necessaria maggiore capacità computazionale e, sullo stesso HW, l'inferenza sarà un pò pù lenta.
I modelli pre-trained disponibili sono elencati [qui](https://github.com/ultralytics/yolov5#pretrained-checkpoints).

## Custom training: dove è necessario uno sforzo.
Proviamo ora a fare il passo successivo: vogliamo addestrare un **modello custom**, per poter riconoscere all'interno di immagini gli oggetti che ci interessano per il nostro, concreto, caso d'uso. E, vogliamo usare YOLO V5.

Cosa manca, dopo l'installazione ed i passaggi fatti fino ad ora?

Facciamo un passaggio indietro: nel Deep Learning, ed in generale nel Machine Learning, la **conoscenza all'interno di un modello è portata dal dataset** su cui il modello è stato addestrato.

Possiamo utilizzare il **Transfer Learning** per velocizzare l'addestramento. Ovvero, possiamo partire da un modello pre-trained su un dataset che contiene oggetti ma non quelli di specifico interesse. Ed il Transfer Learning in Computer Vision è uno strumento potente, da utilizzare.

Ma, per avere un modello che, con l'accuratezza richiesta, sia in grado di riconoscere e localizzare i nostri oggetti di interesse, dobbiamo fare un **fine-tuning** del modello su un dataset "labeled" che contenga i nostri oggetti di interesse.

E l'impegno necessario riguarda l'operazione di **"labeling"** del dataset. Ovvero: dobbiamo avere a disposizione almeno un centinaio di immagini che contengano i nostri oggetti, dobbiamo intorno a questi oggetti disegnare il Bounding Box Rectangle ed associare la classe corretta.

Per il labeling vi sono molti tool, anche gratuiti, a disposizione. Una "Data Labeling Application" è disponibile in OCI Data Science.

Ma, poichè molti di voi potrebbero preferire l'utilizzo di strumenti Open, liberamente disponibili, vi porterò l'esempio di [Roboflow](https://roboflow.com/).

Per progetti "non commerciali" potete utilizzare Roboflow. Dovete soltanto registrarvi. Poi, potrete effettuare la creazione di un progetto, effettuare: 
* l'upload delle immagini
* disegnare i BB rectangles
* associare ad essi le classi
* esportare il dataset in formato YOLO V5.

Roboflow semplifica anche l'esportazione. Genera automaticamente il codice, che potrete utilizzare in un Notebook, per scaricare il dataset (in formato YOLO V5) all'interno della Notebook Session che abbiamo preparato.

Quindi: l'unico sforzo richiesto è di avere la pazienza di collezionare un insieme abbastanza grande e variegato di immagini e di effettuare il labeling di tali immagini.

**Quante immagini?** Eh, è una domanda che spesso mi viene posta. Non esiste una riposta valida per qualunque scenario (ricordiamo gli insegnamenti del "NO free-lunch theorem").

In alcuni casi **un centinaio di immagini possono essere sufficienti**. Ma devono presentare gli oggetti da riconoscere ed identificare nelle più varie condizioni di reale utilizzo. Inoltre, dipende dall'accuratezza che si vuole ottenere. Regola generale: più immagini si hanno e meglio è.

## Il formato YOLO V5
Prima di passare al training vero e proprio, diamo uno sguardo attento al **dataset in formato YOLO V5**. E' importante capire come è strutturato, in modo da poter identificare rapidamente e correggere eventuali problemi.

Innanzitutto, il dataset deve essere stato suddiviso in tre "split":
* train dataset
* validation dataset
* test dataset

Le prime due parti sono utilizzate durante il training. Nel training la misura delle metriche per la **Precision, Recall ed mAP** sono fatte sul dataset di validazione.

Il dataset di test non è utilizzato durante il training, ma lo possiiamo utilizzare alla fine per capire quanto il nostro modello è in grado di generalizzare.

Un primo file di cui dobbiamo registrare la collocazione (il pathname completo) è il file data.yaml
In questo file troviamo l'elenco delle classi di oggetti ed i link per i dataset di train e validation. Riporto un esempio, con due classi

```
names:
- barcode
- qrcode
nc: 2
train: BarCode-detector-6/train/images
val: BarCode-detector-6/valid/images
```

Un mio suggerimento: i percorsi per train e validation sono relativi. Per evitare inutili complicazioni sostituiamoli con i percorsi assoluti.

Se ci spostiamo nella cartella "train" /analogo discorso per validation e test) vi troviamo due sotto-cartelle: una contenente le immagini e l'altra contenente i file con la specifica della posizione di BB rectangles.

nella cartella labels per ciascun file jpeg contenuto nella cartella "images" troviamo un file associato, con eguale nome ma estensione ".txt".
In questo file troveremo una riga distinta per ciascun oggetto identificato.

Il formato è:
codice-classe xc yc width height

Esempio:
1 0.61171875 0.49921875 0.11953125 0.16640625
0 0.64609375 0.22734375 0.28671875 0.03984375
0 0.8328125 0.2890625 0.1109375 0.04453125

In base all'esempio data.yaml di sopra concludiamo che la prima riga è relativa ad un qrcode e le altre a barcodes.

E' importante notare che le coordinate x ed y, cosi come larghezza ed altezza, sono normalizzate. Xc ed yc identificano il centro del BB rectangle.
Per tornare ai valori assoluti (pixel) si deve:
* moltiplicare xc e width per la larghezza, in pixel, dell'immagine
* moltiplicare yc ed height per l'altezza, sempre in pixel, dell'immagine.

Quindi: concludendo:
* attenzione ai percorsi dei file e directory, a parteire da data.yaml
* per ogni immagine, il labeling è contenuto in un file txt associato; Nel file abbiamo una iga per oggetto, nel formato sopra specificato


























