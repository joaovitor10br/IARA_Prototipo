#!/bin/bash

#Código que chama a tela de boas vindas, criada em Python, para o arquivo bash
RET=$(python3 /home/joao/TesteBASH/boasvindas.py)

if [ "$RET" -ne 1 ]; then
    echo "Usuario cancelou"
    exit
fi

#Este codigo chama a segunda tela e retorna o valor para o bash via stdout
SELECAO=$(python3 /home/joao/TesteBASH/segunda_tela.py)
if [ "$SELECAO" -eq 10 ]; then
    SOFTWARE="deja-dup"
elif [ "$SELECAO" -eq 20 ]; then
    SOFTWARE="timeshift"
elif [ "$SELECAO" -eq 30 ]; then
    SOFTWARE="rclone"
else
    echo "Usuario cancelou"
    exit
fi

#Essa parte verifica se o programa está instalado
if ! command -v $SOFTWARE &>/dev/null; then
    dialog --infobox "Instalando $SOFTWARE..." 5 50
    sudo apt update
    sudo apt install $SOFTWARE -y
fi

#Essa parte irá abrir o software após ele ter sido instalado
dialog --infobox "Abrindo $SOFTWARE..." 5 50
$SOFTWARE


#Essa função cria uma terceira tela, onde nela o usuário poderá escolher quais softwares deseja manter na ISO
TERCEIRA=$(python3 /home/joao/TesteBASH/terceira_tela.py)
RET=$?

if [ "$RET" -ne 0 ]; then
    echo "Usuario cancelou a terceira tela"
    exit
fi

#O codigo TERCEIRA agora tera o caminho escolhido pelo usuario
echo "O usuario escolheu a pasta: $TERCEIRA"


#Codigo que chama a tela de escolha de softwares antes do usuario criar a ISO
python3 /home/joao/TesteBASH/quarta_tela.py

RET=$?
if [ "$RET" -ne 0 ]; then
    echo "Usuario cancelou a quarta tela"
    exit
fi
