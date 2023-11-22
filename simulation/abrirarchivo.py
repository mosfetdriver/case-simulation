# Abre un archivo en modo de lectura (por defecto)
nombre_archivo = "C:/Users/karla/Sumo/misimulacion/osm.view.xml"

try:
    with open(nombre_archivo, "r") as archivo:
        contenido = archivo.read()
        print("Contenido del archivo:")
        print(contenido)
except FileNotFoundError:
    print(f"El archivo '{nombre_archivo}' no existe.")
except Exception as e:
    print(f"Ocurrió un error al abrir el archivo: {str(e)}")
