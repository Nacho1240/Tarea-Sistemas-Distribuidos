import json
import csv
import sys
from pathlib import Path

def inferir_tipo(valor):
    if isinstance(valor, bool):
        return 'chararray'
    elif isinstance(valor, int):
        return 'int'
    elif isinstance(valor, float):
        return 'float'
    else:
        return 'chararray'

def inferir_esquema(objeto):
    esquema = []
    for clave, valor in objeto.items():
        tipo = inferir_tipo(valor)
        esquema.append(f"{clave}:{tipo}")
    return ', '.join(esquema)

def json_array_a_csv(json_path, csv_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        datos = json.load(f)

    if not isinstance(datos, list) or not datos:
        print("❌ El JSON debe ser un array no vacío de objetos.")
        return

    # 🔍 Encontrar todas las claves presentes en cualquier objeto
    todas_las_claves = set()
    for item in datos:
        todas_las_claves.update(item.keys())
    campos = sorted(todas_las_claves)  # Orden alfabético opcional

    # 🧽 Rellenar los campos faltantes con ""
    filas_normalizadas = []
    for item in datos:
        fila = {clave: item.get(clave, "") for clave in campos}
        filas_normalizadas.append(fila)

    # 📝 Escribir CSV
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(filas_normalizadas)

    print(f"\n✅ CSV generado: {csv_path}")

    # Inferir tipos usando el primer objeto completo
    ejemplo = filas_normalizadas[0]
    esquema = inferir_esquema(ejemplo)
    pig_cmd = f"datos = LOAD '{csv_path}' USING PigStorage(',') AS ({esquema});"

    print("\n💡 Comando LOAD para Pig:\n")
    print(pig_cmd)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python json_a_csv_pig.py entrada.json salida.csv")
        sys.exit(1)

    json_path = Path(sys.argv[1])
    csv_path = Path(sys.argv[2])

    if not json_path.exists():
        print(f"❌ Archivo no encontrado: {json_path}")
        sys.exit(1)

    json_array_a_csv(json_path, csv_path)
