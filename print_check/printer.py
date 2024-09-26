from print_check.to_pdf import crop_and_display_pdf
import socket


def printer_check(count_print: int = 1, user_id: int = 0):
    pdf_file = f'print_check/checks/check_{user_id}.pdf'
    image = crop_and_display_pdf(pdf_file, right=460, bottom=313)

    zpl = image_to_zpl(image)

    printer_ip = '192.168.0.65'
    printer_port = 9100
    # Подключаемся к принтеру и отправляем ZPL
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((printer_ip, printer_port))
        for i in range(count_print):
            sock.sendall(zpl.encode('utf-8'))


def image_to_zpl(image):
    """
    Преобразует изображение в ZPL формат для печати на принтере.
    """
    # Конвертируем изображение в черно-белое
    bw_image = image.convert('1')

    # Получаем размеры изображения
    width, height = bw_image.size

    # Преобразуем пиксели в шестнадцатеричный формат для ZPL
    pixels = bw_image.getdata()
    row_bytes = (width + 7) // 8  # Количество байтов в строке
    total_bytes = row_bytes * height
    zpl_data = []

    for y in range(height):
        row_data = []
        for x in range(0, width, 8):
            byte = 0
            for bit in range(8):
                if x + bit < width:
                    pixel = pixels[y * width + x + bit]
                    if pixel == 0:  # Черный пиксель
                        byte |= (1 << (7 - bit))
            row_data.append(f'{byte:02X}')
        zpl_data.append(''.join(row_data))

    zpl_image_data = ''.join(zpl_data)

    # Формируем команду ZPL для печати изображения
    zpl_command = f"""
^XA
^FO173,5
^GFA,{total_bytes},{total_bytes},{row_bytes},{zpl_image_data}
^FS
^XZ
"""

    return zpl_command
