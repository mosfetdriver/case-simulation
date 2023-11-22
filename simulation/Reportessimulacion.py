from nbconvert import PDFExporter
import nbformat

# Ruta al archivo .ipynb que deseas convertir
input_notebook = "C:\Users\karla.ipynb"

# Ruta de salida para el archivo PDF
output_pdf = "C:\Users\karla.pdf"

# Cargar el cuaderno .ipynb
with open(input_notebook, 'r', encoding='utf-8') as notebook_file:
    notebook_content = nbformat.read(notebook_file, as_version=4)

# Configurar el exportador PDF
pdf_exporter = PDFExporter()

# Realizar la conversión
(pdf, resources) = pdf_exporter.from_notebook_node(notebook_content)

# Guardar el archivo PDF
with open(output_pdf, 'wb') as pdf_file:
    pdf_file.write(pdf)
