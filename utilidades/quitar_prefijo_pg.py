from pathlib import Path
import re

DATA_DIR = Path(r"c:\Users\wwwed\OneDrive - Escuela Politécnica Nacional\Escritorio\EPN\SEPTIMO SEMESTRE\RI\ir26a\data")

print("Quitando prefijo 'pg' de los nombres de archivos...\n")

renamed = 0
skipped = 0
conflicts = 0

# Procesar todos los archivos
txt_files = sorted(DATA_DIR.glob("*.txt"))

for file_path in txt_files:
    # Buscar patrón: pg### - Título.txt
    match = re.match(r"pg\d+ - (.+\.txt)$", file_path.name)
    
    if match:
        new_name = match.group(1)
        new_path = file_path.parent / new_name
        
        # Si el archivo ya existe, añadir número
        if new_path.exists() and new_path != file_path:
            base = new_path.stem
            suffix = new_path.suffix
            idx = 2
            while True:
                candidate = file_path.parent / f"{base} ({idx}){suffix}"
                if not candidate.exists():
                    new_path = candidate
                    break
                idx += 1
            conflicts += 1
        
        file_path.rename(new_path)
        renamed += 1
        print(f"✓ {file_path.name} → {new_path.name}")
    else:
        skipped += 1

print(f"\n{'='*60}")
print(f"Renombrados: {renamed}")
print(f"Conflictos resueltos: {conflicts}")
print(f"Sin cambios: {skipped}")
print(f"{'='*60}")
