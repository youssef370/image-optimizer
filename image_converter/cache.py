import hashlib
import json
from pathlib import Path


def compute_hash_key(file_path: Path, output_format: str, quality: int):
    stat = file_path.stat()

    key_string = "|".join(
        [
            str(file_path.resolve()),
            str(stat.st_mtime),
            str(stat.st_size),
            output_format,
            str(quality),
        ]
    )

    return hashlib.sha256(key_string.encode()).hexdigest()

def add_to_cache(
    hashkey: str,
    input_file_path: Path,
    output_file_path: Path,
    quality: int,
    output_format: str,
):

    with open(".image-converter-cache.json", "r") as f:
        cache = json.load(f)

    new_cache_entry = {
        hashkey: {
            "input": str(input_file_path.resolve()),
            "output": str(output_file_path.resolve()),
            "quality": str(quality),
            "format": output_format,
            "mtime": output_file_path.stat().st_mtime,
        }
    }

    with open(".image-converter-cache.json", "w") as f:
        json.dump(new_cache_entry, cache, indent=4)

def load_cache():
    ...

def save_cache():
    ...

def create_cache():
    ...
