import re                                # Módulo para trabajar con expresiones regulares (extracción de datos del texto)
from datetime import datetime            # Para manejar fechas y convertirlas a un formato estándar
from pymongo import MongoClient          # Cliente de MongoDB para conectar e insertar datos en la base

# Conexión a la base de datos local de MongoDB
cliente = MongoClient('mongodb://localhost:27017')   # Dirección por defecto de un servidor local de MongoDB
db = cliente['almacenamiento']                       # Se accede (o crea si no existe) la base de datos llamada "almacenamiento"
coleccion = db['fnac_famosos_norm']                  # Se accede (o crea) la colección para guardar los registros normalizados

# Ruta del archivo que contiene los datos a procesar
archivo = "DATOS2.txt"

# Función para intentar convertir fechas comunes al formato chileno estándar DD/MM/AAAA
def normalizar_fecha(fecha_str):
    formatos = [                                      # Lista de posibles formatos que puede tener la fecha en el archivo
        "%Y/%m/%d", "%Y-%m-%d",                       # Año-Mes-Día con slash o guión
        "%d/%m/%Y", "%d-%m-%Y",                       # Día-Mes-Año con slash o guión
        "%d/%m/%y", "%d-%m-%y"                        # Día-Mes-Año corto (2 dígitos)
    ]
    for fmt in formatos:
        try:
            fecha = datetime.strptime(fecha_str, fmt)           # Intenta convertir la fecha al formato actual del bucle
            return fecha.strftime("%d/%m/%Y")                   # Si tiene éxito, la devuelve en formato chileno
        except ValueError:
            continue                                            # Si falla, prueba el siguiente formato
    return None                                                 # Si ningún formato funcionó, retorna None

# Abrir el archivo de texto y leer todas las líneas
with open(archivo, "r", encoding="utf-8") as file:
    lineas = file.readlines()

# Procesar cada línea del archivo
for linea in lineas:
    # Usar expresión regular para separar el nombre del personaje y su fecha
    match = re.match(r"\d+\.\s*(.+?)\s*-\s*(.+)", linea.strip())
    if match:
        nombre = match.group(1).strip()             # Extraer y limpiar el nombre del personaje
        fecha_raw = match.group(2).strip()          # Extraer y limpiar la fecha original

        print(f"\n🟢 Nombre: {nombre} | Fecha original: {fecha_raw}")

        # Intentar normalizar la fecha
        fecha_normalizada = normalizar_fecha(fecha_raw)

        if fecha_normalizada:
            registro = f"{nombre} - {fecha_normalizada}"  # Formato final para insertar
            if not coleccion.find_one({'registro': registro}):  # Verifica si ya existe el mismo registro
                coleccion.insert_one({'registro': registro})     # Inserta si no existe
                print(f"✅ Insertado en MongoDB: {registro}")
            else:
                print(f"⚠️ Ya existe en MongoDB: {registro}")
        else:
            # Si no se pudo normalizar, tratar de extraer el año manualmente
            anio = "????"                       # Año por defecto si no se puede detectar
            sufijo = ""                        # Para guardar "a.C." o "d.C." si se detecta

            # Intentar encontrar un número de 2 a 4 cifras (ej: 69, 1028)
            anio_match = re.search(r"(\d{2,4})", fecha_raw)
            if anio_match:
                anio = anio_match.group(1)

            # Revisar si la fecha contiene algún indicio de a.C. o d.C.
            if 'a.C.' in fecha_raw or 'ac' in fecha_raw.lower():
                sufijo = " a.C."                # Si detecta era antigua
            elif 'd.C.' in fecha_raw or 'dc' in fecha_raw.lower():
                sufijo = " d.C."                # Si detecta era después de Cristo

            # Crear una fecha ficticia "00/00/AAAA" con sufijo si aplica
            fecha_final = f"00/00/{anio}{sufijo}"
            registro = f"{nombre} - {fecha_final}"

            # Insertar si no existe
            if not coleccion.find_one({'registro': registro}):
                coleccion.insert_one({'registro': registro})
                print(f"⚠️ Fecha estimada usada: {fecha_final}")
                print(f"✅ Insertado en MongoDB: {registro}")
            else:
                print(f"⚠️ Ya existe en MongoDB: {registro}")
    else:
        # Si no se logró extraer nombre y fecha, mostrar advertencia
        print(f"❌ Línea no reconocida: {linea.strip()}")

