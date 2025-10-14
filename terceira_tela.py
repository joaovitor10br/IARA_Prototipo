import sys
import os
os.environ["QT_QPA_PLATFORM"] = "xcb"
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QMessageBox, QDialog, QFileDialog
)
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor
from PyQt5.QtCore import Qt, QSize
from quarta_tela import iniciar_tela

class TerceiraTela(QDialog):
    def __init__(self):
        super().__init__()
        self.ret = 0
        self.pasta = None

        self.setWindowTitle("Projeto X - Escolha a sua pasta")
        self.setFixedSize(600, 400)
        self.setStyleSheet("background-color: black;")

        layout = QVBoxLayout()

        titulo = QLabel("Escolha em qual pasta deseja salvar a sua ISO")
        titulo.setFont(QFont("Arial", 14))
        titulo.setStyleSheet("color: white;")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        # botão da pasta
        btn_pasta = QPushButton()
        btn_pasta.setIcon(QIcon("/home/joao/TesteBASH/icons/pasta.png"))
        btn_pasta.setIconSize(QSize(128, 128))
        btn_pasta.setFixedSize(140, 140)
        btn_pasta.setStyleSheet("background-color: transparent; border: none;")
        btn_pasta.clicked.connect(self.abrir_explorador)
        layout.addWidget(btn_pasta, alignment=Qt.AlignCenter)

        # botão próximo
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
            QPushButton:hover { background-color: #2980b9; }
        """)
        botao.clicked.connect(self.confirmar)
        layout.addWidget(botao, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def abrir_explorador(self):
        # Remove temporariamente o estilo escuro pra não afetar o explorador
        estilo_antigo = self.styleSheet()
        self.setStyleSheet("")

        # Abre o explorador de arquivos nativo
        caminho = QFileDialog.getExistingDirectory(
            self,
            "Escolha a pasta onde deseja salvar",
            os.path.expanduser("~"),
            QFileDialog.ShowDirsOnly
        )

        # Restaura o estilo original da janela principal
        self.setStyleSheet(estilo_antigo)

        if caminho:
            os.makedirs(caminho, exist_ok=True)
            self.pasta = caminho

            # Cria manualmente o QMessageBox com estilo 100% visível
            msg = QMessageBox(self)
            msg.setWindowTitle("Pasta selecionada")
            msg.setText(f"Pasta escolhida:\n{caminho}")
            msg.setIcon(QMessageBox.Information)
            msg.setStandardButtons(QMessageBox.Ok)

            # Aplica estilo explícito — fundo claro, texto preto, botão azul
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: white;
                    color: black;
                    font-size: 13px;
                    font-family: Arial;
                }
                QLabel {
                    color: white;
                }
                QPushButton {
                    background-color: white;
                    color: black;
                    padding: 6px 14px;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #005fa3;
                }
            """)
            msg.exec_()


    def confirmar(self):
        if not self.pasta:
            QMessageBox.warning(self, "Atenção", "Por favor, escolha uma pasta antes de continuar.")
            return
        self.ret = 1
        self.accept()  # Fecha a tela e marca como aceita

    def closeEvent(self, event):
        if self.ret == 0:
            tela = FecharTela()
            resposta = tela.exec()
            if resposta == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

class FecharTela(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fechar o programa")
        self.setFixedSize(300, 150)
        self.setStyleSheet("background-color: black; color: white;")

        layout = QVBoxLayout()

        mensagem = QLabel("Você quer mesmo fechar o programa?")
        mensagem.setFont(QFont("Arial", 12))
        mensagem.setAlignment(Qt.AlignCenter)
        layout.addWidget(mensagem)

        botoes_layout = QHBoxLayout()
        botao_sim = QPushButton("Sim")
        botao_nao = QPushButton("Não")

        botao_sim.setStyleSheet("""
            QPushButton { background-color: #3498db; color: white; padding: 6px 12px; border-radius: 6px; }
            QPushButton:hover { background-color: #2980b9; }
        """)
        botao_nao.setStyleSheet("""
            QPushButton { background-color: #aaa; color: black; padding: 6px 12px; border-radius: 6px; }
            QPushButton:hover { background-color: #888; }
        """)
        botao_sim.clicked.connect(lambda: self.done(QMessageBox.Yes))
        botao_nao.clicked.connect(lambda: self.done(QMessageBox.No))

        botoes_layout.addWidget(botao_sim)
        botoes_layout.addWidget(botao_nao)
        layout.addLayout(botoes_layout)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    tela = TerceiraTela()
    if tela.exec() == QDialog.Accepted and tela.pasta:
        print("Pasta escolhida:", tela.pasta)
        iniciar_tela(pasta_escolhida=tela.pasta)
    sys.exit(app.exec())
