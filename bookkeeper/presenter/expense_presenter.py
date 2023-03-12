from bookkeeper.models.expense import Expense


class ExpensePresenter:

    def __init__(self, view, cat_repo, exp_repo):
        self.view = view
        self.exp_repo = exp_repo
        self.exp_data = None
        self.repo_cat_data = cat_repo
        self.cat_data = cat_repo.get_all()
        self.view.expense_add_button_clicked(self.handle_expense_add_button_clicked)
        self.view.expense_delete_button_clicked(self.handle_expense_delete_button_clicked)

    def update_expense_data(self):
        self.exp_data = self.exp_repo.get_all()
        if self.exp_data:
            for e in self.exp_data:
                for c in self.cat_data:
                    if c.pk == e.category:
                        e.category = c.name
                        break
            self.view.set_expense_table(self.exp_data)

    def show(self):
        self.view.show()
        self.update_expense_data()
        self.view.set_category_dropdown(self.cat_data)

    def handle_expense_add_button_clicked(self) -> None:
        cat_pk = self.view.get_selected_cat()
        amount = self.view.get_amount()
        expense_date = self.view.get_expense_date()
        exp_comment = self.view.get_comment()
        exp = Expense(int(amount), cat_pk, expense_date, comment=exp_comment)
        self.exp_repo.add(exp)
        self.update_expense_data()

    def handle_expense_delete_button_clicked(self) -> None:
        selected = self.view.get_selected_expenses()
        if selected:
            for e in selected:
                self.exp_repo.delete(e)
            self.update_expense_data()
