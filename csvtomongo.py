import json
from bson import ObjectId

# Lee el archivo con la tabla (usa el nombre real de tu archivo)
with open("tabla.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

data = []
id_counter = 1

for line in lines:
    line = line.strip()
    if not line or line.startswith("CODIGO"):  # Ignora líneas vacías y encabezados
        continue

    parts = line.split(",")  # separador coma
    if len(parts) < 5:
        continue

    code, product, estiba, piso, pacas = parts[:5]

    try:
        item = {
            "_id": {"$oid": str(ObjectId())},
            "id": {"$numberInt": str(id_counter)},
            "code": {"$numberInt": code.strip()},
            "product": product.strip(),
            "shelves": {"$numberInt": estiba.strip()},
            "floors": {"$numberInt": piso.strip()},
            "packs": {"$numberInt": pacas.strip()}
        }
        data.append(item)
        id_counter += 1
    except Exception as e:
        print("Error en línea:", line, e)

# Guardar en un archivo JSON
with open("output.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Se generaron {len(data)} documentos JSON correctamente.")
