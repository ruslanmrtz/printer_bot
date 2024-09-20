from fpdf import FPDF, XPos, YPos


def get_pdf(hours: int, name: str, user_id: int):
    # Создаем PDF-документ
    pdf = FPDF()
    pdf.add_page()

    # Устанавливаем шрифты
    pdf.add_font("DejaVu", "", "print_check/fonts/DejaVuSans.ttf")  # Обычный
    pdf.add_font("DejaVu", "B", "print_check/fonts/DejaVuSans-Bold.ttf")  # Жирный
    pdf.add_font("DejaVu", "I", "print_check/fonts/DejaVuSerif-Italic.ttf")  # Курсив
    pdf.add_font("DejaVu", "BI", "print_check/fonts/DejaVuSans-BoldOblique.ttf")  # Жирный курсив

    # Рисуем прямоугольник (50 мм от левого края, 40 мм от верхнего края, ширина 90 мм, высота 65 мм)
    pdf.rect(50, 40, 90, 65)

    # Устанавливаем шрифт для заголовка (жирный курсив)
    pdf.set_font("DejaVu", "BI", 16)

    # Заголовок "ЗЕЛЕНЫЙ ЛУК" большими буквами по центру
    pdf.set_xy(50, 45)
    pdf.cell(90, 10, text=name, new_x=XPos.RIGHT, new_y=YPos.TOP, align="C")

    # Устанавливаем шрифт для основного текста
    pdf.set_font("DejaVu", "", 12)

    # Пишем "Срок хранения" слева
    pdf.set_xy(50, 55)
    pdf.cell(110, 10, text=f"Срок хранения: {hours} ч. при t +2...+4", new_x=XPos.RIGHT, new_y=YPos.TOP, align="L")

    # Следующая строка для даты
    pdf.set_xy(50, 65)  # Устанавливаем координаты для даты
    pdf.cell(110, 10, text="Дата: __________________________________", new_x=XPos.RIGHT, new_y=YPos.TOP, align="L")

    # Следующая строка для часа
    pdf.set_xy(50, 75)  # Устанавливаем координаты для часа
    pdf.cell(110, 10, text="Час: ____________________________________", new_x=XPos.RIGHT, new_y=YPos.TOP, align="L")

    # Рисуем линию после строки с часом
    pdf.set_xy(50, 90)  # Устанавливаем координаты для линии
    pdf.line(50, 91, 140, 91)  # Рисуем линию от (50, 91) до (140, 91)

    # Устанавливаем координаты для подписи
    pdf.set_xy(50, 93)
    pdf.cell(90, 10, text="Муртазин Р.Ш.", new_x=XPos.RIGHT, new_y=YPos.TOP, align="L")

    # Сохраняем PDF-документ
    pdf.output(f"print_check/check/check_{user_id}.pdf")

    print("PDF успешно создан!")