
#Projeto IARA (Protótipo) - Criador de ISOs personalizáveis

> ⚠️ **Atenção** este repositório abriga apenas a versão protótipa do projeto, feita em Python e PyQt5 para interface gráfica e Bash para lógica de programação e backend. Nessa versão protótipa o programa apenas baixa a imagem ISO dos repositórios oficiais das distribuições Linux, sem fazer qualquer alteração em seu conteúdo. Em breve estarei começando a desenvolver a versão "definitiva" do software, que será feita em Flutter para interface gráfica e Rust para lógica de programação e backend.

Esse projeto tem como objetivo desenvolver um software, onde o usuário poderá criar um arquivo ISO do seu próprio sistema, com todas ou quase todas as suas configurações dentro dele, como wallpaper, softwares, entre outros. Este programa foi feito para ser utilizado como uma forma de segurança, em que, caso acontença algum problema no computador do usuário, ele sempre terá uma cópia do mesmo ao seu lado, seja num pendrive, HD/SSD externo ou até mesmo na nuvem.


##Funcionalidades


-Escolher entre diferentes softwares de backup, como o Déjà Dup, Timeshift ou Rclone
-Selecionar em qual pasta deseja salvar a sua imagem ISO
-Interface gráfica minimalista, simples e intuitiva
-Compatível com distribuições Linux baseadas no Debian como o Ubuntu e Linux Mint, entre outras


##Instalação:

```bash
#Clone o repositório
git clone https://github.com/joaovitor10br/projeto-x.git

#Entre na pasta do projeto
cd projeto-x

#Crie e ative um ambiente virtual (opcional, mas recomendado)
python3 -m venv venv
source venv/bin/activate

#Instale as dependências
pip install -r requirements.txt
```

##Como usar:

1 - Abra o terminal do seu sistema, seja o VSCode ou o terminal padrão da sua distro e digite: 

```bash

./app.bash

```
2 - Siga os passos da interface: Escolha o método de backup, selecione a pasta de destino da ISO e confirme para gerar a ISO (Essa opção ainda não está disponível)

##Contribuição
As contribuições serão muito bem-vindas e de grande ajuda! Abra uma issue ou envie um pull request!


##Licença: MIT License


<<<<<<< HEAD
##Em desenvolvimento
