class ExpensePresenter:

    def __init__(self, model, view, repo):
        self.model = model
        self.view = view
        self.data = repo.get_all()

    def show(self):
        self.view.show()
        self.view.set_expense_table(self.data)
