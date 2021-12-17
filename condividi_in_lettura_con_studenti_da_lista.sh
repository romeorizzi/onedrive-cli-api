#!/bin/bash
# nota: questo script è pensato (e testato) per essere lanciato dal folder in cui si trova (in locale, il folder ~/OneDrive) che è il mounting point in locale del mio intero OneDrive Microsoft.
# primo argomento: la data della sessione di esame (esempio: 2021-09-28)
# argomenti sucessivi: la sequenza di ID_students ai quali vuoi dare accesso in SOLA LETTURA alla cartella col loro tema + tua correzzione + file tabellone_punteggi_con_voti.pdf

# UN POSSIBILE MODO DI CHIAMARE QUESTO SCRIPT (dopo esserti ricopiato in locale un .csv quale ad esempio  profilo_esercizi_per_studente_submitted.csv):
# ./condividi_in_lettura_con_studenti_da_lista.sh 2021-09-28 $( cut -d, -f1 profilo_esercizi_per_studente_submitted.csv )

# >>> trovi una sezione di TROUBLESHOOTING all'uso in calce al presente script <<<


DATA_ESAME=$1
shift
echo "Imposto condivisioni in SOLA LETTURA e tutte dentro il folder dell'appello ${DATA_ESAME}"

declare -A runtime
declare -a order;
start_time=`date +%s`
restart_time=$start_time

BOLD='\e[1m'
RED='\033[0;31m'
PURPLE='\033[0;35m'
LPURPLE='\033[1;51m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
#printf "I ${RED}love${NC} Stack Overflow\n"
#printf "I ${PURPLE}love${NC} Stack Overflow\n"
#printf "I ${LPURPLE}love${NC} Stack Overflow\n"

tipo_avanzamento="NEXT"
i=1;
PREV_EXE_VERSION=-1
for ID_student in "$@" 
do
    if [[ $tipo_avanzamento == "STOP" ]]; then
	echo -e "\nok, HAI DECISO DI INTERROMPERE A QUESTO PUNTO DELLA LISTA. Sia fatta la tua volontà.\n"
	break
    fi
    printf "\n${PURPLE}Creiamo condivisione con studente numero $i${NC}: ${BOLD}$ID_student${NC}\n"
    python onedrive-cli-api/share.py esamiRO/${DATA_ESAME}/${ID_student} ${ID_student}@studenti.univr.it r
    python onedrive-cli-api/share.py esamiRO/${DATA_ESAME}/quadro_voti/tabellone_punteggi_con_voti.pdf ${ID_student}@studenti.univr.it r
    if [[ $tipo_avanzamento != "ALL" ]]; then
	echo -e "\nOra valuta se sei soddisfatto di come ha funzionato per il primo studente nella lista (o fino a quì) e decidi come proseguire."
	read -p  "Proseguire con 1 prossimo studente (nN), con TUTTI gli studenti (aA) che seguono nella lista, oppure uscire (EXIT con ogni altro tasto)? " -n 1 -r
	case $(echo $REPLY | tr '[A-Z]' '[a-z]') in
            n) echo -e "\nok, proseguiamo di 1 sol passo\n" ;;
	    a) tipo_avanzamento="ALL" ;;
            *) tipo_avanzamento="STOP" ;;
        esac
    fi    
    current_time=`date +%s`
    runtime["studente_$(printf "%2d" $i)_$ID_student"]=$((current_time-restart_time))
    order+=( "studente_$(printf "%2d" $i)_$ID_student" )
    restart_time=$current_time
    i=$((i + 1))
done
echo
echo "Finito!"
echo
echo "Analizza la reportistica dei tempi impiegati:"
for i in "${order[@]}"
do
    echo "$i: ${runtime[$i]}"
done
current_time=`date +%s`
total_time=$((current_time-start_time))
echo 
echo "TEMPO TOTALE= $total_time"
exit 0

# TROUBLESHOOTING:
# possibili problemi:
# Problem 1:  quando lanci questo script da terminale ti copia nella clipboard il codice da immettere nel browser. Ma il browser può apparirti irresponsive e non sai come fare.
# Infatti sul terminale avrà scritto le seguenti due righe:
# > Expired token
# > The code CAQD3TVFK has been copied to your clipboard, and your web browser is opening https://microsoft.com/devicelogin. Paste the code to sign in.
# Non panicare per la riga con "Expired token", infatti scade dopo 3600 secondi e sei quì proprio per rinnovarlo, per questo te lo ha messo nella clip-board.
# Tuttavia se provi a pastarlo nel browser lui si blocca.
# Come uscirne:
#   1. pigia il pulsante "next" senza pasatre il token
#   2. a quel punto, quando lui si lamenta che il token è sbagliato, potrai ora inserire il token senza che il browser si impalli. (Il modo più semplice sarà con Ctrl-V dato che lo hai nella clipboard, ma puoi anche fare percorsi più lunghi, ora non si dovrebbe più impallare).
# Problem 2:  when on the terminal you get something like:
# > Getting id of tabellone_punteggi_con_voti.pdf...
# > Traceback (most recent call last):
# >   File "onedrive-cli-api/share.py", line 225, in <module>
# >     item_id = get_item_id(GRAPH_SESSION, item_path)['id'] # esempio: item_id='01GJ5S5QPJL4RWEX72O5A2VCU2GGMS6UVZ'
# > KeyError: 'id'
# significa che non trova il file in questione. Se ti sembra di trovare quel file in locale, la causa potrebbe allora essere che non hai sincronizzato OneDrive e quindi lui non trova il file cui ti riferisci.
#
# Problem 3:  when on the terminal you get something like:
# > Traceback (most recent call last):
# >  File "onedrive-cli-api/share.py", line 13, in <module>
# >    from adal import AuthenticationContext
#ModuleNotFoundError: No module named 'adal'
# significa che hai lanciato il comando da dentro un environment dove adal non c'è.
