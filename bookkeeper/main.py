from PySide6.QtWidgets import QVBoxLayout, QLabel, QWidget, QGridLayout, QComboBox, QLineEdit, QPushButton

from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.utils import read_tree

import sys
from PySide6 import QtCore, QtWidgets

cat_repo = SQLiteRepository[Category]('test.db', Category)  # TODO: репозиторий sqlite пока не реализован


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Программа для ведения бюджета")
        self.setFixedSize(500, 600)

        self.layout = QVBoxLayout()

        self.layout.addWidget(QLabel('Последние расходы'))

        self.expenses_grid = QtWidgets.QTableView()
        self.layout.addWidget(self.expenses_grid)

        self.layout.addWidget(QLabel('Бюджет'))
        self.layout.addWidget(QLabel('<TODO: таблица бюджета>\n\n\n\n\n\n\n\n'))

        bottom_controls = QGridLayout()

        bottom_controls.addWidget(QLabel('Сумма'), 0, 0)

        amount_line_edit = QLineEdit()

        bottom_controls.addWidget(amount_line_edit, 0, 1)
        #bottom_controls.addWidget(QLabel('=============='), 0, 2)
        bottom_controls.addWidget(QLabel('Категория'), 1, 0)

        category_dropdown = QComboBox()
        category_dropdown.addItems(['Продукты', 'Тест', 'Тест'])

        bottom_controls.addWidget(category_dropdown, 1, 1)

        category_edit_button = QPushButton('Редактировать')
        bottom_controls.addWidget(category_edit_button, 1, 2)

        expense_add_button = QPushButton('Добавить')
        bottom_controls.addWidget(expense_add_button, 2, 1)

        bottom_widget = QWidget()
        bottom_widget.setLayout(bottom_controls)

        self.layout.addWidget(bottom_widget)

        data = cat_repo.get_all()

        self.model = TableModel(data)
        self.expenses_grid.setModel(self.model)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
