import sys
from icecream import ic
from parser_logic import convert
from PySide6.QtWidgets import QMainWindow, QApplication, QLabel, QErrorMessage, QFileDialog, QComboBox, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QMessageBox

class MyMessageBox(QMessageBox):
    def __init__(self, title='Aviso de actividad', message='mensaje', type='warning'):
        super().__init__()
        self.setWindowTitle(title)
        self.setText(message)
        match(type.lower()):
            case 'warning':
                self.setIcon(self.Icon.Warning)
            case 'information':
                self.setIcon(self.Icon.Information)
            case 'critical':
                self.setIcon(self.Icon.Critical)
            case 'question':
                self.setIcon(self.Icon.Question)
            case _:
                self.setIcon(self.Icon.Warning)
        self.setStandardButtons(QMessageBox.Ok)
        self.setDefaultButton(QMessageBox.Ok)
        
class MyWindow(QMainWindow):
    sel_file_name = ''
    sel_file_type = ''
    save_file_name = ''
    save_file_filter = 'Archivos XML (*.xml)'
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Conversor de preguntas de cuestionario")
        self.setGeometry(400,200,600, 300) # mirar como extraer la posicion intermedia en la ventana
        # Creación del widget principal_layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        # Creación de los layouts
        principal_layout = QVBoxLayout()
        main_widget.setLayout(principal_layout)
        row_01 = QHBoxLayout()
        row_01.addWidget(QLabel("Elige el formato al que quieres exportar"))
        self.combo_box = QComboBox()
        self.combo_box.addItems(['MoodleXML', 'Aiken'])
        self.sel_file_type = self.combo_box.itemText(0)  # Guarda el tipo de archivo seleccionado
        row_01.addWidget(self.combo_box)
        principal_layout.addLayout(row_01)

        row_02 = QHBoxLayout()
        row_02.addWidget(QLabel("Selecciona el archivo origen:"))
        sel_file = QPushButton("Buscar archivo")
        row_02.addWidget(sel_file)
        self.file_name_label = QLabel('Ningún archivo seleccionado')
        row_02.addWidget(self.file_name_label)
        principal_layout.addLayout(row_02)

        row_03 = QHBoxLayout()
        button_convert = QPushButton("Convertir")
        row_03.addWidget(button_convert)
        principal_layout.addLayout(row_03)

        # Conecta los botones a los métodos
        sel_file.clicked.connect(self.chooseFile)
        self.combo_box.currentTextChanged.connect(self.selFileType)
        button_convert.clicked.connect(self.startConversion)

    def chooseFile(self):
        options = QFileDialog.Options() # type: ignore
        file_name, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo de preguntas", "", "Archivos de texto (*.txt)")
        if file_name:
            self.sel_file_name = file_name
            self.file_name_label.setText(self.sel_file_name.split("/")[-1])

    def selFileType(self):
        self.sel_file_type = self.combo_box.currentText()
        match(self.sel_file_type.lower()):
            case 'aiken':
                aviso = MyMessageBox(message='En formato Aiken no se puede aplicar una puntuación por pregunta que no sea 1')
                aviso.exec()
                self.save_file_filter = 'Archivos de texto (*.txt)'
            case 'moodlexml':
                self.save_file_filter = 'Archivos XML (*.xml)'
        ic(self.save_file_filter)

    def startConversion(self):
        if not self.sel_file_name:

            return
        save_options = QFileDialog.Options() # type: ignore
        save_file_name, _ = QFileDialog.getSaveFileName(self, "Guardar archivo convertido", "", self.save_file_filter, options=save_options)
        ic(save_file_name)
        convert(self.sel_file_name, save_file_name, self.sel_file_type)
        aviso = MyMessageBox(message="Se ha completado la conversión del archivo", type="Information")
        aviso.exec()

def __main__():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    __main__()
