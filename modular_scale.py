import os
import fitz  # PyMuPDF
from PIL import Image, ImageDraw, ImageFont


def escalar_y_modular_un_solo_pdf(input_path, num_modulos=4):
    try:
        original_pdf = fitz.open(input_path)
    except Exception as e:
        return f"❌ Error al abrir el PDF: {e}"

    factor = 4
    dpi = 600

    # Carpeta de salida automática
    input_dir = os.path.dirname(input_path)
    input_name = os.path.splitext(os.path.basename(input_path))[0]
    output_pdf_path = os.path.join(input_dir, f"{input_name}-MOD.pdf")  

    # 1 cm = 28.346 pt
    cm_to_pt = 28.346
        
    # Detectar ancho total desde el nombre del archivo
    
    if "400" in input_name:
        total_ancho_cm = 400
    elif "600" in input_name:
        total_ancho_cm = 600
    else:
        total_ancho_cm = num_modulos * 100  # Valor por defecto

    ancho_por_modulo_cm = total_ancho_cm / num_modulos
    alto_cm = 60 if "60" in input_name else 40  # Detecta altura desde nombre

    real_width_pt = ancho_por_modulo_cm * cm_to_pt
    real_height_pt = alto_cm * cm_to_pt


    documento_modular = fitz.open()  # 🗂️ Un solo PDF final

    for pagina_idx, pagina in enumerate(original_pdf):
        matrix = fitz.Matrix(factor, factor)
        pix = pagina.get_pixmap(matrix=matrix, dpi=dpi)
        img_data = pix.tobytes("png")

        temp_img_path = "temp_full_page.png"
        with open(temp_img_path, "wb") as temp_file:
            temp_file.write(img_data)

        image = Image.open(temp_img_path)
        img_width, img_height = image.size
        modulo_ancho_px = img_width // num_modulos

        for i in range(num_modulos):
            x0 = i * modulo_ancho_px
            x1 = (i + 1) * modulo_ancho_px
            box = (x0, 0, x1, img_height)
            imagen_modulo = image.crop(box)

            # 🖋️ Agregar texto al pie del módulo
            draw = ImageDraw.Draw(imagen_modulo)
            texto = f"{input_name}-{i+1}/{num_modulos}"
            font_size = 40
            try:
                font_path = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
                font = ImageFont.truetype(font_path, font_size)
            except:
                font = ImageFont.load_default()

            bbox = draw.textbbox((0, 0), texto, font=font)
            text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
            x_text = imagen_modulo.width - text_width - 20
            y_text = imagen_modulo.height - text_height - 20
            draw.text((x_text, y_text), texto, font=font, fill=(0, 0, 0))

            # Guardar imagen temporal del módulo
            temp_modulo_img = f"temp_modulo_{i+1}.png"
            imagen_modulo.save(temp_modulo_img)

            # Añadir a PDF final
            nueva_pagina = documento_modular.new_page(width=real_width_pt, height=real_height_pt)
            nueva_pagina.insert_image(fitz.Rect(0, 0, real_width_pt, real_height_pt), filename=temp_modulo_img)
            os.remove(temp_modulo_img)

        os.remove(temp_img_path)

    documento_modular.save(output_pdf_path)
    documento_modular.close()
    return f"✅ PDF con módulos exportado en: {output_pdf_path}"


def menu_escalar_y_modular():
    print("🧰 MODULAR PDF COMO UN SOLO ARCHIVO MULTIPÁGINA")
    input_path = input("📂 Ruta completa del PDF de entrada: ").strip()
    num_modulos = int(input("🔢 ¿En cuántos módulos horizontales quieres dividir? (4 o 6): ").strip())

    print("⏳ Procesando...")

    resultado = escalar_y_modular_un_solo_pdf(input_path=input_path, num_modulos=num_modulos)
    print(resultado)


if __name__ == "__main__":
    menu_escalar_y_modular()
