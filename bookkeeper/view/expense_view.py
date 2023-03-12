from PySide6.QtWidgets import QVBoxLayout, QLabel, QWidget, QLineEdit
from PySide6.QtWidgets import QGridLayout, QComboBox, QPushButton
from PySide6 import QtCore, QtWidgets
from bookkeeper.view.category_view import CategoryDialog
from datetime import date, datetime
import re


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
        self.header_names = list(data[0].__dataclass_fields__.keys())

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.header_names[section]
        return super().headerData(section, orientation, role)

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            fields = list(self._data[index.row()].__dataclass_fields__.keys())
            return self._data[index.row()].__getattribute__(fields[index.column()])

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0].__dataclass_fields__)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.item_model = None
        self.setWindowTitle("Программа для ведения бюджета")

        self.layout = QVBoxLayout()

        self.layout.addWidget(QLabel('Последние расходы'))

        self.expenses_grid = QtWidgets.QTableView()
        self.layout.addWidget(self.expenses_grid)

        self.budget_grid = QtWidgets.QTableView()
        self.layout.addWidget(QLabel('Бюджет'))
        self.layout.addWidget(self.budget_grid)

        self.bottom_controls = QGridLayout()

        self.bottom_controls.addWidget(QLabel("Дата транзакции, 'ГГГГ-ММ-ДД'"), 2, 0)
        self.expense_date_line_edit = QLineEdit()
        self.bottom_controls.addWidget(self.expense_date_line_edit, 2, 1)

        self.bottom_controls.addWidget(QLabel('Сумма'), 0, 0)

        self.amount_line_edit = QLineEdit()

        self.bottom_controls.addWidget(self.amount_line_edit, 0, 1)
        self.bottom_controls.addWidget(QLabel('Категория'), 1, 0)

        self.category_dropdown = QComboBox()

        self.bottom_controls.addWidget(self.category_dropdown, 1, 1)

        self.category_edit_button = QPushButton('Редактировать')
        self.bottom_controls.addWidget(self.category_edit_button, 1, 2)
        self.category_edit_button.clicked.connect(self.show_cats_dialog)

        self.expense_add_button = QPushButton('Добавить')
        self.bottom_controls.addWidget(self.expense_add_button, 3, 1)

        self.expense_delete_button = QPushButton('Удалить')
        self.bottom_controls.addWidget(self.expense_delete_button, 3, 2)

        self.bottom_widget = QWidget()
        self.bottom_widget.setLayout(self.bottom_controls)

        self.layout.addWidget(self.bottom_widget)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)

    def set_expense_table(self, data):
        if data:
            self.item_model = TableModel(data)
            self.expenses_grid.setModel(self.item_model)
            self.expenses_grid.resizeColumnsToContents()
            grid_width = sum([self.expenses_grid.columnWidth(x) for x in range(0, self.item_model.columnCount(0) + 1)])
            self.setFixedSize(grid_width + 80, 600)

    def set_category_dropdown(self, data):
        for c in data:
            self.category_dropdown.addItem(c.name, c.pk)

    def expense_add_button_clicked(self, slot):
        self.expense_add_button.clicked.connect(slot)

    def expense_delete_button_clicked(self, slot):
        self.expense_delete_button.clicked.connect(slot)

    def get_amount(self) -> float:
        amount = self.amount_line_edit.text()
        if amount == "":
            return 0
        elif amount.isdigit() or amount[-3] == '.':
            return float(self.amount_line_edit.text())
        else:
            raise Exception("Unrecognized amount format")

    def get_expense_date(self):
        if self.expense_date_line_edit.text() == "":
            return date.today()
        date_string = self.expense_date_line_edit.text()
        date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
        if date_pattern.match(date_string):
            return datetime.strptime(date_string, '%Y-%m-%d').date()
        else:
            raise Exception("Unrecognized datetime format")

    def __get_selected_row_indices(self) -> list[int]:
        if self.expenses_grid.selectionModel():
            return list(set([qmi.row() for qmi in self.expenses_grid.selectionModel().selection().indexes()]))
        return None

    def get_selected_expenses(self) -> list[int] | None:
        idx = self.__get_selected_row_indices()
        if not idx:
            return None
        return [self.item_model._data[i].pk for i in idx]

    def get_selected_cat(self) -> int:
        return self.category_dropdown.itemData(self.category_dropdown.currentIndex())

    def category_edit_button_clicked(self, slot):
        self.category_edit_button.clicked.connect(slot)

    def show_cats_dialog(self, data):
        if data:
            cat_dlg = CategoryDialog(data)
            cat_dlg.setWindowTitle('Редактирование категорий')
            cat_dlg.setGeometry(300, 100, 500, 300)
            cat_dlg.exec()
