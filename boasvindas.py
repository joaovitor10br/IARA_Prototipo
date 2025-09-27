import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox, QDialog, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from segunda_tela import SegundaTela

class BoasVindas(QWidget):
    def __init__(self):
        super().__init__()

        self.ret = 0 #0 indica que cancelou, 1 indica que avancou

        self.setWindowTitle("Projeto X") #Titulo do programa
        self.setFixedSize(500, 300) #Defini o tamanho da tela inicial
        self.setStyleSheet("background-color: black") #Defini a cor de fundo para cinza claro

        #Cria o texto de boas vindas
        label = QLabel("Olá, seja bem-vindo ao Projeto X!\n\nAntes de começar a criar a sua ISO, \nprecisamos fazer algumas alterações.")
        label.setStyleSheet("color: white;")
        label.setFont(QFont("Arial", 14, QFont.Bold))
        label.setAlignment(Qt.AlignCenter)

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
        botao.clicked.connect(self.avancar)

        #Cria o layout da tela de boas vindas
        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(label, alignment=Qt.AlignCenter)
        layout.addStretch()
        layout.addWidget(botao, alignment=Qt.AlignCenter)
        layout.addStretch()
        self.setLayout(layout)

    def avancar(self):
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

def iniciar_tela():
    app = QApplication(sys.argv)
    janela = BoasVindas()
    janela.show()
    app.exec()
    return janela.ret #Retorna os valores 0 ou 1 para o app.bash

if __name__ == "__main__":
    resultado = iniciar_tela()
    print(resultado)
