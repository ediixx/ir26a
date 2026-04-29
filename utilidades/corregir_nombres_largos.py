from pathlib import Path
import re

DATA_DIR = Path(r"c:\Users\wwwed\OneDrive - Escuela Politécnica Nacional\Escritorio\EPN\SEPTIMO SEMESTRE\RI\ir26a\data")

print("Buscando archivos con nombres muy largos...\n")

max_length = 200  # Git tiene problemas con nombres muy largos
renamed = 0

for file_path in DATA_DIR.glob("*.txt"):
    if len(file_path.name) > max_length:
        # Acortar el nombre
        stem = file_path.stem[:max_length - 4]  # Dejar espacio para .txt
        new_name = f"{stem}.txt"
        new_path = file_path.parent / new_name
        
        # Si ya existe, agregar número
        if new_path.exists():
            base = new_path.stem
            idx = 2
            while True:
                candidate = file_path.parent / f"{base}_{idx}.txt"
                if not candidate.exists():
                    new_path = candidate
                    break
                idx += 1
        
        file_path.rename(new_path)
        renamed += 1
        print(f"✓ Acortado: {file_path.name[:50]}...")
        print(f"  → {new_path.name[:50]}...\n")

print(f"Total de archivos acortados: {renamed}")

# Verificar que no hay más archivos muy largos
problematic = [f for f in DATA_DIR.glob("*.txt") if len(f.name) > max_length]
if problematic:
    print(f"⚠️ Aún hay {len(problematic)} archivos muy largos")
else:
    print("✓ Todos los nombres están dentro del límite")
