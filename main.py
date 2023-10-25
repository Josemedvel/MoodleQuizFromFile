import sys
from icecream import ic
from parser_logic import convert
from PySide6.QtWidgets import QMainWindow, QApplication, QLabel, QErrorMessage, QFileDialog, QComboBox, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QMessageBox

class Ventana(QMainWindow):
    sel_file_name = ''
    sel_file_type = ''
    save_file_name = ''
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Conversor de preguntas de cuestionario")
        self.setFixedSize(600, 300)
        # Creación del widget principal_layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        # Creación de los layouts
        principal_layout = QVBoxLayout()
        main_widget.setLayout(principal_layout)
        row_01 = QHBoxLayout()
        row_01.addWidget(QLabel("Elige el formato al que quieres exportar"))
        combo_box = QComboBox()
        combo_box.addItems(['MoodleXML', 'Aiken'])
        self.sel_file_type = combo_box.itemText(0)  # Guarda el tipo de archivo seleccionado
        row_01.addWidget(combo_box)
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
        button_convert.clicked.connect(self.startConversion)

    def chooseFile(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo de preguntas", "", "Archivos de texto (*.txt);;Todos los archivos (*)")
        if file_name:
            self.sel_file_name = file_name
            self.file_name_label.setText(self.sel_file_name.split("/")[-1])

    def startConversion(self):
        if not self.sel_file_name:
            return
        save_options = QFileDialog.Options()
        save_file_name, _ = QFileDialog.getSaveFileName(self, "Guardar archivo convertido", "", "Archivos XML (*.xml);;Todos los archivos (*)",options=save_options)
        ic(save_file_name)
        convert(self.sel_file_name, save_file_name, self.sel_file_type)
        aviso = QMessageBox()
        aviso.setInformativeText("Se ha completado la conversión del archivo")
        aviso.setWindowTitle("Aviso de actividad")
        aviso.setStandardButtons(QMessageBox.Discard)
        aviso.setDefaultButton(QMessageBox.Discard)
        aviso.setIcon(QMessageBox.Icon.Information)
        aviso.exec()

def __main__():
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    __main__()
