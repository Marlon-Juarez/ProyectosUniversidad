import sys
from red.generar_imagen import grafo
from PyQt5.QtWidgets import QApplication, QMainWindow
# Importa la clase Ui_cadena desde el archivo generado
from interface.vtn_principal import Ui_ProyectoMC2
from controlador_Interfaces.cont_VtnCadena import VentanaCadena
from controlador_Interfaces.cont_VtnSemaforo import ControladorSemaforo

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_ProyectoMC2()
        self.ui.setupUi(self)

        # Conectar botón a evento
        self.ui.btn_Semaforo.clicked.connect(self.abrir_simulacion_semaforo)
        self.ui.btn_cadena.clicked.connect(self.abrir_cadena)

    def abrir_simulacion_semaforo(self):
        self.ventana_cadena = ControladorSemaforo()
        self.ventana_cadena.exec_() 

    def abrir_cadena(self):
        self.ventana_cadena = VentanaCadena()
        self.ventana_cadena.exec_() 



if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec_())