import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QHBoxLayout, QPushButton, QMessageBox
)
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtCore import Qt
from quinta_tela import QuintaTela #Esse codigo importa a quinta tela ja pronta

class QuintaTelaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Escolha a sua distribuição Linux")
        self.setGeometry(400, 200, 500, 350)

        layout = QVBoxLayout()
        label = QLabel("Qual distribuição Linux você usa?")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        #Cria o layout horizontal para os icones
        icones_layout = QHBoxLayout()

        #Essa parte cria o icone do Ubuntu
        self.ubuntu_btn = QLabel()
        ubuntu_pix = QPixmap("icons/ubuntu_logo.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.ubuntu_btn.setPixmap(ubuntu_pix)
        self.ubuntu_btn.setAlignment(Qt.AlignCenter)
        self.ubuntu_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.ubuntu_btn.mousePressEvent = self.abrir_ubuntu #Esse comando vai abrir a tela do ubuntu

        #Essa parte cria o icone do Arch Linux
        self.arch_btn = QLabel()
        arch_pix = QPixmap("icons/arch_linux_logo.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.arch_btn.setPixmap(arch_pix)
        self.arch_btn.setAlignment(Qt.AlignCenter)
        self.arch_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.arch_btn.mousePressEvent = self.abrir_arch #Esse comando vai abrir a tela do arch

        icones_layout.addWidget(self.ubuntu_btn)
        icones_layout.addWidget(self.arch_btn)

        layout.addLayout(icones_layout)
        self.setLayout(layout)

    #Essa funcao vai abrir a lista de distros baseadas no ubuntu
    def abrir_ubuntu(self, event):
        self.hide() #Esse comando esconde a tela principal
        self.ubuntu_window = QuintaTela()
        self.ubuntu_window.show()

    #Essa funcao vai abrir a lista de distros baseadas no arch (em andamento)
    def abrir_arch(self, event):
        QMessageBox.information(self, "Em desenvolvimento", "As distribuições baseadas no Arch Linux estarão disponíveis em breve")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = QuintaTelaPrincipal()
    janela.show()
    sys.exit(app.exec_())

