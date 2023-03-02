class ExpensePresenter:

    def __init__(self, model, view, cat_repo, exp_repo):
        self.model = model
        self.view = view
        self.data = exp_repo.get_all()

    def show(self):
        self.view.show()
        self.view.set_expense_table(self.data)
