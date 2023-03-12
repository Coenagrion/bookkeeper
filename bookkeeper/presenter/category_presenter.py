from bookkeeper.models.category import Category
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.presenter.expense_presenter import ExpensePresenter


class CategoryPresenter:

    def __init__(self, view, cat_repo: SQLiteRepository):
        self.cat_repo = cat_repo
        self.view = view
        self.view.category_add_button_clicked(self.handle_category_add_button_clicked)

    def show(self):
        self.view.show()
        self.view.set_category_dropdown(self.cat_repo.get_all())

    def handle_category_add_button_clicked(self) -> None:
        parent_pk = self.view.get_selected_parent_cat()
        new_category_name = self.view.get_category_name()
        cat = Category(new_category_name, parent_pk)
        self.cat_repo.add(cat)
        self.show()

