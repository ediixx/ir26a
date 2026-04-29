from pathlib import Path

DATA_DIR = Path(r"c:\Users\wwwed\OneDrive - Escuela Politécnica Nacional\Escritorio\EPN\SEPTIMO SEMESTRE\RI\ir26a\data")

print("Acortando títulos muy largos...\n")

max_title_length = 100  # Máximo de caracteres para el título
renamed = 0

for file_path in DATA_DIR.glob("*.txt"):
    stem = file_path.stem
    
    # Si el título es muy largo, acortarlo
    if len(stem) > max_title_length:
        new_stem = stem[:max_title_length].rstrip()
        new_name = f"{new_stem}.txt"
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
        print(f"✓ Acortado:")
        print(f"  De: {file_path.name}")
        print(f"  A:  {new_path.name}\n")

print(f"{'='*70}")
print(f"Total de archivos acortados: {renamed}")
print(f"{'='*70}")
