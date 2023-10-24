import sys
from PySide6.QtWidgets import QMainWindow, QApplication, QLabel, QFileDialog, QComboBox, QVBoxLayout, QHBoxLayout, QWidget, QPushButton

class Ventana(QMainWindow):
    
    def __init__(self):
        def chooseFile():
            print("abro ventana de selección")
            vent_aux = QFileDialog()
            vent_aux.show()
        super().__init__()
        self.setWindowTitle("Conversor de preguntas de cuestionario")
        self.setFixedSize(400,300)
        #Creación del widget principal
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        #Creación de los layouts
        principal = QVBoxLayout()
        main_widget.setLayout(principal)
        fila_01 = QHBoxLayout()
        fila_01.addWidget(QLabel("Elige el formato al que quieres exportar"))
        desplegable = QComboBox()
        desplegable.addItems(['Aiken','MoodleXML'])
        fila_01.addWidget(desplegable)
        principal.addLayout(fila_01)

        fila_02 = QHBoxLayout()
        fila_02.addWidget(QLabel("Selecciona el archivo origen:"))
        sel_archivo = QPushButton("Buscar archivo")
        fila_02.addWidget(sel_archivo)
        principal.addLayout(fila_02)
        
        #slots
        sel_archivo.clicked.connect(chooseFile)
        
        

def __main__():
    print("hello world")
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    __main__()