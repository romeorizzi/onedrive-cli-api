#!/bin/bash
# primo argomento: la data della sessione di esame (esempio: 2021-06-18)
# argomenti sucessivi: la sequenza di ID_students ai quali vuoi dare accesso in SOLA LETTURA alla cartella col loro tema + tua correzzione.

# POSSIBILI MODI DI CHIAMARE QUESTO SCRIPT (dopo esserti ricopiato in locale un .csv quale ad esempio  profilo_esercizi_per_studente_submitted.csv):
# ./condividi_in_lettura_con_studenti_da_lista.sh $( cut -d, -f1 profilo_esercizi_per_studente_submitted.csv )

DATA_ESAME=$1

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
    python onedrive-cli-api/share.py esamiRO/2021-06-18/${ID_student} ${ID_student}@studenti.univr.it r
    if [[ $tipo_avanzamento != "ALL" ]]; then
	echo -e "\nOra valuta se sei soddisfatto di come ha funzionato per il primo studente nella lista (o fino a quì) e decidi come proseguire."
	read -p  "Proseguire con 1 prossimo studente (nN), con TUTTI gli studenti (aA) che seguono nella lista, oppure uscire (EXIT con ogni altro tasto)? " -n 1 -r
	case $(echo $REPLY | tr '[A-Z]' '[a-z]') in
            n) echo -e "\nok, proseguiamo di 1 sol passo\n" ;;
	    a) tipo_avanzamento="ALL"
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

