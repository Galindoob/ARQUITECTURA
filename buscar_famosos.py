from pymongo import MongoClient  # Importa la librería para conectar con MongoDB desde Python

# Establece la conexión con MongoDB local
cliente = MongoClient("mongodb://localhost:27017")  # Se conecta al servidor local en el puerto por defecto
db = cliente["almacenamiento"]                      # Selecciona o crea la base de datos llamada 'almacenamiento'
coleccion = db["fnac_famosos_norm"]                 # Selecciona o crea la colección que contiene los famosos normalizados

# Función para buscar famosos por nombre
def buscar_por_nombre():
    # Solicita el nombre del famoso al usuario
    nombre = input("🔍 Ingrese el nombre del famoso a buscar: ").strip().lower()
    resultados = coleccion.find()  # Recupera todos los registros de la colección
    # Filtra los registros que contengan el nombre (ignora mayúsculas y espacios)
    encontrados = [r['registro'] for r in resultados if nombre in r['registro'].lower()]

    if encontrados:
        print("\n✅ Resultados encontrados:")
        for r in encontrados:
            print(f" - {r}")  # Imprime cada registro encontrado
    else:
        print("❌ No se encontró ningún famoso con ese nombre.")  # Si no hay coincidencias

# Función para buscar famosos por año de nacimiento
def buscar_por_anio():
    anio = input("📅 Ingrese el año de nacimiento a buscar (ej: 1564): ").strip()
    resultados = coleccion.find()  # Consulta todos los registros
    # Busca coincidencias que contengan el año en el campo 'registro'
    encontrados = [r['registro'] for r in resultados if f"/{anio}" in r['registro'] or anio in r['registro'].split("/")[-1]]

    if encontrados:
        print("\n✅ Famosos nacidos en ese año:")
        for r in encontrados:
            print(f" - {r}")  # Muestra los registros encontrados
    else:
        print("❌ No se encontró ningún famoso para ese año.")  # Mensaje si no hay resultados

# Menú principal
print("=== BUSCADOR DE FAMOSOS ===")  # Título del programa
print("1. Buscar por nombre")
print("2. Buscar por año")
opcion = input("Seleccione una opción (1 o 2): ")  # Pide al usuario que elija una opción

# Según la opción seleccionada, ejecuta la función correspondiente
if opcion == "1":
    buscar_por_nombre()
elif opcion == "2":
    buscar_por_anio()
else:
    print("❌ Opción inválida.")  # Mensaje si el usuario ingresa algo incorrecto
