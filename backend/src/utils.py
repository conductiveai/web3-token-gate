from datetime import datetime, timedelta
from typing import List

from schemas.organization import BreakdownItem


def fill_breakdown(items: List[BreakdownItem]):
    """ fill empty days to make sure there is exactly 30 records in chronological order """

    start_date = datetime.now() - timedelta(days=30)

    for i in range(30):
        date = (start_date + timedelta(days=i)).date()
        if not any(item.label == date for item in items):
            items.append(BreakdownItem(label=date, count=0))

    items.sort(key=lambda item: item.label)

    return items
