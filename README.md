# 🕮 Manhwa Downloader

Este proyecto permite descargar automáticamente todos los capítulos de un manhwa desde [olympusbiblioteca.com](https://olympusbiblioteca.com), guardando las imágenes de cada capítulo y generando archivos PDF organizados.  

La herramienta detecta automáticamente el nombre del manhwa desde la URL y crea una carpeta padre con subcarpetas para imágenes y PDFs.  

---

## 📂 Estructura del Proyecto
```
manwha_scraper/
│── api/
│   ├── __init__.py
│   └── chapters_api.py
│
│── downloaders/
│   ├── __init__.py
│   ├── image_downloader.py
│   └── pdf_generator.py
│
│── main.py
│── requirements.txt
│── README.md
│── output/  (generada automáticamente)
```
---

## ⚙️ Funcionamiento

1. **Obtención de capítulos**  
   - `ChaptersAPI` consulta el endpoint de capítulos y devuelve un listado con `id` y `name` de cada uno.

2. **Descarga de imágenes**  
   - `ImagesAPI` obtiene las URLs de imágenes de cada capítulo.
   - `DownloaderService` descarga y organiza las imágenes en `output/<manhwa>/images/<capítulo>/`.

3. **Generación de PDFs**  
   - `PDFGenerator` crea un archivo PDF por cada capítulo usando las imágenes descargadas.
   - Los PDFs se guardan en `output/<manhwa>/pdfs/`.

4. **Carpeta dinámica**  
   - El nombre de la carpeta principal (`output/<manhwa>`) se genera automáticamente a partir del `slug` del manhwa en la URL.

---

## 🛠️ Personalizar para otro manhwa

Para usar el script con otro manhwa:

1. Abre `main.py`.
2. Modifica la variable la variable slug 

```
SLUG = "el-asesino-yu-ijin20250729-110824049"

BASE_URL = f"https://dashboard.olympusbiblioteca.com/api/series/{SLUG}/chapters?page=1&direction=desc&type=comic"
CHAPTER_URL_TEMPLATE = f"https://olympusbiblioteca.com/api/capitulo/{SLUG}/{{chapter_id}}?type=comic"
```
Ejemplo:

URL de capítulos:
```

https://dashboard.olympusbiblioteca.com/api/series/el-asesino-yu-ijin20250729-110824049/chapters?page=2&direction=desc&type=comic
```

El script creará automáticamente la estructura:
```
output/Nuevo_manhwa_slug/
    images/
    pdfs/
```
▶️ Ejecución
1. Instalar dependencias:
```python
pip install -r requirements.txt
```
2. Ejecutar el scrpt:
```python
python main.py
```

✅ Resultado
Al finalizar la ejecución, tendrás:
```
output/
└── Jugad20_225_reso_10000_anos_despues13424/
    ├── images/
    │   ├── 122/
    │   └── 121/
    └── pdfs/
        ├── 122.pdf
        └── 121.pdf
```
