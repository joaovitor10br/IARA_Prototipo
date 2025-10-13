import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QRadioButton, QPushButton, QProgressBar, QMessageBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal

#Essa classe cria uma Thread para baixar o arquivo
class DownloadThread(QThread):
    progress = pyqtSignal(int) #Esse codigo ira criar a barra de progresso de donwload
    finished = pyqtSignal() #Esse codigo ira criar a barra de finalizado do download
    error = pyqtSignal(str) #Cria o codigo de erro


    def __init__(self, url, destino):
        super().__init__()
        self.url = url
        self.destino = destino

    def run(self):
        try:
            response = requests.get(self.url, stream=True, allow_redirects=True, timeout=30)
            response.raise_for_status()  # Lança erro se não for 200 OK

            total = response.headers.get('Content-Length')
            total = int(total) if total is not None else 0

            with open(self.destino, 'wb') as file:
                baixado = 0
                for data in response.iter_content(chunk_size=1024 * 64):
                    if not data:
                        continue
                    file.write(data)
                    baixado += len(data)
                    if total > 0:
                        progresso = int(baixado * 100 / total)
                        self.progress.emit(progresso)
                    else:
                        # Caso não saiba o tamanho total, mostra progresso simbólico
                        self.progress.emit((baixado // (1024 * 1024)) % 100)

            self.finished.emit()

        except Exception as e:
            self.error.emit(str(e))

class QuintaTela(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Escolha sua distribuição Ubuntu")
        self.setGeometry(400, 200, 400, 300)

        layout = QVBoxLayout()

        label = QLabel("Selecione uma distribuição baseada no Ubuntu: ")
        layout.addWidget(label, alignment=Qt.AlignCenter)

        self.opcao1 = QRadioButton("Ubuntu 24.04 LTS")
        self.opcao2 = QRadioButton("Ubuntu 22.04 LTS")
        self.opcao3 = QRadioButton("Linux Mint 22")
        self.opcao4 = QRadioButton("Zorin OS 17")

        layout.addWidget(self.opcao1)
        layout.addWidget(self.opcao2)
        layout.addWidget(self.opcao3)
        layout.addWidget(self.opcao4)

        self.barra = QProgressBar() #Esse codigo cria a barra de progresso
        self.barra.setValue(0)
        layout.addWidget(self.barra)

        self.botao_avancar = QPushButton("Avançar")
        self.botao_avancar.clicked.connect(self.baixar_iso)
        layout.addWidget(self.botao_avancar)

        self.setLayout(layout)

    def baixar_iso(self):
        if self.opcao1.isChecked():
            url = "https://ubuntu.c3sl.ufpr.br/releases/22.04/ubuntu-22.04.5-desktop-amd64.iso"
            nome = "ubuntu_24_04.iso"
        elif self.opcao2.isChecked():
            url = "https://releases.ubuntu.com/22.04/ubuntu-22.04.5-desktop-amd64.iso"
            nome = "ubuntu_22_04.iso"
        elif self.opcao3.isChecked():
            url = "https://mirror.csclub.uwaterloo.ca/linuxmint/stable/22/linuxmint-22-cinnamon-64bit.iso"
            nome = "linuxmint_22.iso"
        elif self.opcao4.isChecked():
            url = "https://mirror.umd.edu/zorin/17/Zorin-OS-17.3-Core-64-bit-r2.iso"
            nome = "zorin_17.iso"
        else:
            QMessageBox.warning(self, "Aviso", "Selecione uma distribuição antes de avançar.")
            return
        
        destino = f"/home/joao/Downloads/{nome}"

        self.botao_avancar.setEnabled(False)
        self.download_thread = DownloadThread(url, destino)
        self.download_thread.progress.connect(self.barra.setValue)
        self.download_thread.finished.connect(self.download_concluido)
        self.download_thread.error.connect(self.download_falhou)
        self.download_thread.start()

    def download_falhou(self, mensagem):
        QMessageBox.critical(self, "Erro no download", f"Ocorreu um erro: {mensagem}")
        self.botao_avancar.setEnabled(True)

    def download_concluido(self):
        QMessageBox.information(self, "Concluído", "Download finalizado com sucesso!")
        self.botao_avancar.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = QuintaTela()
    janela.show()
    sys.exit(app.exec_())
