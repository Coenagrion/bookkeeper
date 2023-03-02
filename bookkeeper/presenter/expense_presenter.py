from bookkeeper.models.expense import Expense

class ExpensePresenter:

    def __init__(self, model, view, cat_repo, exp_repo):
        self.model = model
        self.view = view
        self.exp_repo = exp_repo
        self.exp_data = self.exp_repo.get_all()
        self.cat_data = cat_repo.get_all()
        self.view.on_expense_add_button_clicked(self.handle_expense_add_button_clicked)

    def update_expense_data(self):
        self.exp_data = self.exp_repo.get_all()
        self.view.set_expense_table(self.exp_data)

    def show(self):
        self.view.show()
        self.update_expense_data()
        self.view.set_category_dropdown(self.cat_data)

    def handle_expense_add_button_clicked(self):
        cat_pk = self.view.get_selected_cat()
        amount = self.view.get_amount()
        exp = Expense(int(amount), cat_pk)
        self.exp_repo.add(exp)
        self.update_expense_data()
