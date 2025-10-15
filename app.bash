#!/bin/bash

#Código que chama a tela de boas vindas, criada em Python, para o arquivo bash
RET=$(python3 /home/joao/IARA/boasvindas.py)

if [ "$RET" -ne 1 ]; then
    echo "Usuario cancelou"
    exit
fi

#Este codigo chama a segunda tela e retorna o valor para o bash via stdout
SELECAO=$(python3 /home/joao/IARA/segunda_tela.py)
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
    #dialog --infobox "Instalando $SOFTWARE..." 5 50
    sudo apt update -y
    sudo apt install $SOFTWARE -y
fi

#Essa parte irá abrir o software após ele ter sido instalado
#dialog --infobox "Abrindo $SOFTWARE..." 5 50
#$SOFTWARE


#Essa função cria uma terceira tela, onde nela o usuário poderá escolher quais softwares deseja manter na ISO
TERCEIRA=$(python3 /home/joao/IARA/terceira_tela.py)
RET=$?

if [ "$RET" -ne 0 ]; then
    echo "Usuario cancelou a terceira tela"
    exit
fi

#O codigo TERCEIRA agora tera o caminho escolhido pelo usuario
echo "O usuario escolheu a pasta: $TERCEIRA"


#Codigo que executa a quarta tela, onde o usuario pode escolher os softwares para deixar pre instalado e pega os pacotes selecionados
SELECIONADOS=$(python3 /home/joao/IARA/quarta_tela.py)

if [ -z "$SELECIONADOS" ]; then
    echo "Usuário não selecionou nada ou cancelou a ação"
    exit
fi

echo "Usuário escolheu: $SELECIONADOS"

#Esse codigo cria a pasta de destino, caso nao exista
mkdir -p /home/joao/iso_build/custom/packages/

#Esse codigo copia os arquivos .deb para a pasta da ISO
for prog in $SELECIONADOS; do
    cp "$prog" /home/joao/iso_build/custom/packages/
done

#Esse codigo permite que o usuario escolha onde quer salvar seus arquivos .deb
DESTINO=$(python3 /home/joao/IARA/escolher_pasta.py)

if [ -z "$DESTINO" ]; then
    echo "Usuário cancelou ou não escolheu a pasta"
    exit
fi

#Esse comando ira copiar os pacotes selecionados
for prog in $SELECIONADOS; do
    cp "$prog" "$DESTINO"
done

#Esse codigo chama a quinta_tela_principal.py
python3 /home/joao/IARA/quinta_tela_principal.py
RET=$?

if [ "$RET" -ne 0 ]; then
    echo "Usuário cancelou a escolha da distribuição"
    exit
fi
