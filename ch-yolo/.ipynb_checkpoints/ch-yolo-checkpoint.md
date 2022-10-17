# Object Detection in OCI Data Science: YOLO V5

## Introduzione.
Uno dei task che spesso devono essere attuati in ambito Computer Vision è la **Object Detection**.

Quando si parla di **Object Detection** sin intende l'identificazione di specifici oggetti (auto, persone, etc) all'interno di un'immagine
e l'identificazione della loro localizzazione, ovvero del rettangolo minimo (Bounding Box Rectangle) che contiene l'oggetto.

TODO: inserire esempio di Object Detection qui.

Riconoscere oggetti all'interno di un'immagine non è un compito semplice. Dipende dagli oggetti. Ma oggi si può fare e non è molto difficile.

Ma, tutta una serie di applicazioni richiedono che l'Object Detection possa essere fatta **molto velocemente**, in tempo reale, in modo da poterla applicare ad esempio ad un video 
a 60 fps. Basta immaginare tutto lo sforzo che è fatto oggi per sviluppare i sistemi a guida autonoma.

Inoltre, se si vuole addestrare un modello custom, si vuole poterlo fare con elevata accuratezza anche senza poter disporre di un numero elevato di immagini per ciascuna delle classi.

YOLO è un acronimo che sta per: "You Only Look at Once". E' stato inventato, con la prima versione dell'algoritmo, per evidenziare la sua estrema velocità.

Su YouTube è disponibile un video, che se non erro fa riferimento alla versione V2, che mostra YOLO in azione su una [famosa scena di un film di azione](https://www.youtube.com/watch?v=VOC3huqHrss)

Le prime implementazioni di YOLO non erano semplici da utilizzare, basate su una Rete Neurale (Darknet) implementata in C++.
Tuttavia, a partire dalla v. 5 un'azienda, Ultralytics, ha fatto un notevole sforzo per semplificare l'adozione di YOLO ed ha messo a disposizione codice e modelli su GitHub.
Il repository GitHUb di YOLO V5 è disponibile alla seguente [URL](https://github.com/ultralytics/yolov5)

Nei paragrafi seguenti io vi mostrerò, passo passo, quali sono le operazioni da compiere per effettuare il training di un modelo custom, in OCI Data Science, e come utilizzare il modello per l'inferenza.

## Installazione di YOLO V5.







