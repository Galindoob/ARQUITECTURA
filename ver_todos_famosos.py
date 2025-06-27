from pymongo import MongoClient
from datetime import datetime

# Conexión a MongoDB
cliente = MongoClient("mongodb://localhost:27017")
db = cliente["almacenamiento"]
coleccion = db["fnac_famosos_norm"]

# Función para calcular edad
def calcular_edad(fecha_str):
    try:
        nacimiento = datetime.strptime(fecha_str, "%d/%m/%Y")
        hoy = datetime.today()
        edad = hoy.year - nacimiento.year - ((hoy.month, hoy.day) < (nacimiento.month, nacimiento.day))
        return edad
    except:
        return None

# Función para verificar si es cumpleaños
def es_cumpleanios(fecha_str):
    try:
        nacimiento = datetime.strptime(fecha_str, "%d/%m/%Y")
        hoy = datetime.today()
        return nacimiento.day == hoy.day and nacimiento.month == hoy.month
    except:
        return False

# Obtener todos los registros y ordenarlos
registros = coleccion.find()
lista = sorted([r["registro"] for r in registros if "registro" in r])

# Mostrar todos los famosos con edad y 🎂 si corresponde
print("🎓 LISTA COMPLETA DE FAMOSOS REGISTRADOS\n")

for r in lista:
    partes = r.split(" - ")
    if len(partes) == 2:
        nombre, fecha = partes
        edad = calcular_edad(fecha)
        cumple = " 🎂" if es_cumpleanios(fecha) else ""
        edad_str = f" → {edad} años" if edad is not None else ""
        print(f"• {r}{edad_str}{cumple}")
    else:
        print(f"• {r}")
