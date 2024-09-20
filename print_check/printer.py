from to_pdf import get_pdf


def printer_check(hours: int, name: str, user_id: int):
    get_pdf(hours, name, user_id)

    print('Процесс печати....')

