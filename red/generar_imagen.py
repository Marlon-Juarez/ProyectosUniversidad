from graphviz import Digraph
import os

class grafo:

    def __init__(self, cadena=""):
        self.dot = Digraph(format='png')
        self.nombre_archivo = "red_petri"
        self.cadena = cadena
        self.paso_actual = 0
        self.lista_chars = list(cadena) if cadena else []
        self.letra_actual = None
        self.estado_actual = 0

    def generar(self, tipo):
        # Reiniciar estados
        self.paso_actual = 0
        self.estado_actual = 0
        self.lista_chars = list(self.cadena) if self.cadena else []
        
        # Generar el grafo completo inicial
        
        if(tipo == "cadena"):
            self.generar_red_cadena()  
        elif(tipo == "semaforo"):
            self.generar_red_semaforo()

        self._renderizar()

    def siguiente_paso(self):
        if not self.lista_chars:
            return False  # No hay más pasos
            
        if self.estado_actual == 0:
            # Primer paso: tomar la primera letra
            self.letra_actual = self.lista_chars.pop(0)
            self.estado_actual = 1
        else:
            # Avanzar al siguiente estado
            self.estado_actual += 1
            
        # Generar el grafo con el estado actual
        self.red_animada_cadena()
        self._renderizar()
        
        # Si hemos completado todos los estados para esta letra
        if self.estado_actual >= 20:  # Ajusta según tus estados necesarios
            self.estado_actual = 0
            if not self.lista_chars:
                return False  # No hay más letras
                
        return True  # Hay más pasos

    def generar_red_semaforo(self):
        # Limpiar el grafo
        self.dot.clear()
        
        # Lugares
        self.dot.node('P1', shape='circle', label='luz_Verde1')
        self.dot.node('P2', shape='circle', label='luz_Amarilla1')
        self.dot.node('P3', shape='circle', label='<<font point-size="20">luz_Roja1<br/>●</font>>', style='filled', fillcolor='red')
        self.dot.node('P4', shape='circle', label='espera1')

        self.dot.node('P5', shape='circle', label='<<font point-size="20">luz_Verde2<br/>●</font>>', style='filled', fillcolor='green')
        self.dot.node('P6', shape='circle', label='luz_Amarilla2')
        self.dot.node('P7', shape='circle', label='luz_Roja2')
        self.dot.node('P8', shape='circle', label='espera2')
        
  

        # Transiciones
        self.dot.node('T1', shape='box', label='T verde1 -> amarilla1, espera2')
        self.dot.node('T2', shape='box', label='T amarilla1 -> roja1')
        self.dot.node('T3', shape='box', label='T roja1 -> verde1')

        self.dot.node('T4', shape='box', label='T verde2 -> amarilla2, espera1')
        self.dot.node('T5', shape='box', label='T amarilla2 -> roja2')
        self.dot.node('T6', shape='box', label='T roja2 -> verde2')


        # Arcos
        self.dot.edge('P1', 'T1')
        self.dot.edge('T1', 'P2')
        self.dot.edge('T1', 'P8')

        self.dot.edge('P2', 'T2')
        self.dot.edge('T2', 'P3')
        self.dot.edge('P3', 'T3')
        self.dot.edge('P4', 'T3')
        self.dot.edge('T3', 'P1')

        self.dot.edge('P5', 'T4')
        self.dot.edge('T4', 'P6')
        self.dot.edge('T4', 'P4')

        self.dot.edge('P6', 'T5')
        self.dot.edge('T5', 'P7')
        self.dot.edge('P7', 'T6')
        self.dot.edge('P8', 'T6')
        self.dot.edge('T6', 'P5')

    def generar_red_semaforo_animado(self, i):
        # Limpiar el grafo
        self.dot.clear()

        # -------- Lugares --------

        # luz_Verde1 (P1)
        color = "green" if i == 2 else "white"
        etiqueta = "<br/>●" if i == 2 else " "
        self.dot.node('P1', shape='circle', label=f'<<font point-size="20">luz_Verde1{etiqueta}</font>>', style='filled', fillcolor=color)

        # luz_Amarilla1 (P2)
        color = "yellow" if i == 3 else "white"
        etiqueta = "<br/>●" if i == 3 else " "
        self.dot.node('P2', shape='circle', label=f'<<font point-size="20">luz_Amarilla1{etiqueta}</font>>', style='filled', fillcolor=color)

        # luz_Roja1 (P3)
        color = "red" if i == 1 else "white"
        etiqueta = "<br/>●" if i == 1 else " "
        self.dot.node('P3', shape='circle', label=f'<<font point-size="20">luz_Roja1{etiqueta}</font>>', style='filled', fillcolor=color)

        # espera1 (P4)
        color = "blue" if i == 1 else "white"
        etiqueta = "<br/>●" if i == 1 else " "
        self.dot.node('P4', shape='circle', label=f'<<font point-size="20">espera1{etiqueta}</font>>', style='filled', fillcolor=color)

        # luz_Verde2 (P5) - estática como en original
        color = "green" if i == 0 else "white"
        etiqueta = "<br/>●" if i == 0 else " "
        self.dot.node('P5', shape='circle', label=f'<<font point-size="20">luz_Verde2{etiqueta}</font>>', style='filled', fillcolor=color)

        # luz_Amarilla2 (P6)
        color = "yellow" if i == 1 else "white"
        etiqueta = "<br/>●" if i == 1 else " "
        self.dot.node('P6', shape='circle', label=f'<<font point-size="20">luz_Amarilla2{etiqueta}</font>>', style='filled', fillcolor=color)

        # luz_Roja2 (P7)
        color = "red" if i == 2 or i == 3 else "white"
        etiqueta = "<br/>●" if i == 3 else ("<br/>●" if i == 2 else " ")
        self.dot.node('P7', shape='circle', label=f'<<font point-size="20">luz_Roja2{etiqueta}</font>>', style='filled', fillcolor=color)

        # espera2 (P8)
        color = "blue" if i == 3 else "white"
        etiqueta = "<br/>●" if i == 3 else " "
        self.dot.node('P8', shape='circle', label=f'<<font point-size="20">espera2{etiqueta}</font>>', style='filled', fillcolor=color)


        # -------- Transiciones --------
        # Definir colores para transiciones usadas
        t1_color = "lightgray" if i == 3 else "white"  # T1 usada en estado 3
        t2_color = "lightgray" if i == 0 else "white"  # T2 usada en estado 3
        t3_color = "lightgray" if i == 2 else "white"  # T3 usada en estado 2
        t4_color = "lightgray" if i == 1 else "white"  # T4 usada en estado 1
        t5_color = "lightgray" if i == 2 else "white"  # T5 usada en estado 2
        t6_color = "lightgray" if i == 0 else "white"  # T6 usada en estado 0

        self.dot.node('T1', shape='box', label='T verde1 -> amarilla1, espera2', 
                    style='filled', fillcolor=t1_color)
        self.dot.node('T2', shape='box', label='T amarilla1 -> roja1', 
                    style='filled', fillcolor=t2_color)
        self.dot.node('T3', shape='box', label='T roja1 -> verde1', 
                    style='filled', fillcolor=t3_color)
        self.dot.node('T4', shape='box', label='T verde2 -> amarilla2, espera1', 
                    style='filled', fillcolor=t4_color)
        self.dot.node('T5', shape='box', label='T amarilla2 -> roja2', 
                    style='filled', fillcolor=t5_color)
        self.dot.node('T6', shape='box', label='T roja2 -> verde2', 
                    style='filled', fillcolor=t6_color)

        # -------- Arcos --------
        self.dot.edge('P1', 'T1')
        self.dot.edge('T1', 'P2')
        self.dot.edge('T1', 'P8')

        self.dot.edge('P2', 'T2')
        self.dot.edge('T2', 'P3')
        self.dot.edge('P3', 'T3')
        self.dot.edge('P4', 'T3')
        self.dot.edge('T3', 'P1')

        self.dot.edge('P5', 'T4')
        self.dot.edge('T4', 'P6')
        self.dot.edge('T4', 'P4')

        self.dot.edge('P6', 'T5')
        self.dot.edge('T5', 'P7')
        self.dot.edge('P7', 'T6')
        self.dot.edge('P8', 'T6')
        self.dot.edge('T6', 'P5')


    def generar_red_cadena(self):
        # Limpiar el grafo
        self.dot.clear()
        
        # Lugares
        self.dot.node('P1', shape='circle', label='Inicio', xlabel=f'{self.lista_chars}', style='filled', fillcolor='green')
        self.dot.node('P2', shape='circle', label='Letras')
        self.dot.node('P3', shape='circle', label='Error')
        self.dot.node('P4', shape='circle', label='A')
        self.dot.node('P5', shape='circle', label='P')
        self.dot.node('P6', shape='circle', label='R')
        self.dot.node('P7', shape='circle', label='O')
        self.dot.node('P8', shape='circle', label='B')
        self.dot.node('P9', shape='circle', label='D')
        self.dot.node('P10', shape='circle', label='Fin')

        # Transiciones
        self.dot.node('T1', shape='box', label='T_1')
        self.dot.node('T2', shape='box', label='T_2')
        self.dot.node('T3', shape='box', label='T_3')
        self.dot.node('T4', shape='box', label='T_4')
        self.dot.node('T5', shape='box', label='T_5')
        self.dot.node('T6', shape='box', label='T_6')
        self.dot.node('T7', shape='box', label='T_7')
        self.dot.node('T8', shape='box', label='T_8')
        self.dot.node('T9', shape='box', label='T_9')
        self.dot.node('T10', shape='box', label='T_10')

        # Arcos
        self.dot.edge('P1', 'T1')
        self.dot.edge('T1', 'P2')
        self.dot.edge('P2', 'P3')
        self.dot.edge('P2', 'T2')
        self.dot.edge('T2', 'P2')
        self.dot.edge('T2', 'P4')
        self.dot.edge('P4', 'T3')
        self.dot.edge('P4', 'T8')
        self.dot.edge('T7', 'P4')
        self.dot.edge('T3', 'P5')
        self.dot.edge('P5', 'T4')
        self.dot.edge('T4', 'P6')
        self.dot.edge('P6', 'T5')
        self.dot.edge('T5', 'P7')
        self.dot.edge('T9', 'P7')
        self.dot.edge('P7', 'T10')
        self.dot.edge('P7', 'T6')
        self.dot.edge('T6', 'P8')
        self.dot.edge('P8', 'T7')
        self.dot.edge('T8', 'P9')
        self.dot.edge('P9', 'T9')
        self.dot.edge('T10', 'P10')
        self.dot.edge('P3', 'P10')

    def red_animada_cadena(self):
        # Limpiar el grafo
        self.dot.clear()
        
        # Actualizar etiquetas según el estado actual
        xlabel = f'{self.lista_chars}'
        
        # Color para elementos activos
        color_activo = "green" if self.estado_actual == 0 else 'white'
        llenado = 'filled' if self.estado_actual == 0 else ''
        
        # Lugares con estado actual
        self.dot.node('P1', shape='circle', label='Inicio', xlabel=xlabel, style=llenado, fillcolor=color_activo)
        
        # Transición T1 activa en estado 1
        lbl = self.letra_actual if self.estado_actual == 1 else ''
        llenado = 'filled' if self.estado_actual == 1 else ''
        color_activo = "green" if self.estado_actual == 1 else 'white'

        self.dot.node('T1', shape='box', label='T_1', xlabel=lbl, style=llenado, fillcolor=color_activo)
        
        # P2 (Letras) activo en estado 2
        lbl = self.letra_actual if self.estado_actual == 2 else ''
        llenado = 'filled' if self.estado_actual == 2 else ''
        color_activo = "green" if self.estado_actual == 2 else 'white'
        self.dot.node('P2', shape='circle', label='Letras', xlabel=lbl, style=llenado, fillcolor=color_activo)

        # P3 error

        lbl = self.letra_actual if self.estado_actual == 2 else ''
        llenado = 'filled' if self.estado_actual == 2 else ''
        color_activo = "green" if self.estado_actual == 2 else 'white'
        self.dot.node('P2', shape='circle', label='Letras', xlabel=lbl, style=llenado, fillcolor=color_activo)
        
        # Resto de nodos (simplificado - puedes añadir más lógica para otros estados)
        self.dot.node('P3', shape='circle', label='Error')
        self.dot.node('P4', shape='circle', label='A')
        self.dot.node('P5', shape='circle', label='P')
        self.dot.node('P6', shape='circle', label='R')
        self.dot.node('P7', shape='circle', label='O')
        self.dot.node('P8', shape='circle', label='B')
        self.dot.node('P9', shape='circle', label='D')
        self.dot.node('P10', shape='circle', label='Fin')

        # Transiciones
        self.dot.node('T2', shape='box', label='T_2')
        self.dot.node('T3', shape='box', label='T_3')
        self.dot.node('T4', shape='box', label='T_4')
        self.dot.node('T5', shape='box', label='T_5')
        self.dot.node('T6', shape='box', label='T_6')
        self.dot.node('T7', shape='box', label='T_7')
        self.dot.node('T8', shape='box', label='T_8')
        self.dot.node('T9', shape='box', label='T_9')
        self.dot.node('T10', shape='box', label='T_10')

        # Arcos (igual que antes)
        self.dot.edge('P1', 'T1')
        self.dot.edge('T1', 'P2')
        self.dot.edge('P2', 'P3')
        self.dot.edge('P2', 'T2')
        self.dot.edge('T2', 'P2')
        self.dot.edge('T2', 'P4')
        self.dot.edge('P4', 'T3')
        self.dot.edge('P4', 'T8')
        self.dot.edge('T7', 'P4')
        self.dot.edge('T3', 'P5')
        self.dot.edge('P5', 'T4')
        self.dot.edge('T4', 'P6')
        self.dot.edge('P6', 'T5')
        self.dot.edge('T5', 'P7')
        self.dot.edge('T9', 'P7')
        self.dot.edge('P7', 'T10')
        self.dot.edge('P7', 'T6')
        self.dot.edge('T6', 'P8')
        self.dot.edge('P8', 'T7')
        self.dot.edge('T8', 'P9')
        self.dot.edge('P9', 'T9')
        self.dot.edge('T10', 'P10')
        self.dot.edge('P3', 'P10')

    def _renderizar(self):
        # Crear la carpeta si no existe
        output_folder = 'red'
        os.makedirs(output_folder, exist_ok=True)
        # Renderizar el archivo
        self.dot.render(filename=self.nombre_archivo, directory=output_folder, cleanup=True)