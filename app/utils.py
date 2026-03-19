from datetime import datetime, date


def parse_date(date_val):
    if not date_val:
        return None

    if isinstance(date_val, (date, datetime)):
        return date_val if isinstance(date_val, date) else date_val.date()

    if isinstance(date_val, str):
        for fmt in ('%d/%m/%Y', '%d/%m/%y'):
            try:
                return datetime.strptime(date_val, fmt).date()
            except ValueError:
                continue

    return None
