import sys
import subprocess
import os
import json
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

        pasta_base = os.path.expanduser("~")
        json_path = os.path.join(pasta_base, "Teste", "programas_selecionados.json")
        if not os.path.exists(json_path):
            QMessageBox.critical(self, "Erro", f"O arquivo {json_path} não foi encontrado.")
            return
        with open(json_path) as f:
            pacotes = json.load(f)

        #Chama o script bash que injeta os pacotes
        script_path = os.path.join(os.path.dirname(__file__), "scripts", "injetar_pacotes.sh")
        if not os.path.exists(script_path):
            QMessageBox.critical(self, "Erro", f"O script {script_path} não foi encontrado.")
            return
        comando = ["bash", script_path] + pacotes

        try:
            subprocess.run(comando, check=True)
            QMessageBox.information(self, "Sucesso", "Pacotes injetados com sucesso")
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Erro", f"Falha ao injetar pacotes: {e}")


    #Essa funcao vai abrir a lista de distros baseadas no arch (em andamento)
    def abrir_arch(self, event):
        QMessageBox.information(self, "Em desenvolvimento", "As distribuições baseadas no Arch Linux estarão disponíveis em breve")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = QuintaTelaPrincipal()
    janela.show()
    sys.exit(app.exec_())

