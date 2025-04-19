import datetime
from typing import Any
from langfuse.decorators import observe


@observe()
def get_task_deadline(deadline_date: str) -> int | Any:
    try:
        today_date = datetime.datetime.now().date()
        deadline_date = datetime.datetime.strptime(deadline_date, "%Y-%m-%d").date()
        days_left = (deadline_date - today_date).days
        deadline_utility = max(0, 1 - days_left / 7)
        return deadline_utility
    except Exception as e:
        print(e)
        return 0
