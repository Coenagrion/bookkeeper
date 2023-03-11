class Budget:
    """
    Расчет бюджета за последние периоды: день, неделя. месяц, год
    """
    period: str
    max_budget: float = 0.0
    perm_summary: float = 0.0
    budget_left: float = 0.0