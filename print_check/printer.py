from print_check.to_pdf import get_pdf
from datetime import datetime


def printer_check(hours: int, name: str, user_id: int, time_start, time_end):

    get_pdf(hours, name, user_id,
            time_start, time_end)

    print('Процесс печати....')

