#!/bin/bash

# adres bot API tg
tgURL=''
# adres pliku logu serwera
mclog='/home/mcserver/spigot/logs/latest.log'   # adres pliku logu serwera

cd /home/mcserver/tg



while true
do




#
# przesylanie z serwera na telegram
#


# kopiujemy obecny log serwera
cp $mclog current.log
# wybieramy z niego wszystkie linie ktorych wczesniej nie bylo i usuwamy kolory
awk 'NR==FNR{a[$0]=1;next}!a[$0]' last.log current.log | sed 's/[\x1B][^m]*m//g' > temp.log

# dopoki tymczasowy plik logu nie jest pusty
while [[ -s temp.log ]]
do
  # wycinamy z niego do 30 linii
  line=$(head -n 30 temp.log)
  echo -n "$(tail -n +31 temp.log)" > temp.log
  # escape'ujemy rozne znaki
  line=${line//\\/\\\\}
  line=${line//\'/\\\'}
  line=${line//\"/\\\"}

  # przesylamy zawartosc na czat ze mna
  result=$(curl -H "Content-Type: application/json" -d '{"chat_id":138268771,"text":"'"$line"'"}' $tgURL"sendMessage")
  # i logujemy odpowiedz serwera tg
  echo $result | jq . >> tg.log


  # przesylamy wiadomosci graczy na czat Wieliczka
  line=$(echo "$line" | grep "Chat Thread")
  if [ -n "$line" ]
  then
    # usuwamy niepotrzebne elementy wiadomosci
    line=$(echo "$line" | sed 's/^\(\[..:..:..\] \)[^<]*</\1</g')
    # wysylamy do api
    result=$(curl -H "Content-Type: application/json" -d '{"chat_id":-244449217,"text":"'"$line"'"}' $tgURL"sendMessage")
    # logujemy odpowiedz serwera
    echo $result | jq . >> tg.log
  fi

done

# zastepujemy poprzedni log obecnym
cp current.log last.log





#
# przesylanie z telegramu na serwer
#


# pobieramy pierwsza wiadomosc z tg
json=$(curl $tgURL"getUpdates?limit=1")

# przekazujemy serwerowi wiadomosc i pobieramy nastepne dopoki sie nie skoncza
while (( $(echo $json | jq '.result | length') == 1 ))
do

  # logujemy pobrany JSON
  echo $json | jq . >> tg.log
  # wyciagamy ID wiadomosci
  id=$(echo $json | jq -r '.result[].update_id')
  # wyciagamy tresc
  message=$(echo $json | jq -r '.result[].message.text')

  # jezeli wiadomosc posiada tresc
  if [ "$message" != "null" ]
  then
    # wyciagniecie nicku
    username=$(echo $json | jq -r '.result[].message.from.username')
    # dodanie say i nicku do wiadomosci
    messageToSend="say <<"$username">> "$message

    # jesli to ja, to sprawdzamy czy wiadomosc jest komenda i odpowiednio zmieniamy ja jesli tak
    if [ "$username" = "wanours" ]
    then
      messageToSend=$(echo $messageToSend | sed 's/^say <<wanours>> \///g')
    fi

    # przekazanie wiadomosci serwerowi
    /home/mcserver/various/spigcom.sh $messageToSend
  fi

  # kolejne pobranie wiadomosci z tg
  json=$(curl $tgURL"getUpdates?limit=1&offset="$((id + 1)) )

done



# czekamy sekunde przed nastepnymi zapytaniami do tg
sleep 1
done
