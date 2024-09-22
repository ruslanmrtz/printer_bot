from fpdf import FPDF, XPos, YPos
import fitz
from PIL import Image
from _datetime import datetime


def get_time(time_start, time_end):
    date_start = datetime.strftime(time_start, "%d.%m.%Y")
    hours_start = datetime.strftime(time_start, "%H:%M")
    date_end = datetime.strftime(time_end, "%d.%m.%Y")
    hours_end = datetime.strftime(time_end, "%H:%M")

    return date_start, hours_start, date_end, hours_end


def get_pdf(hours: int, name: str, user_id: int,
            time_start, time_end):

    date_start, hours_start, date_end, hours_end = get_time(time_start, time_end)

    # Создаем PDF-документ
    pdf = FPDF()
    pdf.add_page()

    pdf.set_line_width(0.85)

    # Устанавливаем шрифты
    pdf.add_font("DejaVu", "", "print_check/fonts/DejaVuSans.ttf")  # Обычный
    pdf.add_font("DejaVu", "B", "print_check/fonts/DejaVuSans-Bold.ttf")  # Жирный
    pdf.add_font("DejaVu", "I", "print_check/fonts/DejaVuSerif-Italic.ttf")  # Курсив
    pdf.add_font("DejaVu", "BI", "print_check/fonts/DejaVuSans-BoldOblique.ttf")  # Жирный курсив

    # Рисуем прямоугольник (50 мм от левого края, 40 мм от верхнего края, ширина 80 мм, высота 30 мм)
    pdf.rect(50, 40, 81, 30)

    # Устанавливаем шрифт для заголовка (жирный курсив)
    pdf.set_font("DejaVu", "BI", 14)

    # Заголовок "ЗЕЛЕНЫЙ ЛУК" большими буквами по центру
    pdf.set_xy(50, 40)
    pdf.cell(80, 7, text=name, new_x=XPos.RIGHT, new_y=YPos.TOP, align="C")

    # Устанавливаем шрифт для основного текста
    pdf.set_font("DejaVu", "", 12)

    # Пишем "Срок хранения" слева
    pdf.set_xy(50, 45)
    pdf.cell(110, 10, text=f"Срок хранения: {hours} ч. при t +2...+4", new_x=XPos.RIGHT, new_y=YPos.TOP, align="L")

    # Следующая строка для даты
    pdf.set_xy(52, 50)  # Устанавливаем координаты для даты
    pdf.cell(110, 10, text=f"Дата: {date_start}", new_x=XPos.RIGHT, new_y=YPos.TOP, align="L")
    # Следующая строка для часа
    pdf.set_xy(95, 50)  # Устанавливаем координаты для часа
    pdf.cell(110, 10, text=f"Время: {hours_start}", new_x=XPos.RIGHT, new_y=YPos.TOP, align="L")

    # Следующая строка для даты
    pdf.set_xy(54, 55)  # Устанавливаем координаты для даты
    pdf.cell(110, 10, text=f"До: {date_end}", new_x=XPos.RIGHT, new_y=YPos.TOP, align="L")

    # Следующая строка для часа
    pdf.set_xy(98, 55)  # Устанавливаем координаты для часа
    pdf.cell(110, 10, text=f"До: {hours_end}", new_x=XPos.RIGHT, new_y=YPos.TOP, align="L")


    # Рисуем линию после строки с часом
    # pdf.set_xy(50, 90)  # Устанавливаем координаты для линии
    # pdf.line(50, 91, 140, 91)  # Рисуем линию от (50, 91) до (140, 91)

    # Устанавливаем координаты для подписи
    pdf.set_xy(52, 61)
    pdf.cell(90, 10, text="Ст.повар _______ Муртазин Р.Ш.", new_x=XPos.RIGHT, new_y=YPos.TOP, align="L")

    # Сохраняем PDF-документ
    pdf.output(f"print_check/checks/check_{user_id}.pdf")

    print("PDF успешно создан!")


def crop_and_display_pdf(pdf_path, left=0, top=0, right=0, bottom=0):
    """
    Функция для обрезки этикетки PDF и отображения её в Streamlit.

    :param pdf_path: Путь к загруженному PDF файлу
    :param left: Левая граница обрезки (по умолчанию 0)
    :param top: Верхняя граница обрезки (по умолчанию 0)
    :param right: Правая граница обрезки (по умолчанию 0 - обрезка по всей ширине)
    :param bottom: Нижняя граница обрезки (по умолчанию 0 - обрезка по всей высоте)
    """

    # Открываем PDF файл
    document = fitz.open(pdf_path)
    page = document[0]  # Получаем первую страницу

    # Рендерим страницу в изображение
    pix = page.get_pixmap()

    # Преобразуем в PIL изображение
    image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    # Если правый или нижний край не задан, используем полную ширину/высоту изображения
    right = right if right > 0 else image.width
    bottom = bottom if bottom > 0 else image.height

    # Обрезка изображения
    cropped_image = image.crop((left, top, right, bottom))


    return cropped_image
