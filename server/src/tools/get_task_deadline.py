import datetime

def get_task_deadline(deadline_date: str) -> str:
    today_date = datetime.datetime.now().date()
    deadline_date = datetime.datetime.strptime(deadline_date, "%Y-%m-%d").date()
    days_left = (deadline_date - today_date).days
    deadline_utility = max(0, 1 - days_left/ 7)
    return deadline_utility