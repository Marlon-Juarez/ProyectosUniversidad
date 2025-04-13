import sys
from red.generar_imagen import grafo
from PyQt5.QtWidgets import QApplication, QMainWindow
# Importa la clase Ui_cadena desde el archivo generado
from interface.ventana_main import Ui_ProyectoMC2
from controlador_Interfaces.cont_VtnCadena import VentanaCadena

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_ProyectoMC2()
        self.ui.setupUi(self)

        # Conectar botón a evento
        self.ui.Cadena.clicked.connect(self.on_button_click)

    def on_button_click(self):
        self.ventana_cadena = VentanaCadena()
        self.ventana_cadena.exec_()  # Usamos exec_() si es QDialog

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec_())