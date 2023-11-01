import sys
from icecream import ic
from parser_logic import convert
from PySide6.QtWidgets import QMainWindow, QApplication, QLabel, QCheckBox, QFileDialog, QComboBox, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QMessageBox, QButtonGroup, QRadioButton

class MyMessageBox(QMessageBox):
    def __init__(self, title='warning_box de actividad', message='mensaje', type='warning'):
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
    blank_answ_state = False
    blank_answ_check = ''
    sel_pen_type = None
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Conversor de preguntas de cuestionario")
        self.setGeometry(400,200,600, 300) # mirar como extraer la posicion intermedia en la ventana
        # Creación del widget principal_layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        # Creación de los layouts
        principal_layout = QVBoxLayout()
        principal_layout.addSpacing(25)
        main_widget.setLayout(principal_layout)
        row_01 = QHBoxLayout()
        row_01.addStretch()
        row_01.addWidget(QLabel("Elige el formato al que quieres exportar:"))
        row_01.addSpacing(25)
        self.combo_box = QComboBox()
        self.combo_box.addItems(['MoodleXML', 'Aiken'])
        self.sel_file_type = self.combo_box.itemText(0)  # Guarda el tipo de archivo seleccionado
        row_01.addWidget(self.combo_box)
        row_01.addStretch()
        principal_layout.addLayout(row_01)
        principal_layout.addStretch()
        
        row_02 = QHBoxLayout()
        row_02.addStretch()
        self.blank_answ_check = QCheckBox('Añadir respuesta en blanco')
        row_02.addWidget(self.blank_answ_check)
        row_02.addStretch()
        row_02.addWidget(QLabel('Penalización:'))
        self.sel_pen_type = QButtonGroup(self)
        option_01 = QRadioButton('Repartida', self)
        option_01.setChecked(True)
        option_02 = QRadioButton('Media', self)
        self.sel_pen_type.addButton(option_01)
        self.sel_pen_type.addButton(option_02)
        row_02.addWidget(option_01)
        row_02.addWidget(option_02)
        row_02.addStretch()
        principal_layout.addLayout(row_02)
        principal_layout.addStretch()

        row_03 = QHBoxLayout()
        row_03.addStretch()
        row_03.addWidget(QLabel("Selecciona el archivo origen:"))
        row_03.addSpacing(25)
        sel_file = QPushButton("Buscar archivo")
        row_03.addWidget(sel_file)
        row_03.addSpacing(25)
        self.file_name_label = QLabel('Ningún archivo seleccionado')
        row_03.addWidget(self.file_name_label)
        row_03.addStretch()
        principal_layout.addLayout(row_03)
        principal_layout.addStretch()

        row_04 = QHBoxLayout()
        button_convert = QPushButton("Convertir")
        row_04.addWidget(button_convert)
        principal_layout.addLayout(row_04)

        # Conecta los elementos de interacción a los métodos
        sel_file.clicked.connect(self.chooseFile)
        self.combo_box.currentTextChanged.connect(self.selFileType)
        self.blank_answ_check.stateChanged.connect(self.changeBlankState)
        button_convert.clicked.connect(self.startConversion)
        #sel_pen_type.

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
                warning_box = MyMessageBox(message='En formato Aiken no se puede aplicar una puntuación por pregunta que no sea 1')
                warning_box.exec()
                self.save_file_filter = 'Archivos de texto (*.txt)'
            case 'moodlexml':
                self.save_file_filter = 'Archivos XML (*.xml)'
        ic(self.save_file_filter)

    def changeBlankState(self):
        self.blank_answ_state = True if self.blank_answ_check.checkState().name.lower() == 'checked' else False
    def startConversion(self):
        if not self.sel_file_name:
            warning_box = MyMessageBox(message='No tienes ningún archivo seleccionado', type='warning')
            warning_box.exec()
            return
        save_options = QFileDialog.Options() # type: ignore
        save_file_name, _ = QFileDialog.getSaveFileName(self, "Guardar archivo convertido", "", self.save_file_filter, options=save_options)
        #ic(save_file_name)
        penalization_type = self.sel_pen_type.checkedButton().text()
        convert(self.sel_file_name, save_file_name, self.blank_answ_state, penalization_type, self.sel_file_type)
        warning_box = MyMessageBox(message="Se ha completado la conversión del archivo", type="Information")
        warning_box.exec()

def __main__():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    __main__()
