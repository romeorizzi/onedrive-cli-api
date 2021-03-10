# onedrive-cli-api

This project offers an utility (written in python) that allow to modify the sharing profile and permissions of files and directories in your OneDrive directly from command line. The utility works on every platform (Unix,Mac,Windows) and can be run from other scripts of yours. In this way you can automate and/or automatize your workflows. Through the command line or by means of other scripts, you can now instantly and simultaneously (and with no risk of introducing errors) change the permissions for all students (possibly over a different set of files and assignments for every student) at the start of an exam. Apart from the start or end phases of exams and competitions, this more generally helps in any other situation where appropriate timing or even just ease of use, precision, error-resiliency, and robustness might turn essential (let alone the important time savings for the operator).

A description (updated to November 2020) on how some of these operations can be performed by hand, through the standard GUI of OneDrive (as in November 2020) is contained in the file `getby.sharing_fatto_a_mano`.


## Setup

In this section you find instructions on how to set up tokens and permissions for your OneDrive account so that our scripts can work and export their basic functionalities.

<details><summary>Setup Instructions - English</summary>
</details>

<details><summary>Istruzioni per il Setup - Italian</summary>

I passi da compiere sono gli stessi a prescindere dalla piattaforma (Linux/Mac/Windows).

Per utilizzare propriamente il programma, servono due codici generati dal OneDriveManager di Microsoft Azure:

1. CLIENT ID
2. TENANT ID

Entrambe queste stringhe hanno il sequente formato:

    ????????-????-????-????-????????????

ossia constano di 4 campi separati dal carattere `-`. Ogni campo è una stringa di caratteri ciascuno dei quali è una cifra oppure un carattere inglese minuscolo. Le lunghezze dei campi sono: 8-4-4-4-12.

In [figura](figs/OverviewRegisteredApplication2.png) puoi vedere la schermata di OneDriveManager dove ti compaiono questi due codici (CLIENT ID e TENANT ID).

Per ottenere questi due codici, bisogna configurare un account CLIENT di Microsoft e poi configurare un TENANT. Dopodichè si può registrare una propria applicazione per autorizzarla ad agire sul proprio account OneDrive. Dobbiamo infatti autorizzare l'utility se vogliamo poterla utilizzare pr modificare i permessi di accesso ai nostri file su OneDrive.

Il sito ufficiale (ma si dilunga su alcun cose non di vostra pertinenza, nel caso di docenti e studenti assumiamo che, per collegarsi utilmente tra loro, si riferiscano tutti agli accont Microsoft ottenuti dall'istituzione di appartenenza) sarebbe il seguente:

https://docs.microsoft.com/it-it/azure/active-directory/develop/quickstart-register-app

In definitiva, la procedura da seguire per questa prima fase sarebbe la seguente:

Per creare la registrazione dell'app, seguire questa procedura:

1. Accedere al [portale di Azure](https://portal.azure.com/).

2. Si selezioni il proprio account Azure che fa capo all'istituzione di riferimento (questa procedura e questa utility possono essere utilizzate anche per ogni altro tuo account Azure, ma assumiamo qui che il lettore sia interessato a condividere con persone della propria istituzione, nel quale caso potrà quindi avvalersi della conoscenza implicita degli indirizzi mail (ad sempio, per gli studenti UniVR essi sono della forma <matricola>@studenti.univr.it). Consigliamo pertanto di procedere con l'account dell'istituzione.

3. Cercare e selezionare Azure Active Directory.

4. In Gestisci selezionare Registrazioni app > Nuova registrazione.

5. Immettere un nome qualsiasi (negli screenshots offerti d'esempio abbiamo inserito "nomeAcasaccio") per l'applicazione cui si intenda riservare delle autorizzazioni d'accesso. Questo sarà il nome che verrà utilizzato per segnalare gli accessi, e comunque potrai sempre modificarlo in un momento successivo. Inoltre, più registrazioni di app possono condividere lo stesso nome. E' invece l'ID applicazione (CLIENT ID) generato automaticamente a identificare in modo univoco l'app all'interno della piattaforma Azure. Inoltre è fondamentale settare sempre l'URI di reindirizzamento ad una pagina con lo stesso nome scelto per l'app, in modo da permettere all'applicazione di "raccogliere" il token generato e procedere. (Nel sostro caso l'URI sarebbe `https://nomeAcasaccio.com`)

6. Dal menù si selezioni la voce `API permissions` per settare i necessari permessi per l'applicazione. Ai nostri scopi basta assegnare i seguenti permessi (alcuni forse sono superflui):

```
Contacts.ReadWrite
Files.ReadWrite.All
People.Read
User.Read
User.ReadBasic.All
User.ReadWrite
email
openid
```

[figura](figs/permissions_set.jpg)

Nota: Comunque, alla prima operazione che richiede un dato permesso tra quelli impostati sopra (o comunque dopo oltre 3600 secondi da ultimo utilizzo), Azure chiede conferma di accettazione della richiesta nella fase di reindirizzamento al browser). 

Nota: da Windows (sia da cmd che da IDE, ad esempio da PyCharm), Linux (da terminale shell bash) o da Mac (da terminale shell zsh) il funzionamento è lo stesso, sia per predisporre la configurazione del client e la registrazione dell'app che per lanciare l'utility python.


</details>

## Setup of the util

```bash
cp data_for_user_customization_template.py  data_for_user_customization.py
```
and in the new and personal file `data_for_user_customization.py` fill up the two fields:

1. CLIENT ID
2. TENANT ID

with your secret data. (You find them in the Overview Tab of your Microsoft Azure Account).


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

Nota: il codice che scompare all'improvviso, si può reperire tornando al terminale subito dopo esser stati reindirizzati all'autenticazione web (oppure tornando alla console dell'IDE da cui si è lanciato il programma).


<details><summary>2. generazione del token</summary>

Dopo aver verificato la corrispondenza tra CLIENT_ID, TENANT_ID forniti, l'applicazione riesce a entrare in funzione e viene generato un token. Questo token viene salvato nel file `token.json` e permette di interagire con l'API di OneDrive (e quindi spostare, e inviare/condividere file) per 3600 secondi (ossia 100 minuti).

</details>

<details><summary>3. autorizzazione dall'account OneDrive</summary>

Sarai reindirizzato ad una pagina web dove si chiede di autorizzare l'app ad accedere ad uno specifico account OneDrive.

Dopo la vostra conferma, l'utility python esegue la sua consegna sfruttando l'API per condividere un file specificato con lo studente registrato a OneDrive con la mail specificata, ed attribuendo ad esso il permesso indicato (r=sola lettura, w=lettura e scrittura). Se il processo è andato a buon fine, su quel terminale compare riposta [200] o [201], e poi la conferma che il file è stato inviato correttamente.

</details>

<details><summary>4. comunicazione allo studente (recipient del file)</summary>

Allo studente arriverà una mail in cui, dopo essersi autenticato con le credenziali universitarie, avrà accesso al file condiviso con la modalità read.

</details>


Nota: da Windows (sia da cmd che da IDE, ad esempio da PyCharm), Linux (da terminale shell bash) o da Mac (da terminale shell zsh) il funzionamento è lo stesso, sia per predisporre la configurazione del client e la registrazione dell'app che per lanciare l'utility python.

Nota (solo privata): lo script `myshare.py` esemplifica l'uso. Esso contiene qualche commento in cui si evidenzia dove vadano inseriti i dati che è necessario specificare.


</details>

 
 
## History and maintainance of this report:

Currently, we maintain two versions of our utility:

 1. share0.py:  this is the first version developed by Marco Fattorelli (also available to its GitHub repo: https://github.com/marcofattorelli/python-onedrive-api/)

 2. share.py:  this is a more recent version developed by Davide Roznowicz in order to overcome some platform dependent issues.
