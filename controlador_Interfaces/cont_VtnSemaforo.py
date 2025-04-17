from red.generar_imagen import grafo
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QMessageBox, QScrollArea, QVBoxLayout, QWidget, QSizePolicy
from interface.vtn_semaforo import Ui_simulacion_semaforo
from PyQt5.QtGui import QPixmap, QWheelEvent
from PyQt5.QtCore import Qt, QSize
from PyQt5 import QtCore, QtGui, QtWidgets
import os
import sys


class ControladorSemaforo(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_simulacion_semaforo()
        self.ui.setupUi(self)
        self.primera_ejecucion = True


        
        # Lista de estados del semáforo con textos formateados con HTML para saltos de línea
        self.estados_semaforo = [
            {
                "principal": "Roja", 
                "secundario": "Verde", 
                "token": """<b>Estado 0:</b><br/>
                           - T amarilla1 -> roja1:<br/>
                           &nbsp;&nbsp;• Consume token de amarilla1<br/>
                           &nbsp;&nbsp;• Produce token para roja1<br/>
                           - T roja2 -> verde2:<br/>
                           &nbsp;&nbsp;• Consume tokens de luz roja2 y espera2<br/>
                           &nbsp;&nbsp;• Produce token para luz verde1<br/>
                           <br/>
                           <b>Tokens actuales:</b><br/>
                           - Semáforo principal: Rojo<br/>
                           - Semáforo secundario: Verde"""
            },
            {
                "principal": "Amarilla", 
                "secundario": "Roja", 
                "token": """<b>Estado 1:</b><br/>
                           - T verde2 -> amarilla2, espera1:<br/>
                           &nbsp;&nbsp;• Consume el token de luz verde2<br/>
                           &nbsp;&nbsp;• Produce un token para luz amarilla2 y espera1<br/>
                           - T roja1 -> verde1 no puede dispararse (necesita token de espera1)<br/>
                           <br/>
                           <b>Tokens actuales:</b><br/>
                           • Luz Amarilla2<br/>
                           • Luz Roja1<br/>
                           • Espera1"""
            },
            {
                "principal": "Verde", 
                "secundario": "Roja", 
                "token": """<b>Estado 2:</b><br/>
                           - T amarilla2 -> roja2:<br/>
                           &nbsp;&nbsp;• Consume token de amarilla2<br/>
                           &nbsp;&nbsp;• Produce token para roja2<br/>
                           - T roja1 -> verde1:<br/>
                           &nbsp;&nbsp;• Consume tokens de luz roja1 y espera1<br/>
                           &nbsp;&nbsp;• Produce token para luz verde1<br/>
                           <br/>
                           <b>Tokens actuales:</b><br/>
                           • Luz roja2<br/>
                           • Luz verde1"""
            },
            {
                "principal": "Roja", 
                "secundario": "Amarilla", 
                "token": """<b>Estado 3:</b><br/>
                           - T verde1 -> amarilla1, espera2:<br/>
                           &nbsp;&nbsp;• Consume token de luz verde1<br/>
                           &nbsp;&nbsp;• Produce tokens para luz amarilla1 y espera2<br/>
                           - T roja2 -> verde2 no puede dispararse (necesita token de espera2)<br/>
                           <br/>
                           <b>Tokens actuales:</b><br/>
                           • Luz Amarilla1<br/>
                           • Luz Roja2<br/>
                           • Espera2"""
            }
        ]
        

        # Bandera para controlar el estado de pausa
        self.pausado = False

        # Conectar el botón de pausa
        self.ui.btnPausa.clicked.connect(self.toggle_pausa)

        # Inicializar el índice con 1 para que comience en el estado 1
        self.index = 1  # Cambié el valor a 1 para iniciar desde el estado 1

        # Generar las imágenes iniciales
        self.generador_grafo = grafo()
        self.generar_imagenes_iniciales()

        # Configurar el timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.actualizar_elementos)
        self.timer.start(4000)  # 4 segundos

    def generar_imagenes_iniciales(self):
        """Genera todas las imágenes necesarias antes de iniciar el timer"""
        # Generar imágenes del grafo para cada estado
        self.imagenes_grafo = []

        for i in range(4):
            # Limpiar el grafo
            self.generador_grafo.dot.clear()

            # Lugares
            if i == 0: 
                # Configurar el grafo según el estado actual
                self.generador_grafo.generar_red_semaforo()
            else:
                # Configurar el grafo según el estado actual
                self.generador_grafo.generar_red_semaforo_animado(i)

            # Cargar la imagen generada
            self.generador_grafo._renderizar()
            img_path = os.path.join("red", "red_petri.png")
            self.imagenes_grafo.append(QtGui.QPixmap(img_path))
        
        # Imágenes de los semáforos (estas son estáticas)
        self.imagenes_principal = [
            QtGui.QPixmap("interface/img/luzRoja.png").transformed(QtGui.QTransform().rotate(270)),
            QtGui.QPixmap("interface/img/luzRoja.png").transformed(QtGui.QTransform().rotate(270)),
            QtGui.QPixmap("interface/img/luzVerde.png").transformed(QtGui.QTransform().rotate(270)),
            QtGui.QPixmap("interface/img/luzAmarilla.png").transformed(QtGui.QTransform().rotate(270))
        ]
        
        self.imagenes_secundario = [
            QtGui.QPixmap("interface/img/luzVerde.png"),
            QtGui.QPixmap("interface/img/luzAmarilla.png"),
            QtGui.QPixmap("interface/img/luzRoja.png"),
            QtGui.QPixmap("interface/img/luzRoja.png")
        ]

    def actualizar_elementos(self):
        if self.primera_ejecucion:
            self.primera_ejecucion = False
            print("Ejecutándose")
            return  # No hace nada la primera vez, luego de eso el ciclo continuará

        # El resto de la función sigue igual para actualizar los estados
        estado = self.estados_semaforo[self.index]
        self.ui.semaforo_principal.setPixmap(self.imagenes_principal[self.index])
        self.ui.semaforo_secundario.setPixmap(self.imagenes_secundario[self.index])

        # Actualizar el grafo y el texto
        if hasattr(self.ui, 'lblDiagrama'):
            self.ui.lblDiagrama.setPixmap(self.imagenes_grafo[self.index])
        
        self.ui.txtDescripcion.setHtml(f"""
            <div style='font-size: 16px; line-height: 1.5;'>
                {estado['token']}
            </div>
        """)

        # Actualizar índice para el próximo ciclo
        self.index = (self.index + 1) % len(self.estados_semaforo)

    
    def toggle_pausa(self):
        """Alterna entre pausado y reanudado"""
        self.pausado = not self.pausado
        
        if self.pausado:
            self.timer.stop()
            self.ui.btnPausa.setText("Reanudar")
        else:
            self.timer.start(4000)
            self.ui.btnPausa.setText("Pausar")