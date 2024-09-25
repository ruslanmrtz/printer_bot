from fpdf import FPDF, XPos, YPos
import fitz
from PIL import Image, ImageEnhance
from _datetime import datetime

from cities import cities

def get_time(time_start, time_end):
    date_start = datetime.strftime(time_start, "%d.%m.%Y")
    hours_start = datetime.strftime(time_start, "%H:%M")
    date_end = datetime.strftime(time_end, "%d.%m.%Y")
    hours_end = datetime.strftime(time_end, "%H:%M")

    return date_start, hours_start, date_end, hours_end


def get_pdf(hours: int, name: str, user_id: int,
            time_start, time_end, chef, city, workspace, show: bool = False):

    date_start, hours_start, date_end, hours_end = get_time(time_start, time_end)

    # Создаем PDF-документ
    pdf = FPDF()
    pdf.add_page()

    # Подпись
    sigh = workspace.replace('/', '') if city == 'Сургут' else city

    img_path = f"print_check/sign/{sigh}.png"
    img = Image.open(img_path)

    # Увеличиваем контраст
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(5.0)  # Увеличение контраста

    # Сохраняем временное изображение с улучшенным контрастом
    enhanced_img_path = "print_check/sign/Имя_enhanced.png"
    img.save(enhanced_img_path)

    # Вставляем изображение подписи в PDF (сдвинут влево и увеличен в размере)
    pdf.image(enhanced_img_path, x=48, y=83, w=15 * 2)

    pdf.set_line_width(0.85)

    if show:
        # Рисуем прямоугольник (увеличенные размеры)
        pdf.rect(1, 1, 161, 110)

    # Устанавливаем шрифты
    pdf.add_font("DejaVu", "", "print_check/fonts/DejaVuSans.ttf")  # Обычный
    pdf.add_font("DejaVu", "B", "print_check/fonts/DejaVuSans-Bold.ttf")  # Жирный
    pdf.add_font("DejaVu", "I", "print_check/fonts/DejaVuSerif-Italic.ttf")  # Курсив
    pdf.add_font("DejaVu", "BI", "print_check/fonts/DejaVuSans-BoldOblique.ttf")  # Жирный курсив

    # Устанавливаем шрифт для заголовка (жирный курсив)

    pdf.set_font("DejaVu", "BI", 45)  # Увеличиваем размер шрифта в 2 раза

    # Заголовок по центру
    pdf.set_xy(0, 5)
    if len(name.split()) == 2:
        pdf.cell(161, 14, text=name.split()[0], new_x=XPos.RIGHT, new_y=YPos.TOP, align="C")
        pdf.set_xy(0, 18)
        pdf.cell(161, 14, text=name.split()[1], new_x=XPos.RIGHT, new_y=YPos.TOP, align="C")
    else:
        pdf.cell(161, 14, text=name, new_x=XPos.RIGHT, new_y=YPos.TOP, align="C")

    # Основной текст
    pdf.set_font("DejaVu", "", 24)  # Увеличиваем размер шрифта в 2 раза

    # "Срок хранения"
    pdf.set_xy(1, 32)
    pdf.cell(110 * 2, 10 * 2, text=f"Срок хранения: {hours} ч. t {'от 0 до +6'}", new_x=XPos.RIGHT, new_y=YPos.TOP,
             align="L")

    # Дата и время
    pdf.set_xy(2, 50)  # Увеличенные координаты
    pdf.cell(110 * 2, 10 * 2, text=f"Дата: {date_start}", new_x=XPos.RIGHT, new_y=YPos.TOP, align="L")

    pdf.set_xy(2, 62)  # Увеличенные координаты
    pdf.cell(110 * 2, 10 * 2, text=f"Время: {hours_start}", new_x=XPos.RIGHT, new_y=YPos.TOP, align="L")

    pdf.set_xy(90, 50)  # Увеличенные координаты
    pdf.cell(110 * 2, 10 * 2, text=f"До: {date_end}", new_x=XPos.RIGHT, new_y=YPos.TOP, align="L")

    pdf.set_xy(90, 62)  # Увеличенные координаты
    pdf.cell(110 * 2, 10 * 2, text=f"До: {hours_end}", new_x=XPos.RIGHT, new_y=YPos.TOP, align="L")

    pdf.set_xy(2, 87)  # Увеличенные координаты
    pdf.cell(165, 14, text=f"Ст.повар:             {chef}", new_x=XPos.RIGHT, new_y=YPos.TOP, align="L")

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
