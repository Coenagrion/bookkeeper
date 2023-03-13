from datetime import date, timedelta, datetime
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

    def update_budget_daily(self):
        budget = 0
        if self.exp_repo.get_all():
            for exp in self.exp_repo.get_all():
                if exp.expense_date == str(date.today()):
                    budget += exp.amount
        return budget

    def update_budget_weekly(self):
        budget = 0
        if self.exp_repo.get_all():
            for exp in self.exp_repo.get_all():
                exp_date = datetime.strptime(exp.expense_date, '%Y-%m-%d')
                today_datetime = datetime.combine(date.today(), datetime.min.time())
                if (today_datetime - exp_date) <= timedelta(weeks=1):
                    budget += exp.amount
        return budget

    def update_budget_monthly(self):
        budget = 0
        if self.exp_repo.get_all():
            for exp in self.exp_repo.get_all():
                exp_date = datetime.strptime(exp.expense_date, '%Y-%m-%d')
                today_datetime = datetime.combine(date.today(), datetime.min.time())
                if (today_datetime - exp_date) <= timedelta(days=30):
                    budget += exp.amount
        return budget

    def update_budget_annual(self):
        budget = 0
        if self.exp_repo.get_all():
            for exp in self.exp_repo.get_all():
                exp_date = datetime.strptime(exp.expense_date, '%Y-%m-%d')
                today_datetime = datetime.combine(date.today(), datetime.min.time())
                if (today_datetime - exp_date) <= timedelta(days=365):
                    budget += exp.amount
        return budget

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
        day = self.update_budget_daily()
        week = self.update_budget_weekly()
        month = self.update_budget_monthly()
        year = self.update_budget_annual()
        self.view.set_budget(day, week, month, year)
        self.view.set_category_dropdown(self.cat_data)

    def handle_expense_add_button_clicked(self) -> None:
        cat_pk = self.view.get_selected_cat()
        amount = self.view.get_amount()
        expense_date = self.view.get_expense_date()
        exp_comment = self.view.get_comment()
        exp = Expense(int(amount), cat_pk, expense_date, comment=exp_comment)
        self.exp_repo.add(exp)
        self.update_expense_data()
        day = self.update_budget_daily()
        week = self.update_budget_weekly()
        month = self.update_budget_monthly()
        year = self.update_budget_annual()
        self.view.set_budget(day, week, month, year)

    def handle_expense_delete_button_clicked(self) -> None:
        selected = self.view.get_selected_expenses()
        if selected:
            for e in selected:
                self.exp_repo.delete(e)
            self.update_expense_data()
            day = self.update_budget_daily()
            week = self.update_budget_weekly()
            month = self.update_budget_monthly()
            year = self.update_budget_annual()
            self.view.set_budget(day, week, month, year)
