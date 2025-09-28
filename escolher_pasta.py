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



class EscolhaPasta(QWidget):
     def __init__(self):
          super().__init__()
          self.setWindowTitle("Escolha a pasta onde quer salvar os seus arquivos .deb")
          self.pasta = ""

     def abrir_dialog(self):
          self.pasta = QFileDialog.getExistingDirectory(
               self,
               "Escolha a pasta",
               os.path.expanduser("~"), #Codigo que comeca da pasta home do usuario
               QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
          )
          return self.pasta
     
def iniciar_tela():
    app = QApplication(sys.argv)
    tela = EscolhaPasta()
    pasta_escolhida = tela.abrir_dialog()

    if not pasta_escolhida:
        print("O usuário cancelou ou não escolheu a pasta", flush=True)
        sys.exit(1)

    print(pasta_escolhida, flush=True)
    sys.exit(0)

if __name__ == "__main__":
    iniciar_tela()