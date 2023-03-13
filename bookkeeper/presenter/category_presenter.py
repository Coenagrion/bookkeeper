from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.repository.sqlite_repository import SQLiteRepository


class CategoryPresenter:

    def __init__(self, view, cat_repo: SQLiteRepository, exp_repo: SQLiteRepository):
        self.cat_repo = cat_repo
        self.exp_repo = exp_repo
        self.view = view
        self.view.category_add_button_clicked(self.handle_category_add_button_clicked)
        self.view.category_edit_button_clicked(self.handle_category_edit_button_clicked)
        self.view.category_delete_button_clicked(self.handle_category_delete_button_clicked)

    def show(self) -> None:
        self.view.show()
        self.view.set_category_dropdown(self.cat_repo.get_all())
        data = [{'unique_id': c.pk, 'cat_name': c.name, 'parent': c.parent} for c in self.cat_repo.get_all()]
        self.view.import_data(data)

    def handle_category_add_button_clicked(self) -> None:
        parent_pk = self.view.get_selected_parent_cat()
        new_category_name = self.view.get_category_name()
        cat = Category(new_category_name, parent_pk)
        self.cat_repo.add(cat)
        self.show()

    def handle_category_edit_button_clicked(self) -> None:
        selected = self.view.get_selected_cat()
        new_category_name = self.view.get_category_name()
        cat = Category(name=str(new_category_name), parent=self.cat_repo.get(selected).parent, pk=selected)
        self.cat_repo.update(cat)
        self.show()

    def handle_category_delete_button_clicked(self) -> None:
        selected = self.view.get_selected_cat()
        if selected:
            for e in self.exp_repo.get_all():
                if e.category == selected:
                    self.exp_repo.delete(e.pk)
            self.cat_repo.delete(selected)
        self.show()
