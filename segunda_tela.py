import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QDialog
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor
from PyQt5.QtCore import QSize, Qt

class SegundaTela(QDialog):

    def __init__(self):
        super().__init__()

        self.selecionado = 0
        self.ret = 0 #0 indica que cancelou, 1 indica que avancou
        

        self.setWindowTitle("Projeto X - Backup") #Titulo da segunda tela
        self.setFixedSize(600, 400) #Tamanho da segunda tela
        self.setStyleSheet("background-color: black;")

        layout = QVBoxLayout()

        #Este código cria o título, a mensagem referente ao backup
        titulo = QLabel("Escolha a sua opção de backup")
        titulo.setFont(QFont("Arial", 14))
        titulo.setStyleSheet("color: white;")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

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



        #Este comando cria os botões
        btn_deja = QPushButton()
        btn_deja.setIcon(QIcon("/home/joao/TesteBASH/icons/deja_dup.png"))
        btn_deja.setIconSize(QSize(64, 64))
        btn_deja.clicked.connect(lambda: self.selecionar(10)) #Código de saída 10
        btn_time = QPushButton()
        btn_time.setIcon(QIcon("/home/joao/TesteBASH/icons/timeshift.png"))
        btn_time.setIconSize(QSize(64, 64))
        btn_time.clicked.connect(lambda: self.selecionar(20)) #Código de saída 20
        btn_rclone = QPushButton()
        btn_rclone.setIcon(QIcon("/home/joao/TesteBASH/icons/rclone.png"))
        btn_rclone.setIconSize(QSize(64, 64))
        btn_rclone.clicked.connect(lambda: self.selecionar(30)) #Código de saída 30

        #Este comando cria o layout horizontal dos botões
        hbox = QHBoxLayout()
        hbox.addStretch() #Adiciona um espaço antes
        hbox.addWidget(btn_deja)
        hbox.addWidget(btn_time)
        hbox.addWidget(btn_rclone)
        hbox.addStretch() #Adiciona um espaço depois

        hbox.setSpacing(30)

        #Este comando cria o layout vertical dos botões
        vbox = QVBoxLayout()
        vbox.addStretch() #Adiciona um espaço em cima
        vbox.addWidget(titulo) #Adiciona o titulo centralizado
        vbox.addLayout(hbox) #Adiciona os botões centralizados
        vbox.addStretch() #Adiciona um espaço embaixo
        vbox.addWidget(botao, alignment=Qt.AlignCenter) #Adiciona o botão azul na segunda tela
        vbox.addStretch() #Adiciona um espaço final
        

        self.setLayout(vbox) #Seta o layout vertical
        vbox.setSpacing(30)

    def selecionar(self, codigo):
        # Essa linha evita reabrir o programa caso o usuario ja tenha clicado uma vez
        if self.selecionado == codigo:
            return
        
        self.selecionado = codigo

        #Cria um dicionario com os comandos de cada opcao
        comandos = {
            10: ["deja-dup"],
            20: ["timeshift"],
            30: ["rclone"]
        }

        if codigo in comandos:
            try:
                subprocess.Popen(comandos[codigo]) #Esta linha abre o programa sem encerrar a GUI
            except FileNotFoundError:
                aviso = TelaAviso(f"O programa selecionado não está instalado no sistema.")
                aviso.exec()
            except Exception as e:
                aviso = TelaAviso(f"Erro ao abrir o programa {e}")
                aviso.exec()

    def avancar(self):
            if self.selecionado == 0:
                aviso = TelaAviso("Selecione um dos três programas para avançar para a próxima tela.")
                aviso.exec()
                return
            self.ret = 1
            self.accept()

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

class TelaAviso(QDialog):


     #Esta classe ira criar a mensagem de erro caso o usuario tente ir para a terceira tela sem escolher um dos tres backups
    def __init__(self, mensagem):
        super().__init__()
        self.setWindowTitle("Atenção")
        self.setFixedSize(450, 200)
        self.setStyleSheet("background-color: black;")

        layout = QVBoxLayout()

        label = QLabel(mensagem)
        label.setFont(QFont("Arial", 12))
        label.setStyleSheet("color: white;")
        label.setAlignment(Qt.AlignCenter)
        label.setWordWrap(True) #Esse codigo quebra linha automaticamente
        layout.addWidget(label)

        BOTAO_STYLE = """
            QPushButton {
                background-color: #3498db;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1c5d99;
            }
        """
        def criar_botao(texto):
            btn = QPushButton(texto)
            btn.setStyleSheet(BOTAO_STYLE)
            return btn


        #Este codigo ira criar o botao de ok
        btn_ok = criar_botao("OK")
        btn_ok.setStyleSheet(BOTAO_STYLE)

        #Este codigo forca a cor do texto usando o QPalette
        cor = btn_ok.palette()
        cor.setColor(QPalette.ButtonText, QColor("white"))
        btn_ok.setPalette(cor)
        btn_ok.setAutoFillBackground(False)

        btn_ok.clicked.connect(self.accept)

        layout.addWidget(btn_ok, alignment=Qt.AlignCenter)
        self.setLayout(layout)

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
    janela = SegundaTela()
    janela.exec()
    print(janela.selecionado)


if __name__ == "__main__":
    iniciar_tela()
