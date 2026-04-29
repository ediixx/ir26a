from pathlib import Path
import re

BASE_DIR = Path(r"c:\Users\wwwed\OneDrive - Escuela Politécnica Nacional\Escritorio\EPN\SEPTIMO SEMESTRE\RI\ir26a\data\gutenberg\data")
INVALID_CHARS = r'<>:"/\\|?*'


def sanitize_filename(name: str) -> str:
    # Remove invalid Windows filename characters and collapse whitespace.
    cleaned = ''.join('_' if ch in INVALID_CHARS else ch for ch in name)
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" .")
    return cleaned[:180] if len(cleaned) > 180 else cleaned


def extract_title(file_path: Path) -> str:
    # Gutenberg metadata usually includes a line starting with "Title:".
    with file_path.open("r", encoding="utf-8", errors="ignore") as f:
        for _ in range(400):
            line = f.readline()
            if not line:
                break
            if line.startswith("Title:"):
                return line.split("Title:", 1)[1].strip()
    return ""


def unique_target(path: Path) -> Path:
    if not path.exists():
        return path

    base = path.stem
    suffix = path.suffix
    parent = path.parent
    idx = 2
    while True:
        candidate = parent / f"{base} ({idx}){suffix}"
        if not candidate.exists():
            return candidate
        idx += 1


def main() -> None:
    txt_files = sorted(BASE_DIR.glob("*.txt"))
    renamed = 0
    skipped = 0

    for file_path in txt_files:
        title = extract_title(file_path)
        if not title:
            print(f"[SKIP] No title found in: {file_path.name}")
            skipped += 1
            continue

        safe_title = sanitize_filename(title)
        if not safe_title:
            print(f"[SKIP] Empty sanitized title for: {file_path.name}")
            skipped += 1
            continue

        # Keep the original Gutenberg id prefix and append the title.
        new_name = f"{file_path.stem} - {safe_title}.txt"
        target = unique_target(file_path.with_name(new_name))

        if target.name == file_path.name:
            print(f"[OK] Already named: {file_path.name}")
            continue

        file_path.rename(target)
        renamed += 1
        print(f"[RENAME] {file_path.name} -> {target.name}")

    print(f"\nDone. Renamed: {renamed}, Skipped: {skipped}, Total: {len(txt_files)}")


if __name__ == "__main__":
    main()
