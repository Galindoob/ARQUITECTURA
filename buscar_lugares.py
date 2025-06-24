from pymongo import MongoClient  # Importa la librería necesaria para conectar con MongoDB

# Conexión a MongoDB local
cliente = MongoClient("mongodb://localhost:27017")  # Establece conexión con el servidor local de MongoDB
db = cliente["almacenamiento"]                      # Selecciona (o crea si no existe) la base de datos 'almacenamiento'
coleccion = db["lugares"]                           # Selecciona (o crea) la colección 'lugares'

# Función para buscar un lugar por su nombre
def buscar_lugar():
    # Solicita al usuario el nombre del lugar a buscar
    nombre = input("🏛️ Ingrese el nombre del lugar a buscar: ").strip().lower()
    
    resultados = coleccion.find()  # Recupera todos los registros de la colección
    
    # Filtra aquellos cuyo campo 'nombre_lugar' contenga el texto ingresado (sin distinguir mayúsculas)
    encontrados = [r['nombre_lugar'] for r in resultados if nombre in r['nombre_lugar'].lower()]

    # Imprime los resultados encontrados o indica si no se encontraron coincidencias
    if encontrados:
        print("\n✅ Lugares encontrados:")
        for lugar in encontrados:
            print(f" - {lugar}")
    else:
        print("❌ No se encontró ningún lugar con ese nombre.")

# Llama a la función de búsqueda
buscar_lugar()
