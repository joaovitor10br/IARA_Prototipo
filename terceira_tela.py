import sys
import os
os.environ["QT_QPA_PLATFORM"] = "xcb" #Esse codigo garante o uso do backend em X11
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QCheckBox, QPushButton, QSpacerItem, QSizePolicy, 
    QMessageBox, QDialog, QGridLayout, QFileDialog
)
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, QSize
from quarta_tela import iniciar_tela

class TerceiraTela(QDialog):

    def __init__(self):

        self.ret = 0
        self.pasta = None

        super().__init__()
        self.setWindowTitle("Projeto X - Escolha a sua pasta")
        self.setFixedSize(600, 400) #Defini o tamanho da tela de escolha de pasta
        self.setStyleSheet("background-color: black;")

        layout = QVBoxLayout()

        #Cria o titulo da tela
        titulo = QLabel("Escolha em qual pasta deseja salvar a sua ISO")
        titulo.setFont(QFont("Arial", 14))
        titulo.setStyleSheet("color: white;")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        #Este comando cria o botao da pasta
        btn_pasta = QPushButton()
        btn_pasta.setIcon(QIcon("/home/joao/TesteBASH/icons/pasta.png"))
        btn_pasta.setIconSize(QSize(128, 128))
        btn_pasta.setFixedSize(140, 140)
        btn_pasta.setStyleSheet("background-color: transparent; border: none;")
        btn_pasta.clicked.connect(self.abrir_explorador)
        layout.addWidget(btn_pasta, alignment=Qt.AlignCenter)

        #Cria um botão circular com uma seta no centro
        botao = QPushButton("→")
        botao.setFixedSize(70, 70)
        botao.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                border-radius: 35px;
                color: white;
                font-size: 28px;
                font-weight: bold;
            }
            QPushButton: hover {
                background-color: #2980b9;
            }
        """)
        botao.clicked.connect(self.accept)
        layout.addWidget(botao, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def abrir_explorador(self):
         dialog = QFileDialog(self, "Escolha a pasta", os.path.expanduser("~")) #Esse comando ira iniciar a pasta no diretorio home do usuario
         dialog.setOption(QFileDialog.ShowDirsOnly, True)
         dialog.setStyleSheet("") #Esse comando ira garantir que o explorador use o estilo padrao do sistema
         self.pasta = QFileDialog.getExistingDirectory()

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
    
class EscolhaPasta(QWidget):
     def __init__(self):
          super().__init__()
          self.setWindowTitle("Escolha a pasta onde quer salvar os seus arquivos .deb")
          self.pasta = ""

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
     
     app = QApplication([])
     tela = TerceiraTela()
     if tela.exec() == QDialog.Accepted:
          if tela.pasta:
               print("Pasta escolhida: ", tela.pasta)
               quarta = iniciar_tela(pasta_escolhida=tela.pasta) #Codigo que passa a pasta real para a quarta tela
     sys.exit(app.exec())
