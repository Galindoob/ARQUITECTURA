from pymongo import MongoClient  # Importa la librería para conectarse con MongoDB

# Conexión a la base de datos local de MongoDB
cliente = MongoClient("mongodb://localhost:27017")  # Se conecta al servidor MongoDB en localhost y puerto 27017
db = cliente["almacenamiento"]                      # Selecciona o crea la base de datos llamada 'almacenamiento'

print("\n=== BUSCADOR GENERAL ===")  # Título inicial en consola

# Ciclo principal del menú
while True:
    # Menú de opciones para el usuario
    print("\n1. Buscar famoso por nombre")
    print("2. Buscar famoso por año de nacimiento")
    print("3. Buscar lugar por nombre")
    print("4. Buscar ciudad por nombre")
    print("0. Salir")

    # Entrada de la opción seleccionada por el usuario
    opcion = input("Seleccione una opción: ")

    # --- Opción 1: Buscar famoso por nombre ---
    if opcion == "1":
        nombre = input("🔍 Ingrese el nombre del famoso: ").strip().lower()  # Solicita el nombre y lo limpia
        resultados = db["fnac_famosos_norm"].find()                          # Obtiene todos los registros de la colección
        # Filtra los registros que contienen el nombre buscado
        encontrados = [r['registro'] for r in resultados if 'registro' in r and nombre in r['registro'].lower()]
        if encontrados:
            print("\n🎯 Resultados encontrados:")
            for r in encontrados:
                print(f"• {r}")  # Muestra cada resultado encontrado
        else:
            print("❌ No se encontraron coincidencias.")  # Si no encuentra, lo indica

    # --- Opción 2: Buscar famoso por año ---
    elif opcion == "2":
        anio = input("📅 Ingrese el año de nacimiento a buscar (ej: 1564): ").strip()
        resultados = db["fnac_famosos_norm"].find()  # Consulta todos los registros
        # Busca si el año está presente en la fecha (normal o en formato a.C./d.C.)
        encontrados = [r['registro'] for r in resultados if 'registro' in r and 
                       (f"/{anio}" in r['registro'] or f"{anio} a.C." in r['registro'] or f"{anio} d.C." in r['registro'])]
        if encontrados:
            print("\n📆 Resultados encontrados:")
            for r in encontrados:
                print(f"• {r}")
        else:
            print("❌ No se encontraron coincidencias.")

    # --- Opción 3: Buscar lugar por nombre ---
    elif opcion == "3":
        lugar = input("🏛️ Ingrese el nombre del lugar a buscar: ").strip().lower()
        resultados = db["lugares"].find()  # Consulta en la colección 'lugares'
        # Filtra los lugares cuyo nombre contenga el texto ingresado
        encontrados = [r["nombre_lugar"] for r in resultados if "nombre_lugar" in r and lugar in r["nombre_lugar"].lower()]
        if encontrados:
            print("\n📍 Lugares encontrados:")
            for nombre in encontrados:
                print(f"• {nombre}")
        else:
            print("❌ No se encontraron coincidencias.")

    # --- Opción 4: Buscar ciudad por nombre ---
    elif opcion == "4":
        ciudad = input("🌆 Ingrese el nombre de la ciudad a buscar: ").strip().lower()
        resultados = db["ciudades_norm"].find()  # Consulta en la colección 'ciudades_norm'
        # Filtra las ciudades que coincidan parcial o totalmente
        encontrados = [r["ciudad"] for r in resultados if "ciudad" in r and ciudad in r["ciudad"].lower()]
        if encontrados:
            print("\n🏙️ Ciudades encontradas:")
            for nombre in encontrados:
                print(f"• {nombre}")
        else:
            print("❌ No se encontraron coincidencias.")

    # --- Opción 0: Salir del programa ---
    elif opcion == "0":
        print("👋 Saliendo del buscador...")
        break  # Sale del ciclo while

    # --- Cualquier otra opción ---
    else:
        print("❌ Opción no válida. Intente nuevamente.")  # Valida si la opción ingresada no es válida
