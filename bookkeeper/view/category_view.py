from collections import deque
from PySide6.QtWidgets import QVBoxLayout, QLabel, QWidget, QLineEdit, QTreeView
from PySide6.QtWidgets import QGridLayout, QComboBox, QPushButton
from PySide6.QtGui import *
from bookkeeper.repository.sqlite_repository import SQLiteRepository


class CategoryWindow(QWidget):

    def __init__(self, data: SQLiteRepository):
        super().__init__()
        self.repo_data = data
        self.tree = QTreeView(self)

        layout = QVBoxLayout(self)
        layout.addWidget(self.tree)
        self.setWindowTitle('Редактирование категорий')
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Категория'])
        self.tree.header().setDefaultSectionSize(180)
        self.tree.setModel(self.model)
        self.re = data.get_all()

        self.data = [{'unique_id': c.pk, 'cat_name': c.name, 'parent': c.parent} for c in self.re]
        self.import_data(self.data)
        self.tree.expandAll()

        self.bottom_controls = QGridLayout()

        self.bottom_controls.addWidget(QLabel('Название новой категории'), 0, 0)
        self.add_category_name = QLineEdit()
        self.bottom_controls.addWidget(self.add_category_name, 0, 1)

        self.bottom_controls.addWidget(QLabel('Выбрать как родительскую категорию\n'
                                              '          или         \nВыбрать для редактирования|удаления'), 1, 0)
        self.category_dropdown = QComboBox()
        self.bottom_controls.addWidget(self.category_dropdown, 1, 1)

        self.category_add_button = QPushButton('Добавить категорию')
        self.bottom_controls.addWidget(self.category_add_button, 2, 0)

        self.category_edit_button = QPushButton('Редактировать категорию')
        self.bottom_controls.addWidget(self.category_edit_button, 2, 1)

        self.category_delete_button = QPushButton('Удалить категорию и записи о расходах')
        self.bottom_controls.addWidget(self.category_delete_button, 3, 1)

        self.bottom_widget = QWidget()
        self.bottom_widget.setLayout(self.bottom_controls)

        layout.addWidget(self.bottom_widget)

        self.setGeometry(300, 100, 500, 300)

    def import_data(self, data: list[dict], root=None):
        self.model.setRowCount(0)
        if root is None:
            root = self.model.invisibleRootItem()
        seen = {}  # List of  QStandardItem
        values = deque(data)
        while values:
            value = values.popleft()
            if value['parent'] is None:
                parent = root
            else:
                pid = value['parent']
                if pid not in seen:
                    values.append(value)
                    continue
                parent = seen[pid]
            unique_id = value['unique_id']
            parent.appendRow([
                QStandardItem(value['cat_name'])
            ])
            seen[unique_id] = parent.child(parent.rowCount() - 1)

    def get_category_name(self) -> str:
        cat_name = self.add_category_name.text()
        if cat_name == "":
            raise Exception("Unrecognized category format")
        return cat_name

    def set_category_dropdown(self, data):
        self.category_dropdown.setMaxCount(0)
        self.category_dropdown.setMaxCount(len(data))
        for c in data:
            self.category_dropdown.addItem(c.name, c.pk)

    def get_selected_parent_cat(self) -> int:
        return self.category_dropdown.itemData(self.category_dropdown.currentIndex())

    def get_selected_cat(self) -> int:
        return self.category_dropdown.itemData(self.category_dropdown.currentIndex())

    def category_add_button_clicked(self, slot):
        self.category_add_button.clicked.connect(slot)

    def category_edit_button_clicked(self, slot):
        self.category_edit_button.clicked.connect(slot)

    def category_delete_button_clicked(self, slot):
        self.category_delete_button.clicked.connect(slot)
