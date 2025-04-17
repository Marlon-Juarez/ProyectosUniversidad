from red.generar_imagen import grafo
from PyQt5 import QtCore, QtWidgets  # <-- Añade QtWidgets aquí
from PyQt5.QtWidgets import QDialog, QMessageBox, QScrollArea, QVBoxLayout, QWidget, QSizePolicy
from interface.vnt_cadena import Ui_cadena
from PyQt5.QtGui import QPixmap, QWheelEvent
from PyQt5.QtCore import Qt, QSize
import os

class VentanaCadena(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_cadena()
        self.ui.setupUi(self)
        
        # Objeto grafo
        self.red = None
        
        # Configurar el área de scroll para la imagen
        self.scroll_area = QScrollArea(self.ui.frame)
        self.scroll_area.setGeometry(QtCore.QRect(390, 130, 351, 561))
        self.scroll_area.setStyleSheet("border: 2px solid black;")
        self.scroll_area.setWidgetResizable(False)
        
        # Widget contenedor para la imagen
        self.image_container = QWidget()
        self.image_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Configurar el QLabel para la imagen
        self.image_label = QtWidgets.QLabel(self.image_container)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_label.setScaledContents(False)
        
        # Configurar layout para centrar la imagen
        layout = QVBoxLayout(self.image_container)
        layout.addWidget(self.image_label, 0, Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Configurar el scroll area
        self.scroll_area.setWidget(self.image_container)
        
        # Inicializar el controlador de zoom
        self.zoom_controller = ZoomController(
            self.scroll_area,
            self.image_label,
            self.image_container
        )
        
        # Conectar botones
        self.ui.btnIniciar.clicked.connect(self.iniciar_cadena)
        self.ui.btnSiguiente.clicked.connect(self.siguiente_cadena)
        
        # Conectar el evento de rueda del ratón para el zoom
        self.scroll_area.wheelEvent = self.zoom_controller.wheelEvent
        
        # Asegurar scroll arriba al inicio
        self.scroll_area.verticalScrollBar().setValue(0)
        self.scroll_area.horizontalScrollBar().setValue(0)
        self.ui.textBrowser.verticalScrollBar().setValue(0)
    
    def cargar_imagen(self):
        ruta_imagen = "red/red_petri.png"
        if os.path.exists(ruta_imagen):
            pixmap = QPixmap(ruta_imagen)
            self.zoom_controller.set_pixmap(pixmap)
            self.ui.textBrowser.verticalScrollBar().setValue(0)
            return True
        return False

    def iniciar_cadena(self):
        texto = self.ui.txtcampo.toPlainText().strip()

        if texto:
            self.ui.textBrowser.setPlainText(f"Cadena ingresada: {texto}\nPresiona 'Siguiente' para avanzar paso a paso")
            
            # Crear e inicializar el grafo
            self.red = grafo(texto)
            self.red.generar("semaforo")
            
            # Cargar imagen inicial
            if not self.cargar_imagen():
                QMessageBox.warning(self, "Error", "No se pudo generar la imagen del grafo.")
        else:
            QMessageBox.warning(self, "Advertencia", "Por favor ingresa una cadena.")

    def siguiente_cadena(self):
        if not hasattr(self, 'red') or self.red is None:
            QMessageBox.warning(self, "Advertencia", "Primero debes iniciar una cadena")
            return
            
        # Avanzar al siguiente paso
        hay_mas_pasos = self.red.siguiente_paso()
        
        # Actualizar la imagen
        if self.cargar_imagen():
            # Actualizar descripción en textBrowser
            if self.red.estado_actual == 1:
                self.ui.textBrowser.append(f"\nProcesando letra: {self.red.letra_actual}")
            elif self.red.estado_actual > 1:
                self.ui.textBrowser.append(f"Paso {self.red.estado_actual} para letra {self.red.letra_actual}")
            
            if not hay_mas_pasos:
                self.ui.textBrowser.append("\n¡Proceso completado!")
                self.ui.btnSiguiente.setEnabled(False)
        else:
            QMessageBox.warning(self, "Error", "No se pudo actualizar la imagen del grafo.")


class ZoomController:
    def __init__(self, scroll_area, image_label, image_container):
        self.scroll_area = scroll_area
        self.image_label = image_label
        self.image_container = image_container
        self.zoom_factor = 1.0
        self.max_zoom = 3.0
        self.min_zoom = 0.5
        self.current_pixmap = None

    def wheelEvent(self, event: QWheelEvent):
        if event.modifiers() & Qt.ControlModifier:
            delta = event.angleDelta().y()
            if delta > 0:
                self.zoom_in()
            else:
                self.zoom_out()
            event.accept()
        else:
            QScrollArea.wheelEvent(self.scroll_area, event)

    def zoom_in(self):
        if self.zoom_factor < self.max_zoom:
            self.zoom_factor *= 1.1
            self.update_image_zoom()

    def zoom_out(self):
        if self.zoom_factor > self.min_zoom:
            self.zoom_factor /= 1.1
            self.update_image_zoom()

    def update_image_zoom(self):
        if self.current_pixmap:
            original_size = self.current_pixmap.size()
            scaled_size = QSize(
                int(original_size.width() * self.zoom_factor),
                int(original_size.height() * self.zoom_factor)
            )
            
            scaled_pixmap = self.current_pixmap.scaled(
                scaled_size, 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            
            self.image_label.setPixmap(scaled_pixmap)
            self.image_label.resize(scaled_pixmap.size())
            self.image_container.adjustSize()
            
            # Centrar la vista
            self.scroll_area.verticalScrollBar().setValue(0)
            self.scroll_area.horizontalScrollBar().setValue(0)

    def set_pixmap(self, pixmap):
        self.current_pixmap = pixmap
        self.update_image_zoom()