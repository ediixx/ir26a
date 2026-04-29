import hashlib
from pathlib import Path
from collections import defaultdict
import requests
import time

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

print("="*70)
print("PASO 1: BUSCANDO DUPLICADOS")
print("="*70)

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

print(f"{'='*70}")
print(f"Total de duplicados encontrados: {duplicates_found}")
print(f"Archivos a eliminar: {len(files_to_delete)}")
print(f"{'='*70}\n")

# Eliminar duplicados
if files_to_delete:
    print("Eliminando archivos duplicados...\n")
    for file_path in files_to_delete:
        try:
            file_path.unlink()
            print(f"✓ Eliminado: {file_path.name}")
        except Exception as e:
            print(f"✗ Error eliminando {file_path.name}: {e}")
    
    current_count = len(list(DATA_DIR.glob("*.txt")))
    print(f"\n✓ Duplicados eliminados. Libros restantes: {current_count}\n")
else:
    print("✓ No se encontraron duplicados.\n")
    current_count = len(list(DATA_DIR.glob("*.txt")))

print("="*70)
print("PASO 2: DESCARGANDO LIBROS PARA COMPLETAR A 1000")
print("="*70)

TARGET_COUNT = 1000
BOOKS_TO_DOWNLOAD = TARGET_COUNT - current_count

if BOOKS_TO_DOWNLOAD <= 0:
    print(f"✓ Ya tienes {current_count} libros. ¡Meta alcanzada!")
else:
    print(f"Necesito descargar {BOOKS_TO_DOWNLOAD} libros más\n")
    
    downloaded = 0
    failed = 0
    
    # Obtener IDs que ya existen
    existing_ids = set()
    for f in DATA_DIR.glob("*.txt"):
        # Extraer ID del nombre si empieza con número
        parts = f.stem.split()
        if parts and parts[0].isdigit():
            existing_ids.add(int(parts[0]))
    
    print(f"IDs ya descargados: {len(existing_ids)}")
    print("Buscando libros nuevos...\n")
    
    # Descargar nuevos
    book_id = 1
    attempts = 0
    max_attempts = 20000
    
    while downloaded < BOOKS_TO_DOWNLOAD and book_id < max_attempts:
        if book_id not in existing_ids:
            try:
                url = f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt"
                response = requests.get(url, timeout=15)
                
                if response.status_code == 200 and len(response.text) > 100:
                    file_path = DATA_DIR / f"{book_id} - libro.txt"
                    with open(file_path, 'w', encoding='utf-8', errors='ignore') as f:
                        f.write(response.text)
                    downloaded += 1
                    existing_ids.add(book_id)
                    
                    if downloaded % 10 == 0:
                        print(f"Descargados: {downloaded}/{BOOKS_TO_DOWNLOAD}")
            except Exception as e:
                failed += 1
                pass
        
        book_id += 1
        
        if book_id % 20 == 0:
            time.sleep(0.2)
    
    print(f"\n✓ Descargados: {downloaded}")
    print(f"✗ Fallidos: {failed}")
    current_count = len(list(DATA_DIR.glob("*.txt")))
    print(f"Total de libros ahora: {current_count}\n")

print("="*70)
print("PASO 3: ELIMINANDO PREFIJOS DE ARCHIVOS NUEVOS")
print("="*70 + "\n")

# Procesar archivos con patrón "### - libro.txt"
import re

renamed = 0
for file_path in DATA_DIR.glob("*-*.txt"):
    # Buscar patrón: ### - libro.txt
    match = re.match(r"^\d+ - libro\.txt$", file_path.name)
    
    if match:
        # Este es un archivo nuevo que no tiene título
        # Intentar obtener el título del contenido
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for _ in range(400):
                    line = f.readline()
                    if not line:
                        break
                    if line.startswith("Title:"):
                        title = line.split("Title:", 1)[1].strip()
                        # Sanitizar el título
                        title = re.sub(r'[<>:"/\\|?*]', '_', title)
                        title = re.sub(r'\s+', ' ', title).strip(' .')
                        title = title[:180] if len(title) > 180 else title
                        
                        new_name = f"{title}.txt"
                        new_path = file_path.parent / new_name
                        
                        # Si existe, agregar número
                        if new_path.exists():
                            base = new_path.stem
                            idx = 2
                            while True:
                                candidate = file_path.parent / f"{base} ({idx}).txt"
                                if not candidate.exists():
                                    new_path = candidate
                                    break
                                idx += 1
                        
                        file_path.rename(new_path)
                        renamed += 1
                        print(f"✓ {file_path.name} → {new_path.name}")
                        break
        except:
            pass

print(f"\nArchivos renombrados: {renamed}")
print(f"\n{'='*70}")
print(f"FINAL: {len(list(DATA_DIR.glob('*.txt')))} libros totales")
print(f"{'='*70}")
