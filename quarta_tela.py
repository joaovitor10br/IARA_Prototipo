import sys
import os
os.environ["QT_QPA_PLATFORM"] = "xcb" #Esse codigo garante o uso do backend em X11
import shutil
import webbrowser
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QCheckBox, QPushButton, QSpacerItem, QSizePolicy, 
    QMessageBox, QDialog, QGridLayout, QFileDialog
)
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, QSize

class QuartaTela(QWidget):

    def __init__(self, pasta_escolhida):
        super().__init__()

        if not pasta_escolhida:
             raise ValueError("A pasta escolhida precisa ser passada pela terceira tela")
        self.pasta_terceira = pasta_escolhida
        self.ret = 0

        self.setWindowTitle("Escolha de programas")
        self.setStyleSheet("background-color: black; color: white;")
        self.resize(400, 300)

        layout_principal = QVBoxLayout()
        layout_principal.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        #Esse codigo cria o titulo da tela
        titulo = QLabel("Escolha quais programas você gostaria de deixar pré-instalado")
        titulo.setFont(QFont("Arial", 12))
        titulo.setStyleSheet("color: white;")
        titulo.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(titulo)
        layout_principal.addSpacing(20)

        #Esse codigo ira criar uma lista de programas junto com seus respectivos icones
        self.lista_programas = [
            ("Firefox", "/home/joao/TesteBASH/icons/firefox_icon.png", "instaladores/firefox"),
            ("Steam", "/home/joao/TesteBASH/icons/steam_icon.png", "instaladores/steam_latest.deb"),
            ("Spotify", "/home/joao/TesteBASH/icons/spotify_icon.png", None),
            ("Discord", "/home/joao/TesteBASH/icons/discord_icon.png", "instaladores/discord-0.0.111.deb"),
        ]


        self.checks = [] #Essa parte do codigo ira criar as checkbox
        layout_programas = QGridLayout()
        layout_programas.setAlignment(Qt.AlignHCenter)

        for i, (nome, icone, deb) in enumerate(self.lista_programas):
            
            checkbox = QCheckBox()
            self.checks.append(checkbox)
            checkbox.setStyleSheet(
            """
            QCheckBox {
                color: white;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid white;
                border-radius: 3px;
                background-color: black;
            }
            QCheckBox::indicator:checked {
                background-color: #3498db;
            }
            """
            )

            label_icon = QLabel()
            pixmap = QPixmap(icone).scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            label_icon.setPixmap(pixmap)

            label_text = QLabel(nome)
            label_text.setFont(QFont("Arial", 11))
            label_text.setStyleSheet("color: white;")

            layout_programas.addWidget(checkbox, i, 0, alignment=Qt.AlignCenter)
            layout_programas.addWidget(label_icon, i, 1, alignment=Qt.AlignCenter)
            layout_programas.addWidget(label_text, i, 2, alignment=Qt.AlignCenter)

        layout_principal.addLayout(layout_programas)
        layout_principal.addSpacing(30)

        #Esse codigo coloca o botao azul centralizado
        
        botao_proximo = QPushButton("→")
        botao_proximo.setStyleSheet(
            """
            QPushButton {
                background-color: #0078D7;
                border-radius: 8px;
                color: white;
                font-size: 28px;
                font-weight: bold;
                padding: 8 16px;
            }
            QPushButton: hover {
                background-color: #005A9E;
            }
        """)

        botao_proximo.clicked.connect(lambda: self.enviar_selecao())

        layout_botao = QHBoxLayout()
        layout_botao.addStretch()
        layout_botao.addWidget(botao_proximo)
        layout_botao.addStretch()
        layout_principal.addLayout(layout_botao)

        layout_principal.addStretch()
        self.setLayout(layout_principal)

    def close_with_value(self, value):
        self.ret = value
        self.close() #Esse codigo vai fechar a janela normalmente

    def enviar_selecao(self):
            selecionados = []
            for checkbox, (nome, __, deb) in zip(self.checks, self.lista_programas):
                 if checkbox.isChecked() and deb is not None:
                      selecionados.append(deb)
                 elif nome == "Spotify":
                      webbrowser.open("https://www.spotify.com/br-pt/download/linux/")
            
            if not selecionados:
                 QMessageBox.warning(self, "Atenção!", "Selecione pelo menos um programa!")
                 return
            
            #Esse codigo copia arquivos para a pasta escolhida pelo usuario
            copiados = []
            for arquivo in selecionados:
                 arquivos_abs = os.path.join(os.path.dirname(__file__), arquivo)
                 destino = os.path.join(self.pasta_terceira, os.path.basename(arquivos_abs))
                 os.makedirs(os.path.dirname(destino), exist_ok=True)
                 shutil.copy2(arquivos_abs, destino)
                 copiados.append(destino)

            print("Arquivos copiados: ", copiados)
            #Esse comando ira imprimir os pacotes selecionados para o bash
            self.ret = 1
            self.close()

    def closeEvent(self, event):
        #Cria a tela de mensagem perguntando se o usuario quer realmente fechar o programa
            if self.ret == 0:
                tela = FecharTela()
                resposta = tela.exec()

                if resposta == QMessageBox.Yes:
                    event.accept()
                else:
                    event.ignore()
            else:
                event.accept()

def iniciar_tela(parent = None, pasta_escolhida=None):
    janela = QuartaTela(pasta_escolhida)
    if parent:
         janela.setParent(parent)
    janela.show()
    return janela

#Essa classe ira fechar a tela
class FecharTela(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fechar o programa")
        self.setFixedSize(300, 150)
        self.setStyleSheet("background-color: black; color: white;")
        
        layout = QVBoxLayout()

        #Cria o texto de confirmacao
        mensagem = QLabel("Você quer mesmo fechar o programa?")
        mensagem.setFont(QFont("Arial", 12))
        mensagem.setAlignment(Qt.AlignCenter)
        layout.addWidget(mensagem) #Essa parte do código adiciona a mensagem

        #Cria os botoes
        botoes_layout = QHBoxLayout()
        botao_sim = QPushButton("Sim")
        botao_nao = QPushButton("Não")

        botao_sim.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 6px 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        botao_nao.setStyleSheet("""
            QPushButton {
                background-color: #aaa;
                color: black;
                padding: 6px 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #888;
            }
        """)
        botao_sim.clicked.connect(lambda: self.done(QMessageBox.Yes))
        botao_nao.clicked.connect(lambda: self.done(QMessageBox.No))

        botoes_layout.addWidget(botao_sim)
        botoes_layout.addWidget(botao_nao)
        layout.addLayout(botoes_layout)

        self.setLayout(layout)

if __name__ == "__main__":
     iniciar_tela()
