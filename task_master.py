import sys

from PySide6 import QtCore
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import *


# Creamos un widget personalizado que agregará el texto y botones a nuestra lista de tareas.
class CustomTaskWidget(QWidget):
    def __init__(self, task):
        super().__init__()

        self.task = QLabel(task)
        self.done = QCheckBox('Completado')
        self.done.stateChanged.connect(self.update_status)
        self.edit_button = QPushButton("Editar")
        self.edit_button.setFixedSize(60, 35)
        self.edit_button.clicked.connect(self.edit_task)
        self.delete_button = QPushButton("Eliminar")
        self.delete_button.setFixedSize(60, 35)
        self.delete_button.clicked.connect(self.delete_task)

        layout = QHBoxLayout()
        layout.addWidget(self.task)
        layout.addWidget(self.done)
        layout.addWidget(self.edit_button)
        layout.addWidget(self.delete_button)
        self.setLayout(layout)

    def edit_task(self):
        pass

    def delete_task(self):
        pass

    def update_status(self, state):
        if state == Qt.Checked:
            self.task.setStyleSheet("text-decoration: line")
        else:
            self.task.setStyleSheet("")


# Creamos la ventana principal.
class WindowTaskMaster(QMainWindow):
    def __init__(self):
        super().__init__()
        # Cambiamos el título de la ventana.
        self.setWindowTitle('TASK MASTER')
        # Definimos el tamaño de la ventana.
        self.resize(800, 600)
        # Llamamos a la función que creara los demás componentes o widgets de nuestra app.
        self._agregar_componentes()
        self.task = None

    # Función que creara los componentes.
    def _agregar_componentes(self):
        # Agregamos una barra de menu.
        menu = self.menuBar()
        # Agregamos el menu archivo.
        menu_archivo = menu.addMenu('Archivo')
        # Agregamos una opción al menu archivo.
        accion_nuevo = QAction('Nueva Tarea', self)
        menu_archivo.addAction(accion_nuevo)
        # Hacemos que se muestre en la barra de estado.
        accion_nuevo.setStatusTip('Nueva Tarea')
        # Mostramos la barra de estado.
        self.statusBar().showMessage('Barra de estado..')

        # Preparamos en la ventana cuál será la disposición de componentes.
        # Los componentes se organizarán en un grid.
        layout = QGridLayout()

        # Creamos una etiqueta.
        self.task_label = QLabel('Agregar Tarea:')
        self.task_label.setAlignment(Qt.AlignCenter)
        # Asignamos una posición a la etiqueta en el layout.
        layout.addWidget(self.task_label, 0, 0)

        # Creamos la entrada de texto donde definiremos las tareas.
        self.task_entry = QLineEdit()
        self.task_entry.setPlaceholderText('Agregar una tarea')
        # Asignamos una posición a la entrada de texto en el layout.
        layout.addWidget(self.task_entry, 0, 1, 1, 6)

        self.pick_date_label = QLabel('Elegir una fecha')
        layout.addWidget(self.pick_date_label, 1, 1)

        self.pick_date = QDateEdit()
        default_date = QtCore.QDate.currentDate()
        self.pick_date.setDate(default_date)
        self.pick_date.setCalendarPopup(True)
        self.pick_date.setDisplayFormat('dd/MM/yyyy')
        layout.addWidget(self.pick_date, 1, 2)

        self.pick_time_label = QLabel("Elegir una hora")
        layout.addWidget(self.pick_time_label, 1, 3)

        self.pick_hour = QTimeEdit(None)
        default_time = QtCore.QTime(8, 0)
        self.pick_hour.setTime(default_time)
        self.pick_hour.setDisplayFormat("HH:mm")
        layout.addWidget(self.pick_hour, 1, 4)

        self.set_alarm = QCheckBox('Establecer Alarma')
        self.set_alarm.stateChanged.connect(self.start_alarm)
        layout.addWidget(self.set_alarm, 1, 5)

        # Creamos el botón de guardar tarea.
        self.save_task_button = QPushButton('Guardar Tarea')
        # Asociamos el accionar del botón a un evento o función.
        self.save_task_button.clicked.connect(self.guardar_tarea)
        # Asignamos una posición al botón de guardar en el layout.
        layout.addWidget(self.save_task_button, 1, 6)

        self.task_list = QListWidget(None)
        layout.addWidget(self.task_list, 2, 0, 3, 8)

        # Creamos el contenedor donde se ubicaran los componentes en la ventana principal.
        container = QWidget(None)
        container.setLayout(layout)
        self.setCentralWidget(container)

    # Creamos la función que ejecuta el accionar del botón.
    def guardar_tarea(self):
        self.task = f'{self.task_entry.text()} \nVence el: {self.pick_date.text()} a las {self.pick_hour.text()}'
        if self.task:
            new_task_item = CustomTaskWidget(self.task)
            new_task_item.edit_button.clicked.connect(self.edit_task)
            new_task_item.delete_button.clicked.connect(self.delete_task)
            task_list_item = QListWidgetItem()
            task_list_item.setSizeHint(new_task_item.sizeHint())
            self.task_list.addItem(task_list_item)
            self.task_list.setItemWidget(task_list_item, new_task_item)
            self.task_entry.clear()

    def start_alarm(self):
        pass

    def edit_task(self):
        selected_task = self.task_list.currentItem()
        if selected_task:
            index = self.task_list.row(selected_task)
            task_item = self.task_list.item(index)
            task_widget = self.task_list.itemWidget(task_item)
            label = task_widget.task
            texto = label.text()
            self.task_entry.setText(texto)
            self.task_list.takeItem(index)
        print('Se ha hecho click en el botón Editar')

    def delete_task(self):
        selected_task = self.task_list.currentItem()
        if selected_task:
            index = self.task_list.row(selected_task)
            self.task_list.takeItem(index)
        print('Se ha hecho click en el botón Eliminar')


if __name__ == '__main__':
    app = QApplication()
    window = WindowTaskMaster()
    window.show()
    sys.exit(app.exec())
