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

**Quante immagini?** Eh, è una domanda frequente. Non esiste una risposta valida per qualunque scenario (ricordiamo gli insegnamenti del "NO free-lunch theorem").

In alcuni casi **un centinaio di immagini possono essere sufficienti**. Ma devono presentare gli oggetti da riconoscere ed identificare nelle più varie condizioni di reale utilizzo. Inoltre, dipende dall'accuratezza che si vuole ottenere. Regola generale: più immagini si hanno e meglio è.

## Il formato YOLO V5
Prima di passare al training vero e proprio, diamo uno sguardo attento al **dataset in formato YOLO V5**. E' importante capire come è strutturato, in modo da poter identificare rapidamente e correggere eventuali problemi.

Innanzitutto, il dataset deve essere stato suddiviso in tre "split":
* train dataset
* validation dataset
* test dataset

Le prime due parti sono utilizzate durante il training. Nel training la misura delle metriche per la **Precision, Recall ed mAP** sono fatte sul dataset di validazione.

Il dataset di test non è utilizzato durante il training, ma lo possiiamo utilizzare alla fine per capire quanto il nostro modello è in grado di generalizzare.

Un primo file di cui dobbiamo registrare la collocazione (il pathname completo) è il file data.yaml.
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

Se ci spostiamo nella cartella "train" (analogo discorso per validation e test) vi troviamo due sotto-cartelle: una contenente le immagini e l'altra contenente i file con la specifica della posizione dei BB rectangles.

Nella cartella labels, per ciascun file jpeg contenuto nella cartella "images" troviamo un file associato, con eguale nome ma estensione ".txt".
In questo file troveremo una riga distinta per ciascun oggetto identificato.

Il formato è:
codice-classe xc yc width height

Esempio:
```
1 0.61171875 0.49921875 0.11953125 0.16640625
0 0.64609375 0.22734375 0.28671875 0.03984375
0 0.8328125 0.2890625 0.1109375 0.04453125
```

In base all'esempio data.yaml di sopra concludiamo che la prima riga è relativa ad un qrcode (1) e le altre a barcodes (0).

E' importante notare che le coordinate x ed y, cosi come larghezza ed altezza, sono normalizzate. Xc ed yc identificano il centro del BB rectangle.
Per tornare ai valori assoluti (pixel) si deve:
* moltiplicare xc e width per la larghezza, in pixel, dell'immagine
* moltiplicare yc ed height per l'altezza, sempre in pixel, dell'immagine.

Quindi: concludendo:
* attenzione ai percorsi dei file e directory, a partire da data.yaml
* per ogni immagine, il labeling è contenuto in un file txt associato; Nel file abbiamo una riga per oggetto, nel formato sopra specificato

## Custom training.
Abbiamo installato tutte le librerie richieste da YOLO V5, abbiamo effettuato il labeling del dataset, abbiamo portato il dataset, in formato YOLO V5, all'interno di una crtella dedicata nella nostra Notebook Session. A questo punto abbiamo tutti gli ingredienti, pronti, per lanciare una prima sessione di addestramento.

I passi seguenti saranno fatti dal terminal. Ricordiamo di attivare l'ambiente conda che abbiamo preparato, con il comando:
```
conda activate /home/datascience/conda/computervision_p37_gpu_v1
```
A questo punto, spostiamoci nella directory yolov5, ottenuta dal clone del repository GitHub di Ultralytics.

In questa directory troveremo lo script python (train.py)che utilizzeremo per il training.

Dobbiamo scegliere il modello pre-trained da utilizzare. Per velocizzare, essendo un primo tentativo, utilizziamo **yolov5s.pt**.

Il comando da lanciare è:
```
python train.py --img 640 --batch 8 --epochs 60 --data /home/datascience/barcode-dataset/BarCode-detector-6/data.yaml --weights yolov5s.pt
```

Esaminiamolo:
* specifichiamo (640) le dimensioni in pixel delle immagini, scalate, su cui il modello lavora. Dipende da quale modello pre-trained usiamo
* ho abbassato il batch_size (8) per evitare OOM sulla GPU
* ho specificato 60 epochs
* data: contiene il persorso assoluto del file data.yaml (vedi sopra)
* infine: weights definisce il modello pre-trained

Nel mio caso utilizzando il modello "small" e con 60 epochs riesco ad ottenere, in circa 3 minuti, un buon risultato.
La valutazione sul dataset di "validation" riporta:
```
Model summary: 157 layers, 7015519 parameters, 0 gradients, 15.8 GFLOPs
                 Class     Images  Instances          P          R      mAP50   mAP50-95: 100%|██████████| 2/2 [00:00<00:00,  5.75it/s]                                              
                   all         21        163      0.835      0.923      0.951      0.612
               barcode         21        143      0.872       0.86      0.924      0.572
                qrcode         21         20      0.798      0.986      0.978      0.652
```

ovvero: una **Recall** pari a 0.99 ed una **Precision** pari a 0.80. Un risultato abbastanza buono.

Possiamo fare meglio? Dipende dal caso esaminato e dal dataset. Nel mio caso si. Utilizzando un modello "large" ed 80 epochs riesco ad ottenre i seguenti risultati:

|Class     |Images  |Instances      |P          |R       |mAP50   |mAP50-95 |
|----------|--------|---------------|-----------|--------|--------|---------|
|   all    |   21   |      163      |   0.966   |  0.962 |  0.979 |   0.78  |
| barcode  |   21   |      143      |   0.945   |  0.923 |  0.963 |   0.712 |
| qrcode   |   21   |      20       |   0.987   |  1     |  0.995 |   0.849 |

Il risultato dell'addestramento è salvato in una sottodirectory all'interno della directory runs/train. Il file è best.pt (pt sta per PyTorch).

## Inferenza con il modello custom addestrato.
Rispetto al Notebook esaminato nella sezione "Un primo Test di YOLO V5", l'unico cambiamento necessario riguarda il codice per caricare il modello custom:

```
# Model path: the dir with best.pt from training
MODEL_PATH = "/home/datascience/yolov5/runs/train/exp5/weights/best.pt"

model = torch.hub.load("ultralytics/yolov5", "custom", path=MODEL_PATH)
```

Il Notebook [yolo_custom_inference](./yolo_custom_inference.ipynb) contiene il codice di esempio completo.

## Approfondimento: Precision e Recall.
I termini **Precision** e **Recall** compaiono spesso quando si analizzano le prestazioni di modelli che devono "classificare oggetti".

Consideriamo un esempio "classico" di modello di classificazione: un modello diagnostico, che a partire da una serie di dati istologici vuole identificare se il campione è indicativo di una possibile forma di cancro (caso positivo) oppure no (negativo). (Potremmo star lavorando sul famoso Breast Cancer Dataset).

Se il campione è realmente positivo il nostro modello può prevedere positivo ed avremo un Vero Positivo (TP) oppure può prevedere negativo ed avremo un Falso Negativo (FN).

Se il campione è negativo il modello può prevedere correttamente negativo ed avremo Vero Negativo (TN) oppure può prevedere positivo ed avremo un Falso Positivo (FP).

La **Recall** misura la capacità del modello ad identificare correttamente i casi positivi. Ovvero, se il caso è positivo qual è la probabilità (condizionata) che il modello dica positivo? E' la Recall.

La **Precision** misura invece la probabilità che un caso indicato come positivo sia realmente positivo.

Nel caso dell'Object Detection la Recall ci dice quanto il modello è bravo ad identificare un barcode come tale (oppure un qrcode). Quindi una Recall eguale ad 1 vuol dire: tutti i barcode sono identificati e tutti i Qrcode sono identificati. 
Ma potrebbero esservi FP. Ovvero, il modello potrebbe identificare porzioni di immagine e dire: contengono barcode, sbagliando.
Quanto più alta è la Precision tanto meno sono i FP.

Se preferite le formule, come me, le potete trovare su [Wikipedia](https://en.wikipedia.org/wiki/Precision_and_recall).

Per coloro che lavorano in ambito biomedicale, al posto di Recall si utilizza **"Sensitivity"**: l'abilita di un modello di identificare tutti i casi positivi.

In italiano Sensitivity si traduce con **Sensibilità**. Per darvi un'idea concreta, negli ultimi due anni abbiamo spesso sentito perlare della Sensibilità dei test diagnostici per il COVID19.






























