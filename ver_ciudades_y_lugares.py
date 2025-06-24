from pymongo import MongoClient  # Importa la librería necesaria para conectarse y trabajar con MongoDB

# Conexión a MongoDB local
cliente = MongoClient("mongodb://localhost:27017")  # Se conecta al servidor MongoDB en localhost
db = cliente["almacenamiento"]                      # Selecciona la base de datos llamada 'almacenamiento'

# Mostrar ciudades almacenadas en la colección 'ciudades_norm'
print("📍 CIUDADES GUARDADAS:")                      # Título informativo para mostrar las ciudades
ciudades = db["ciudades_norm"].find()               # Obtiene todos los documentos de la colección 'ciudades_norm'
for ciudad in ciudades:
    print("•", ciudad.get("ciudad", "[Sin nombre]"))  # Imprime cada ciudad, o un mensaje por defecto si no tiene campo 'ciudad'

# Mostrar lugares almacenados en la colección 'lugares'
print("\n🏛️ LUGARES GUARDADOS:")                    # Título informativo para mostrar los lugares
lugares = db["lugares"].find()                      # Obtiene todos los documentos de la colección 'lugares'
for lugar in lugares:
    print("•", lugar.get("nombre_lugar", "[Sin nombre]"))  # Imprime cada lugar, o mensaje por defecto si falta el campo
