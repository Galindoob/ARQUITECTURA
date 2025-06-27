from pymongo import MongoClient

# Conexión a MongoDB
cliente = MongoClient("mongodb://localhost:27017")
db = cliente["almacenamiento"]

# Mostrar ciudades
print("📍 CIUDADES GUARDADAS:")
ciudades = db["ciudades_norm"].find()
lista_ciudades = sorted([c.get("ciudad", "[Sin nombre]") for c in ciudades])
for ciudad in lista_ciudades:
    print(f"• {ciudad}")

# Mostrar lugares
print("\n🏛️ LUGARES GUARDADOS:")
lugares = db["lugares"].find()
lista_lugares = sorted([l.get("nombre_lugar", "[Sin nombre]") for l in lugares])
for lugar in lista_lugares:
    print(f"• {lugar}")
