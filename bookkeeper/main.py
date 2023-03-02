from PySide6.QtWidgets import QApplication
from bookkeeper.view.expense_view import MainWindow
from bookkeeper.presenter.expense_presenter import ExpensePresenter
from bookkeeper.models.category import Category
from bookkeeper.repository.sqlite_repository import SQLiteRepository
import sys

DB_NAME = 'test.db'

if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = MainWindow()
    model = None  # TODO: здесь должна быть модель
    cat_repo = SQLiteRepository[Category](DB_NAME, Category)  # TODO: здесь должны быть расходы
    window = ExpensePresenter(model, view, cat_repo)  # TODO: передать три репозитория
    window.show()
    app.exec_()
