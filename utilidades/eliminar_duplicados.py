import os
import hashlib
from pathlib import Path
from collections import defaultdict

# Configuración
DATA_DIR = Path(r"c:\Users\wwwed\OneDrive - Escuela Politécnica Nacional\Escritorio\EPN\SEPTIMO SEMESTRE\RI\ir26a\data")

def get_file_hash(filepath):
    """Calcula SHA256 de un archivo"""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        print(f"Error leyendo {filepath}: {e}")
        return None

print("Analizando libros para encontrar duplicados...")
print(f"Carpeta: {DATA_DIR}\n")

# Obtener todos los archivos txt
txt_files = list(DATA_DIR.glob("*.txt"))
print(f"Total de archivos: {len(txt_files)}\n")

# Mapeo hash -> lista de archivos
hash_map = defaultdict(list)
duplicates_found = 0
files_to_delete = []

for file_path in txt_files:
    file_hash = get_file_hash(file_path)
    if file_hash:
        hash_map[file_hash].append(file_path)

# Encontrar duplicados
print("Duplicados encontrados:\n")
for file_hash, files in hash_map.items():
    if len(files) > 1:
        duplicates_found += 1
        print(f"[DUPLICADO #{duplicates_found}] {len(files)} copias:")
        for i, f in enumerate(files):
            print(f"  {i+1}. {f.name} ({f.stat().st_size / 1024:.0f} KB)")
        
        # Mantener el primer archivo, eliminar el resto
        for f in files[1:]:
            files_to_delete.append(f)
        print()

print(f"\n{'='*60}")
print(f"Total de duplicados encontrados: {duplicates_found}")
print(f"Archivos a eliminar: {len(files_to_delete)}")
print(f"{'='*60}\n")

if files_to_delete:
    print("Eliminando archivos duplicados...\n")
    for file_path in files_to_delete:
        try:
            file_path.unlink()
            print(f"✓ Eliminado: {file_path.name}")
        except Exception as e:
            print(f"✗ Error eliminando {file_path.name}: {e}")
    
    remaining = len(list(DATA_DIR.glob("*.txt")))
    print(f"\n✓ Duplicados eliminados. Libros restantes: {remaining}")
else:
    print("✓ No se encontraron duplicados.")

print(f"\nTotal de libros únicos ahora: {len(list(DATA_DIR.glob('*.txt')))}")
