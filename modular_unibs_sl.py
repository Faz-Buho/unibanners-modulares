import os
import fitz  # PyMuPDF
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import tempfile

# 🔧 Configuración de la página (debe ir primero)
st.set_page_config(page_title="Modularizador PDF", layout="centered")

# 🖼️ Banner o logo en la parte superior
st.image("assets/banner.png", use_container_width=True)


def escalar_y_modular_un_solo_pdf_streamlit(uploaded_file, num_modulos):
    factor = 4
    dpi = 600

    # Guardar archivo temporalmente
    temp_dir = tempfile.mkdtemp()
    input_path = os.path.join(temp_dir, uploaded_file.name)
    with open(input_path, "wb") as f:
        f.write(uploaded_file.read())

    input_name = os.path.splitext(uploaded_file.name)[0]
    output_pdf_path = os.path.join(temp_dir, f"{input_name}-MOD.pdf")

    try:
        original_pdf = fitz.open(input_path)
    except Exception as e:
        return None, f"❌ Error al abrir el PDF: {e}"

    # Ajuste automático de altura según nombre del archivo
    if "4x60" in input_name or "6x60" in input_name:
        real_height_cm = 60
    else:
        real_height_cm = 40
    real_width_cm = 100  # Siempre 100 cm por módulo

    cm_to_pt = 28.346
    real_width_pt = real_width_cm * cm_to_pt
    real_height_pt = real_height_cm * cm_to_pt

    documento_modular = fitz.open()

    for pagina in original_pdf:
        matrix = fitz.Matrix(factor, factor)
        pix = pagina.get_pixmap(matrix=matrix, dpi=dpi)
        img_data = pix.tobytes("png")

        temp_img_path = os.path.join(temp_dir, "temp_full_page.png")
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

            # 🖋️ Texto en la parte inferior derecha
            draw = ImageDraw.Draw(imagen_modulo)
            texto = f"{input_name}-{i+1}/{num_modulos}"
            font_size = 40
            try:
                font_path = "assets/Arial-Bold.ttf"  # nombre igual al archivo real
                font = ImageFont.truetype(font_path, font_size)

            except:
                font = ImageFont.load_default()

            bbox = draw.textbbox((0, 0), texto, font=font)
            text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
            x_text = imagen_modulo.width - text_width - 20
            y_text = imagen_modulo.height - text_height - 20
            draw.text((x_text, y_text), texto, font=font, fill=(0, 0, 0))

            temp_modulo_img = os.path.join(temp_dir, f"temp_modulo_{i+1}.png")
            imagen_modulo.save(temp_modulo_img)

            nueva_pagina = documento_modular.new_page(width=real_width_pt, height=real_height_pt)
            nueva_pagina.insert_image(
                fitz.Rect(0, 0, real_width_pt, real_height_pt),
                filename=temp_modulo_img
            )

    documento_modular.save(output_pdf_path)
    documento_modular.close()

    with open(output_pdf_path, "rb") as f:
        result_bytes = f.read()

    return result_bytes, f"✅ PDF con módulos exportado correctamente"


# 🧩 Interfaz de Streamlit
st.title("MODULAR UNIBANNERS")

uploaded_file = st.file_uploader("📂 Sube tu archivo PDF", type=["pdf"])

if uploaded_file:
    num_modulos = st.selectbox("🔢 ¿En cuántos módulos quieres dividir?", [4, 6])

    if st.button("Procesar PDF"):
        with st.spinner("⏳ Procesando..."):
            output_data, mensaje = escalar_y_modular_un_solo_pdf_streamlit(uploaded_file, num_modulos)

        if output_data:
            st.success(mensaje)
            st.download_button(
                label="⬇️ Descargar PDF modular",
                data=output_data,
                file_name=f"{os.path.splitext(uploaded_file.name)[0]}-MOD.pdf",
                mime="application/pdf"
            )
        else:
            st.error(mensaje)
