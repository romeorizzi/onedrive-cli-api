# onedrive-cli-api

This project offers an utility (written in python) that allow to modify the sharing profile and permissions of files and directories in your OneDrive directly from command line. The utility works on every platform (Unix,Mac,Windows) and can be run from other scripts of yours. In this way you can automate and/or automatize your workflows. Through the command line or by means of other scripts, you can now instantly and simultaneously change the permissions for all students. In this way you can readily assign to every student his own profile of permissions over a personalized set of files that differs from student to student, while avoiding to burdening things and introduce errors in the tedious and lengthy operations that would be otherwise required from the OneDrive GUI). All these syncs will now take a breeze at the start or at the end of an exam, when timing is crucial. Apart from the start or end phases of exams and competitions, this more generally helps in any other situation where appropriate timing or even just ease of use, precision, error-resiliency, and robustness might turn essential (let alone the important time savings for the operator).

A description (updated to November 2020) on how some of these operations can be performed by hand, through the standard GUI of OneDrive (as in November 2020) is contained in the file `getby.sharing_fatto_a_mano`.


## Setup of the Permissions within your Azure Account

In this section you find instructions on how to set up tokens and permissions for your OneDrive account so that our scripts can work and export their basic functionalities.

<details><summary>Setup Instructions - English</summary>

To be translated from the italian version.
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

Il sito Azure con della documentazione ufficiale sarebbe il seguente:

https://docs.microsoft.com/it-it/azure/active-directory/develop/quickstart-register-app

Ma esso si dilunga su alcune cose non di reale pertinenza per l'uso che abbiamo in mente noi: nel caso di docenti e studenti assumiamo che, per collegarsi utilmente tra di loro, siano tutti tenuti o comunque prediligano riferirsi agli account Microsoft ottenuti dall'istituzione di appartenenza. Si noti che quando questa scelta può essere adottata (o sono pochi i destinatari non coperti in questo modo), si ha poi spesso l'ulteriore benefit che gli indirizzi mail stessi (che da Azure vengono utilizzati a stregua di identificativi cui attribuire i permessi) possono essere automaticamente generati. 

In definitiva, la procedura da seguire per la prima fase (registrazione dell'app) può allora essere riassunta nella seguente:

1. Accedere al [portale di Azure](https://portal.azure.com/). Verrà chiesto di [scegliere l'account con cui procedere](figs/AzureLoginChooseAccount.png).

2. Se si appartiene ad un'istituzione che offre OneDrive, e la condivisione dei file è intesa avvenire principalmente entro l'istituzione, conviene selezionare il proprio account Azure che fa capo all'istituzione di riferimento. Ad esempio, [io entro così per conto UniVR](figs/LoginAzureUniVR.png). In ogni caso, la nostra utility e la procedura di seguito descritta possono essere utilizzate anche per ogni altro tuo account Azure.

3. Cercare e selezionare [Azure Active Directory](figs/selezionareAzureActiveDirectory.png).

4. In Gestisci selezionare Registrazioni app > Nuova registrazione.

5. Immettere un nome qualsiasi ([nello screenshot offerto d'esempio](figs/RegisterAnApplication.png) e per il proseguio di questo esempio abbiamo inserito "nomeAcasaccio") per l'applicazione cui si intenda riservare delle autorizzazioni d'accesso. Questo sarà il nome che verrà utilizzato per segnalare gli accessi, e comunque potrai sempre modificarlo in un momento successivo. Inoltre, più registrazioni di app possono condividere lo stesso nome. E' invece l'ID applicazione (CLIENT ID) generato automaticamente a identificare in modo univoco l'app all'interno della piattaforma Azure. Inoltre è fondamentale settare sempre l'URI di reindirizzamento ad una pagina con lo stesso nome scelto per l'app, in modo da permettere all'applicazione di "raccogliere" il token generato e procedere. (Nel sostro caso l'URI sarebbe `https://nomeAcasaccio.com`)

6. Dal menù si selezioni la voce `API permissions` per settare i necessari permessi per l'applicazione. Ai nostri scopi [basta assegnare i seguenti permessi](figs/PermissionsRequested.png) (alcuni forse sono superflui):

    1. [Contacts.ReadWrite](figs/ContactsPermissions.png)
    2. [Files.ReadWrite.All](figs/FilesPermissions.png)
    3. [People.Read](figs/PeoplePermissions.png)
    4. [User.Read](figs/UserPermissions.png)
    5. [User.ReadBasic.All](figs/UserPermissions.png)
    6. [User.ReadWrite](figs/UserPermissions.png)
    7. [email](OpenldPermissions.png)
    8. [openid](figs/openidPermissions.png)

abbiamo inoltre dovuto specificare non solo lo [URL come da questa schermata](figs/SetURL.png) ma anche il [domain come da questa schermata](figs/SelectDomain.png) e (ovviamente in maniera coerente con il nome scelto per l'applicazione, il nesso è illustato appunto [in questa schermata](figs/SetNameAndURIofTheApp.png) ) anche lo URI. E' probabile che anche tu dovrai immettere questi valori nelle schermate più sopra (od analoghe, purtroppo queste interfacce GUI promettono scarsa stabilità). Condividiamo la pena (ma pensate che una volta fatto questo nn dovrete più perdere il vostro tempo, i vostri click, i vostri nervi, e i vostri occhi sulle GUI di OneDrive).
Abbiamo infine dovuto settare a true (lo abbiamo trovato inizializzato a null) il campo ``allowPublicClient` di questa schermata](figs/SetManifest.png), si veda il campo dove è rimasto posizionato il cursore.


#### Other Permissions

Il quadro delle permissions che noi abbiamo trovato bastanti ai nostri scopi è il seguente:

[figura](figs/permissions_set.jpg)

You can of course set other permissions depending on your intended use.


#### Note aggiuntive

Nota: Comunque, alla prima operazione che richiede un dato permesso tra quelli impostati sopra (o comunque dopo oltre 3600 secondi da ultimo utilizzo), Azure chiede conferma di accettazione della richiesta nella fase di reindirizzamento al browser). 

Nota: da Windows (sia da cmd che da IDE, ad esempio da PyCharm), Linux (da terminale shell bash) o da Mac (da terminale shell zsh) il funzionamento è lo stesso, sia per predisporre la configurazione del client e la registrazione dell'app che per lanciare l'utility python.


</details>

## Setup of the util on your local machine

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

To be translated from the italian version.
</details>

<details><summary>Istruzioni d'Uso - Italiano</summary>
Dopo aver effettuato il [Setup dei permssi nel tuo account Azure](#setup-of-the-permissions-within-your-azure-account) e la [configurazione della util](#setup-of-the-util-on-your-local-machine), e, scaricati i pacchetti che ti verranno richiesti in quanto necssari al suo funzionamento, l'utility funziona come segue:

<details><summary>1. immissione del comando da shell</summary>


Da shell scrivo:
```bash
python3 share.py file_da_condividere buon_indirizzo_mail_destinatario tipo_condivisione
```

file_da_condividere: nome di file o folder su tuo OneDrive di cui intendi alterare lo stato di condivisione (condividere/decondividere/condividere in altra modalità)

tipo_condivisione: specifica la modalità di condivisione da settare per quel particolare file o folder e per quel particolare destinatario. Le possibili specifiche sono come da seguente tabella:

| arg_val  | tipo di condivisione  |
|---:|:---|
|  r | assegnare permesso di sola lettura    |
|  w | assegnare permesso anche di scrittura |
| -w | togliere permesso di scrittura        |
| -r | togliere anche permesso di  lettura   |

buon_indirizzo_mail_destinatario: deve essere un buon indirizzo mail nel senso che:

1. deve essere un indirizzo mail del destinatario (ovvio);

2. deve essere noto all'account OneDrive del destinatario, ossia associato al destinatario. 

Nel caso di membri (studenti, docenti, impiegati) di un ente/istituzione//azienda cui OneDrive è offerto dall'ente di appartenenza questi indirizzi saranno predeterminati nel formato e quindi automaticamente generabili.

Ad esempio, nel caso di studenti UniVR potrai indifferentemente usare:

    VR??????@studenti.univr.it

oppure

    id??????@studenti.univr.it

</details>

Nota: una volta immesso il comando (invocata la util) si apre una prima [finestra di Azure dove si richiede di sceglire l'account per l'applicazione](figs/PickAnAccount.png) seguita da una [finestra di Azure dove si richiede di immettere il codice comparso a terminale a valle dell'immissione del comando](figs/EnterCode.png). Si torni quindi al terminale (oppure alla console dell'IDE da cui si è lanciato il programma) per recuperare tale codice e, per copia ed incolla, lo si insrisca dove richiesto per l'autenticazione web.
Questa operazione va fatta solo per la prima chiamata alla util, dopodichè il sistema consentirà automaticamente tutte le operazioni a seguire per un intervallo di tempo di un'ora.

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
