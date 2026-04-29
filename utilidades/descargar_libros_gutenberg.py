import requests
import os
import time
from pathlib import Path

# Configuración
OUTPUT_DIR = Path(r"c:\Users\wwwed\OneDrive - Escuela Politécnica Nacional\Escritorio\EPN\SEPTIMO SEMESTRE\RI\ir26a\data")
TARGET_COUNT = 1000
CURRENT_COUNT = len(list(OUTPUT_DIR.glob("*.txt")))
BOOKS_TO_DOWNLOAD = TARGET_COUNT - CURRENT_COUNT

print(f"Libros actuales: {CURRENT_COUNT}")
print(f"Libros a descargar: {BOOKS_TO_DOWNLOAD}")

# Crear directorio si no existe
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

downloaded = 0
failed = 0
skipped = 0

def download_book(book_id, retries=3):
    """Descarga un libro de Project Gutenberg por ID con reintentos"""
    global downloaded, failed, skipped
    
    file_path = OUTPUT_DIR / f"pg{book_id}.txt"
    
    # Si ya existe, saltar
    if file_path.exists():
        skipped += 1
        return True
    
    for attempt in range(retries):
        try:
            url = f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt"
            response = requests.get(url, timeout=15)
            
            if response.status_code == 200 and len(response.text) > 100:
                with open(file_path, 'w', encoding='utf-8', errors='ignore') as f:
                    f.write(response.text)
                downloaded += 1
                return True
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2)  # Esperar antes de reintentar
            continue
    
    failed += 1
    return False

# Estrategia: descargar libros por rango de IDs
# Los IDs más bajos tienden a ser más disponibles
print(f"\nDescargando libros del catálogo de Project Gutenberg...")
print("Esto puede tomar varias horas. Por favor espera...\n")

book_id = 1
attempts = 0
max_attempts = 15000  # Intenta hasta el ID 15000 para conseguir 1000 libros

while downloaded < BOOKS_TO_DOWNLOAD and book_id < max_attempts:
    if book_id % 100 == 0:
        print(f"Intentando libro {book_id}... [Descargados: {downloaded}, Saltados: {skipped}, Fallidos: {failed}]")
    
    download_book(book_id)
    book_id += 1
    
    # Pequeño delay para no sobrecargar
    if book_id % 10 == 0:
        time.sleep(0.2)

print(f"\n{'='*60}")
print(f"✓ Descargados: {downloaded}")
print(f"⊘ Saltados (ya existían): {skipped}")
print(f"✗ Fallidos: {failed}")
print(f"Total de libros ahora: {len(list(OUTPUT_DIR.glob('*.txt')))}")
print(f"{'='*60}")

if len(list(OUTPUT_DIR.glob('*.txt'))) >= TARGET_COUNT:
    print(f"\n✓ ¡Meta alcanzada! Renombrando libros...")
    time.sleep(1)
    os.system("python rename_gutenberg_titles.py")
