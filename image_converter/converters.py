from PIL import Image
from pathlib import Path

from .globals import SUPPORTED_FORMATS, ENCODERS
from .validators import validate_file
from .cache import add_to_cache, compute_hash_key

import json


def convert_file(
    *, file_path: Path, output_format: str, quality: int, output_dir: Path | None
):
    """Create the output directory and execute the encoding function based user's format input
    Args:
        file_path: Path of the file to convert
        format: Format to which the input file should be converted
        quality: Compression quality inputted by user, if no input then depends on the output file format
        output_dir (optional): Destination directory where output file will be stored
    Returns:
        dict: Operation status and path to output file
    """
    if not validate_file(file_path, SUPPORTED_FORMATS):
        return {"status": "invalid", "file": str(file_path)}

    if not output_dir:
        output_dir = file_path.parent / "converted"

    with open("image-converter-cache.json", "r") as f:
        cache_file = json.load(f)

    hashkey = compute_hash_key(
        file_path=file_path, quality=quality, output_format=output_format
    )
    if hashkey in cache_file.keys():
        return {"status": "cached", "file": str(file_path)}

    output_dir.mkdir(parents=True, exist_ok=True)

    ext = output_format
    try:
        with Image.open(file_path) as img:
            output = ENCODERS[ext](img, quality, output_dir)
            add_to_cache(
                hashkey=hashkey,
                input_file_path=file_path,
                output_file_path=output,
                output_format=output_format,
                quality=quality,
            )
            return {"status": "ok", "file": output}
    except Exception:
        return {"status": "failed", "file": str(file_path)}


def convert_folder_content(
    *,
    folder_path: Path,
    quality: int,
    output_format: str,
    output_dir: Path,
    recursive: bool = False,
):
    """Converts image files within a folder.
    Args:
        folder_path: Path of the folder the content of which should be converted.
        quality: Compression quality inputted by user, if no input then depends on the output file format
    """

    files = folder_path.rglob("*") if recursive else folder_path.iterdir()
    for file in files:
        if not file.is_file():
            continue

        relative_path = file.relative_to(folder_path)
        target_dir = output_dir / relative_path.parent
        target_dir.mkdir(parents=True, exist_ok=True)

        status = convert_file(
            file_path=file,
            output_format=output_format,
            quality=quality,
            output_dir=target_dir,
        )
        print(f"STATUS: {status['status']}, FILE: {status['file']}")
