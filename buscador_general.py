from pymongo import MongoClient
from datetime import datetime

# Conexión a MongoDB
cliente = MongoClient("mongodb://localhost:27017")
db = cliente["almacenamiento"]

# Función para calcular edad desde una fecha válida
def calcular_edad(fecha_str):
    try:
        nacimiento = datetime.strptime(fecha_str, "%d/%m/%Y")
        hoy = datetime.today()
        edad = hoy.year - nacimiento.year - ((hoy.month, hoy.day) < (nacimiento.month, nacimiento.day))
        return edad
    except:
        return None

# Función para verificar si hoy es cumpleaños
def es_cumpleanios(fecha_str):
    try:
        nacimiento = datetime.strptime(fecha_str, "%d/%m/%Y")
        hoy = datetime.today()
        return nacimiento.day == hoy.day and nacimiento.month == hoy.month
    except:
        return False

print("\n=== BUSCADOR GENERAL ===")

while True:
    print("\n1. Buscar famoso por nombre")
    print("2. Buscar famoso por año de nacimiento")
    print("3. Buscar lugar por nombre")
    print("4. Buscar ciudad por nombre")
    print("5. Ver todos los famosos")
    print("0. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        nombre = input("🔍 Ingrese el nombre del famoso: ").strip().lower()
        resultados = db["fnac_famosos_norm"].find()
        encontrados = sorted(
            [r['registro'] for r in resultados if 'registro' in r and nombre in r['registro'].lower()]
        )
        if encontrados:
            print("\n🎯 Resultados encontrados:")
            for r in encontrados:
                partes = r.split(" - ")
                if len(partes) == 2:
                    nombre, fecha = partes
                    edad = calcular_edad(fecha)
                    cumple = " 🎂" if es_cumpleanios(fecha) else ""
                    edad_str = f" → {edad} años" if edad is not None else ""
                    print(f"• {r}{edad_str}{cumple}")
                else:
                    print(f"• {r}")
        else:
            print("❌ No se encontraron coincidencias.")

    elif opcion == "2":
        anio = input("📅 Ingrese el año de nacimiento a buscar (ej: 1564): ").strip()
        resultados = db["fnac_famosos_norm"].find()
        encontrados = sorted(
            [r['registro'] for r in resultados if 'registro' in r and (
                f"/{anio}" in r['registro'] or f"{anio} a.C." in r['registro'] or f"{anio} d.C." in r['registro']
            )]
        )
        if encontrados:
            print("\n📆 Resultados encontrados:")
            for r in encontrados:
                partes = r.split(" - ")
                if len(partes) == 2:
                    nombre, fecha = partes
                    edad = calcular_edad(fecha)
                    cumple = " 🎂" if es_cumpleanios(fecha) else ""
                    edad_str = f" → {edad} años" if edad is not None else ""
                    print(f"• {r}{edad_str}{cumple}")
                else:
                    print(f"• {r}")
        else:
            print("❌ No se encontraron coincidencias.")

    elif opcion == "3":
        lugar = input("🏛️ Ingrese el nombre del lugar a buscar: ").strip().lower()
        resultados = db["lugares"].find()
        encontrados = sorted([
            r["nombre_lugar"] for r in resultados
            if "nombre_lugar" in r and lugar in r["nombre_lugar"].lower()
        ])
        if encontrados:
            print("\n📍 Lugares encontrados:")
            for nombre in encontrados:
                print(f"• {nombre}")
        else:
            print("❌ No se encontraron coincidencias.")

    elif opcion == "4":
        ciudad = input("🌆 Ingrese el nombre de la ciudad a buscar: ").strip().lower()
        resultados = db["ciudades_norm"].find()
        encontrados = sorted([
            r["ciudad"] for r in resultados
            if "ciudad" in r and ciudad in r["ciudad"].lower()
        ])
        if encontrados:
            print("\n🏙️ Ciudades encontradas:")
            for nombre in encontrados:
                print(f"• {nombre}")
        else:
            print("❌ No se encontraron coincidencias.")

    elif opcion == "5":
        print("\n🎓 Famosos registrados:\n")
        registros = db["fnac_famosos_norm"].find()
        lista = sorted([r["registro"] for r in registros if "registro" in r])

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

    elif opcion == "0":
        print("👋 Saliendo del buscador...")
        break
    else:
        print("❌ Opción no válida. Intente nuevamente.")
