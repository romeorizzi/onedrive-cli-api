# onedrive-cli-api

This project offers an utility (written in python) that allow to modify the sharing profile and permissions of files and directories in your OneDrive directly from command line. The utility works on every platform (Unix,Mac,Windows) and can be run from other scripts of yours. In this way you can automate and/or automatize your workflows. Thorough the command line or by means of other scripts, you can now instantly and simultaneously change the permissions for all students (possibly over a different set of files and assignments for every student) at the start of an exam. Apart from the start or end phases of exams and competitions, this more gnerally helps in any other situation where appropriate timing or even just ease of use, precision, error-resiliency, and robustness might turn essential (let alone the important time savings for the operator).

A description (updated to november 2020) on how some of these operations can be performed by hand, through the standard GUI of OneDrive (as in november 2020) is contained in the file `getby.sharing_fatto_a_mano`.


## Setup

In this section you find instructions on how to set up tokens and permissions for your OneDrive account so that our scripts can work and export their basic functionalities.

<details><summary>Setup Instructions - English</summary>
</details>

<details><summary>Istruzioni per il Setup - Italian</summary>
I passi da compiere sono gli stessi a prescindere dalla piattaforma (Linux/Mac/Windows).

Per utilizzare propriamente il programma, servono due codici generati dal OneDriveManager di Microsoft Azure:

> il CLIENT ID e il TENANT ID.

Entrambe queste stringhe hanno il sequente formato:

    ????????-????-????-????-????????????

ossia constano di 4 campi separati dal carattere `-`. Ogni campo è una stringa di caratteri ciascuno dei quali è una cifra oppure un carattere inglese minuscolo. L lunghezze dei campi sono: 8-4-4-4-12.

In [figura](figs/CLIENT_TENANT_ID.jpg) puoi vedere la schermata di OneDriveManager dove ti compaiono questi due codici. 

Il CLIENT ID e TENANT ID.

Per ottenere questi due codici, bisogna configurare un account CLIENT di Microsoft e poi configurare un TENANT. Dopodichè si può registrare una propria applicazione per autorizzarla ad agire sul proprio account OneDrive. Dobbiamo infatti autorizzare l'utility se vogliamo poterla utilizzare pr modificare i permessi di accesso ai nostri file su OneDrive.

Si segua questa procedura:

https://docs.microsoft.com/it-it/azure/active-directory/develop/quickstart-register-app

Preciso di settare l'URL della pagina iniziale (dopo aver regiatrato l'applicazione o in fase di registrazione): ad esempio la mia applicazione si chiama OneDriveManager e l'url è https://OneDriveManager.com
Inoltre fondamentale è settare l'URI di reindirizzamento sempre alla stessa pagina, in modo da permettere all'applicazione di "raccogliere" il token generato e procedere.
Bisogna anche settare alcuni permessi per l'applicazione (di cui viene richiesta accettazione nella fase di reindirizzamento al browser).

Questi sono i permessi richiesti (alcuni forse sono superflui):

[figura](figs/permissions_set.jpg)

Nota: il codice che scompare all'improvviso, si può reperire tornando al terminale subito dopo esser stati reindirizzati all'autenticazione web (oppure tornando alla console dell'IDE da cui si è lanciato il programma).

Nota: da Windows (sia da cmd che da IDE, ad esempio da PyCharm), Linux (da terminale shell bash) o da Mac (da terminale shell zsh) il funzionamento è lo stesso, sia per predisporre la configurazione del client e la registrazione dell'app che per lanciare l'utility python.

</details>


## Usage in action

In this section you find instructions on how to use our utility to change the sharing status of your files or folders under OneDrive. The utility can be used from within a script in order to automatize processes and make them almost instantanous (like at the start or end of an exam).

<details><summary>Usage Instructions - English</summary>
</details>

<details><summary>Istruzioni d'Uso - Italiano</summary>
Dopo aver effettuato il [Setup](#setup) e scaricati i pacchetti richiesti, l'utility funziona come segue:

<details><summary>1. immissione del comando da shell</summary>


Da shell scrivo:
```bash
python3 share.py file_da_condividere buon_indirizzo_mail_destinatario tipo_condivisione
```

file_da_condividere: nome di file o folder su tuo OneDrive di cui intendi alterare lo stato di condivisione (condividere/decondividere/condividere in altra modalità)

tipo_condivisione: specifica la modalità di condivisione da settare per quel particolare file o folder e per quel particolare destinatario. Le possibili specifiche sono come da seguente tabella:

| arg_val  | tipo di condivisione  |
|---:|:---|
|  r | solo lettura     |
|  w |  anche scrittura |

buon_indirizzo_mail_destinatario: deve essere un buon indirizzo mail nel senso che:

1. deve essere un indirizzo mail del destinatario (ovvio);

2. deve essere noto all'account OneDrive del destinatario, ossia associato al destinatario. 

Nel caso di membri (studenti, docenti, impiegati) di un ente/istituzione//azienda cui OneDrive è offerto dall'ente di appartenenza questi indirizzi saranno predeterminati nel formato e quindi automaticamente generabili.

Ad esempio, nel caso di studenti UniVR potrai indifferentemente usare:

    VR??????@studenti.univr.it

oppure

    id??????@studenti.univr.it

</details>

<details><summary>2. generazion del token</summary>

Dopo aver verificato la corrispondenza tra CLIENT_ID, TENANT_ID forniti, l'applicazione riesce a entrare in funzione e viene generato un token (che appunto viene salvato nel file token.json) che permette di interagire con l'API di OneDrive (e quindi spostare, inviare file) per 3600 secondi (ossia 100 minuti).

</details>

<details><summary>3. autorizzazione dall'account OneDrive</summary>

Sarai reindirizzato ad una pagina web dove si chiede di autorizzare l'app ad accedere ad uno specifico account OneDrive.

Dopo la vostra conferma, l'utility python esegue la sua consegna sfruttando l'API per prelevare il file.pdf e inviarlo allo studente di cui mail sopra col permesso indicato. Se il processo è andato a buon fine, su quel terminale compare riposta [200] o [201], e poi la conferma che il file è stato inviato correttamente.

</details>

<details><summary>4. comunicazione allo studente (recipient del file)</summary>

Allo studente arriverà una mail in cui, dopo essersi autenticato con le credenziali universitarie, avrà accesso al file condiviso con la modalità read.

</details>


Nota: da Windows (sia da cmd che da IDE, ad esempio da PyCharm), Linux (da terminale shell bash) o da Mac (da terminale shell zsh) il funzionamento è lo stesso, sia per predisporre la configurazione del client e la registrazione dell'app che per lanciare l'utility python.

Nota (solo privata): il codice myshare.py esmplifica l'uso. Esso contiene qualche commento in cui si evidenzia dove vadano inserit dati specifici.


</details>

 
 
## History and maintainance of this report:

Currently, we maintain two versions of our utility:

 1. share0.py:  this is the first version developed by Marco Fattorelli (also available to its GitHub repo: https://github.com/marcofattorelli/python-onedrive-api/)

 2. share.py:  this is a more recent version developed by Davide Roznowicz in order to overcome some platform dependent issues.
