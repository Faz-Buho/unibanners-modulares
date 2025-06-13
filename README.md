# 📐 Modularizador de PDFs – UNIBANNERS

Una herramienta desarrollada en Python con Streamlit que permite dividir un archivo PDF horizontalmente en 4 o 6 módulos iguales, conservando calidad y añadiendo una etiqueta con el nombre del archivo y el número de módulo.

Ideal para impresión modular de banners grandes.

---

## 🧰 Funcionalidades

- 📤 Subida de archivos PDF
- 📏 División automática en 4 o 6 módulos de 100x40cm o 100x60cm
- 🖨️ Escalado 4x y rasterización en 600 DPI
- 📝 Agrega texto identificador en cada módulo (Ej: `archivo-1/6`)
- 📥 Descarga en un solo PDF multipágina

---

## 🖥️ Instalación Local

1. **Clona el repositorio**  
   ```bash
   git clone https://github.com/tu-usuario/modularizador-unibanners.git
   cd modularizador-unibanners
Crea un entorno virtual (opcional pero recomendado)

bash
Copiar
Editar
python3 -m venv .env
source .env/bin/activate
Instala las dependencias

bash
Copiar
Editar
pip install -r requirements.txt
Ejecuta la app

bash
Copiar
Editar
streamlit run modular_unibs_sl.py
☁️ Deploy en Streamlit Cloud
Ve a: https://streamlit.io/cloud

Conecta tu cuenta de GitHub

Sube el proyecto a un repositorio y selecciona el archivo modular_unibs_sl.py como entrada

Asegúrate de incluir estos archivos en el repo:

modular_unibs_sl.py

requirements.txt

/assets/banner.png

📦 Estructura del Proyecto
bash
Copiar
Editar
📁 modularizador-unibanners/
├── modular_unibs_sl.py          # Código principal
├── requirements.txt             # Dependencias
├── README.md                    # Este archivo
└── assets/
    └── banner.png               # Imagen superior para la app
🧪 Requisitos Técnicos
Python ≥ 3.8

PyMuPDF (fitz)

Pillow (PIL)

Streamlit

🙌 Créditos
Desarrollado por Pablo Faz para automatizar la preparación de archivos de impresión modular en banners.# unibanners-modulares
