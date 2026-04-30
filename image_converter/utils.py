from pathlib import Path


def get_file_extension(file_path: Path) -> str:
    ext = file_path.suffix.lstrip(".").lower()
    if ext == "jpg":
        ext = "jpeg"

    return ext
