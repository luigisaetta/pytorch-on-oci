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

L'installazione è terminate e siamo pronti per utilizzare un modello pre-trained, disponibile sul PyTorch Hub.

## Un primo test di YOLO V5.
L'ambiente è pronto e, prima di lanciarci nell'avventura dell'addestramento di un modello custom, possiamo divertirci ad utilizzare un **modello pre-trained**.

Ovviamente, un modello pre-trained sarà in grado di identificare soltanto gli oggetti delle classi per cui è stato addestrato. Normalmente, YOLO è addestrato sul dataset
[COCO](https://cocodataset.org/#home).

Possiamo utilizzare le istruzioni di esempio fornite sul GitHub di Ultralytics.
```
import torch

# the model is loaded from the PyTorch HUB
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5n - yolov5x6, custom

# Image: we take an exaample from the Ultralytics site
img = 'https://ultralytics.com/images/zidane.jpg'

# Inference
results = model(img)

# Results: prints only text with number and type of Object detected
results.print()

# shows the image with BB rectangles
results.show()
```
Un Notebook con il codice è disponibile [qui](./yolo_inference_one.ipynb)









