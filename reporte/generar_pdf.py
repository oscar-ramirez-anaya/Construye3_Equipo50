import io
import os
import re
import subprocess

from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
AQUI = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(AQUI, "..", "Construye3_Equipo50.pdf")
PIE = "Construye 3 · Equipo 50 · IA5004.10"
# títulos en el mismo orden que los marcadores {P1}..{Pn} del índice
TITULOS = [
    "1. Diseño del paquete de contexto", "1.1 Presupuesto de mesa por procedencia", "1.2 Reglas de selección y compresión",
    "1.3 Aislamiento de datos e instrucciones", "1.4 Vigencia y cita por fuente", "1.5 Aplicación a las dos consultas centrales del caso",
    "2. Política de memoria", "2.1 Qué escribe cada almacén", "2.2 Política de olvido y confidencialidad",
    "3. Catálogo de herramientas, versión 2", "3.1 Contratos de herramienta", "3.2 La acción de mayor consecuencia y su protección",
    "4. Errores, reintentos y escalamiento", "4.1 Repertorio de respuestas al error", "4.2 Política de silla vacía", "4.3 Dos casos obligatorios",
    "5. Evidencia de ejecución", "5.1 Modalidad, parámetros y las tres corridas del equipo",
    "Registro 1 — contexto, episodio guardado y borrador", "Registro 2 — memoria recuperada, duplicado y conflicto",
    "Registro 3 — caso adversarial y exclusión del portal", "Registro 4 — reintentos y silla vacía",
    "5.2 Propuesta de Luna: qué verificamos", "5.3 Lo que el simulador no comprueba",
    "Autoevaluación contra la rúbrica", "Apéndice A. Contribución del equipo", "Apéndice B. Declaración de uso de IA",
    "Glosario", "Referencias", "Comprobaciones finales del notebook",
]


def plano(texto):
    return re.sub(r"\s+", "", texto)


def render(html, pdf):
    ruta = os.path.join(AQUI, "_tmp.html")
    open(ruta, "w", encoding="utf-8").write(html)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf}", f"file://{ruta}"], check=True, capture_output=True)
    os.remove(ruta)


def paginas(pdf):
    textos = [plano(p.extract_text()) for p in PdfReader(pdf).pages]
    # portada (1) e índice (2) se ignoran: en el índice aparecen todos los títulos
    return [next(i + 1 for i, x in enumerate(textos) if i >= 2 and plano(t) in x) for t in TITULOS]


plantilla = open(os.path.join(AQUI, "reporte_tpl.html"), encoding="utf-8").read()
tmp = os.path.join(AQUI, "_tmp.pdf")
html = plantilla
for _ in range(2):
    render(html, tmp)
    nums = paginas(tmp)
    html = plantilla
    for i, n in sorted(enumerate(nums, 1), reverse=True):
        html = html.replace("{P%d}" % i, str(n))
render(html, tmp)
print("páginas por sección:", paginas(tmp))

lector = PdfReader(tmp)
total = len(lector.pages)
escritor = PdfWriter()
for i, pagina in enumerate(lector.pages, 1):
    if i > 1:
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=letter)
        c.setStrokeColorRGB(0.78, 0.8, 0.84)
        c.setLineWidth(0.6)
        c.line(54, 40, letter[0] - 54, 40)
        c.setFont("Times-Roman", 8.5)
        c.setFillColorRGB(0.4, 0.4, 0.4)
        c.drawString(54, 28, PIE)
        c.drawRightString(letter[0] - 54, 28, f"Página {i} de {total}")
        c.save()
        buf.seek(0)
        pagina.merge_page(PdfReader(buf).pages[0])
    escritor.add_page(pagina)
escritor.add_metadata({"/Title": "Construye3_Equipo50", "/Author": "Equipo 50",
                       "/Producer": "", "/Creator": ""})
with open(SALIDA, "wb") as f:
    escritor.write(f)
os.remove(tmp)
print("total", total)
