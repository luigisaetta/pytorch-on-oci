# Autorizzazioni e sicurezza in OCI Data Science

## Introduzione.

Il tema della sicurezza è un tema molto ampio e, per ragioni di tempo e spazio, non posso certamente esaurirlo nell'ambito di questo progetto.

Tuttavia, la mia esperienza con oramai decine di clienti, che utilizzano il nostro Cloud e la nostra piattaforma OCI Data Science, ha mostrato che spesso essi hanno difficoltà e non riescono ad utilizzare rapidamente le risorse Cloud a seguito di una visione no completamente chiara di come gestire tematiche legate alle autorizzazioni all'utilizzo dei servizi. 

In questa nota, proverò ad essere il più possibile chiaro e a fornire tutte le informazioni utili e necessarie per poter impostare le autorizzazioni e consentire al team di Data Scientist di essere rapidamente produttivi.

## I servizi Cloud coinvolti.

Innanzitutto, deve essere chiaro che per poter lavorare, non si utilizzano solo le funzionalità di OCI Data Science.

Normalmente, in un progetto **serio** si utilizzano:
* Oracle Database (tipicamente come OCI Autonomous DWH)
* Object Storage
* OCI Logging

ed è possibile che si utilizzino altri servizi:
* MySQL Cloud Service
* OCI Streaming
* OCI Data Integration
* OCI AI Services (OCI Vision, OCI Language...)

e quindi le autorizzazioni devono consentire a chi usa le Notebook Session di accedere a tali servizi.

## Chiavi o Resource Principal?

Ecco il primo punto da cui partire: i controlli di sicurezza, nel momento in cui è richiesto l'accesso ad un servizio (ad esempio: Object Storage) devono controllare se chi chiede di accedere è autorizzato a farlo. E, teniamo presente che, di default tutto è bloccato se non esplicitamente autorizzato.

A questo punto vi sono due possibilità:
* si autorizza direttamente la persona
* si autorizza la risorsa (es: il Notebook) il cui codice richiede l'accesso

Il secondo meccanismo è detto **"Resource Principal" (RP)**

Se si vuole utilizzare il primo meccanismo, la persona che esegue il codice dovrà fornire una **coppia di chiavi** (pubblica, privata) e la chiave privata è utilizzata per firmare tutte le chiamate REST (l'accesso ai servizi Cloud all fine comporta sempre REST call).
Questo è l'unico meccanismo disponibile se si vogliono invocare servizi Cloud al di fuori di OCI Data Science (ad esempio da codice che gira sul proprio portatile).

Se si lavora all'interno di OCI Data Science il meccanismo **più semplice** e più comunemente utilizzato è il Resource Principal.

## I passi da compiere per utilizzare Resource Principal.

Il meccanismo di Resource Principal, in pratica, consente di autorizzare il Notebook che si sta eseguendo.

Quindi, lo scenario è il seguente: il Data Scientist è autorizzato ad accedere alla Notebook Session ed eseguire il Notebook. Il Notebook, a sua volta, è autorizzato ad accedere, ad esempio, a:
* Object Storage
* Logging Service
* OCI Vision
* etc...

I passi di configurazione, che devono essere eseguiti da un OCI Admin, sono i seguenti:
1. Creazione di un **compartimento** dedicato al team di Data Scientist ed alle loro risorse
2. Creazione di un **gruppo di utenti**, in cui andranno inseriti gli account di tutti i membri del team
3. Creazione di un **Dynamic Group**, in cui vanno inserite le "risorse" da autorizzare
4. Definizione di un **insieme di Policy**, che autorizzano

## Compartimento

E' un raggruppamento logico di risorse. Conviene colocare le risorse (progetti, Notebook Session, bucket) nello stesso compratimento in modo da poter applicare in modo relativamente semplice le policy e poter gestire il monitoraggio del consumo di risorse (per il billing, ad esempio)

Come ogni risorsa in OCI, il compartimento oltre ad un nome ha un identificativo, detto OCID. Prendiamone nota, perchè dovremo utilizzarlo.

## Dynamic Group.

E' nel Dynamic Group che andremo ad inserire tutte le "risorse" che vogliamo utilizzare.

Perchè dinamico? Perchè nel tempo aggiungeremo, ad esempio, Notebook Sessions (o progetti) e ovviamente non vogliamo dover rivedere le policy ogni volta.

La definizione del Dinamyc Group quindi dirà qualcosa del genere: "nel dynamic group DataScienceDG vi sono tutte le Notebook Session create nel compartimento DSCompartment"

Il nostro OCI Admin dovrà quindi creare un Dynamic Group con un istruzione del tipo:
```
ALL {resource.type='datasciencenotebooksession',resource.compartment.id='ocid1.compartment.oc1..aaaaaaaag2cpni5qj6li5ny6ehuahhepbpveopobooayqfeudqygdtfexyzx'}
```
laddove in resource.compartment.id abbiamo specificato l'OCID del nostro compartimento.

Se nel nostro lavoro vogliamo anche utilizzare i JOBS, per eseguire codice in modalità batch, dovremo inserire un'altra specifica nella definizione del Dynamic Group"
```
ALL {resource.type='datasciencejobrun', resource.compartment.id='ocid1.compartment.oc1..aaaaaaaag2cpni5qj6li5ny6ehuahhepbpveopobooayqfeudqygdtfexyzx'}
```

Preciso che i Dynamic Group sono globali, non ristretti ad un compartimento.

Una nota importante, che deriva dalla mia esperienza: si deve fare molta attenzione nello scrivere le definizioni di cui sopra. Un errore non sempre è segnalato e può far perdere molto tempo.

## Le Policy

A questo punto, le policy autorizzeranno il Dynamic Group.

Alcune policy sono definite a livello di root compartment (e valgono per tutti gli altri compartimenti). Altre policy possono essere definite a livello del singolo compartimento.

Per semplificare, riporto la lista di policy minime che, secondo me, vanno definite, per poter lavorare, a livello del nostro compartimento (che abbiamo chiamato DSCompartment)
```
allow dynamic-group DataScienceDG to manage data-science-family in compartment DSCompartment
allow dynamic-group DataScienceDG to manage data-science-models in compartment DSCompartment
allow dynamic-group DataScienceDG to manage object-family in compartment DSCompartment
allow dynamic-group DataScienceDG to manage objects in compartment DSCompartment
allow dynamic-group DataScienceDG to use log-groups in compartment DSCompartment
allow dynamic-group DataScienceDG to use log-content in compartment DSCompartment
```