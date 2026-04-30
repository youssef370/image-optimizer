#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path
from PIL import Image


from .encoders import encode_avif, encode_jpeg, encode_png, encode_webp
from .validators import validate_file, validate_paths

parser = argparse.ArgumentParser()


FORMATS = {
    "jpeg": {
        "encoder": encode_jpeg,
        "quality": 75,
    },
    "avif": {
        "encoder": encode_avif,
        "quality": 85,
    },
    "webp": {
        "encoder": encode_webp,
        "quality": 80,
    },
    "png": {
        "encoder": encode_png,
        "quality": 75,
    },
}
SUPPORTED_FORMATS = set(FORMATS.keys())

ENCODERS = {k: v["encoder"] for k, v in FORMATS.items()}

DEFAULT_QUALITIES = {k: v["quality"] for k, v in FORMATS.items()}

def convert_file(*, file_path: Path, output_format: str, quality: int):
    """Create the output directory and execute the encoding function based user's format input
    Args:
        file_path: Path of the file to convert
        format: Format to which the input file should be converted
        quality: Compression quality inputted by user, if no input then depends on the output file format
    Returns:
        str: Path to the output file
    """
    if not validate_file(file_path, SUPPORTED_FORMATS):
        return {"status": "invalid", "file": str(file_path)}

    output_dir = file_path.parent / "converted"
    output_dir.mkdir(parents=True, exist_ok=True)

    ext = output_format
    try:
        with Image.open(file_path) as img:
            output = ENCODERS[ext](img, quality, output_dir)
            return {"status": "ok", "file": output}
    except Exception:
        print("Cannot open image")
        return {"status": "failed", "file": str(file_path)}

def convert_folder_content(*, folder_path: Path, quality: int, output_format: str):
    """Converts image files within a folder.
    Args:
        folder_path: Path of the folder the content of which should be converted.
        quality: Compression quality inputted by user, if no input then depends on the output file format
    """
    for file in folder_path.iterdir():
        if file.is_file():
            status = convert_file(
                file_path=file, output_format=output_format, quality=quality
            )
            print(f"STATUS: {status['status']}, FILE: {status['file']}")

def main():
    parser.add_argument("paths", nargs="+", help="Files or directories to process")

    parser.add_argument(
        "--format",
        help="Output format",
        choices=SUPPORTED_FORMATS,
        default="webp",
    )

    parser.add_argument("--quality", type=int, help="Quality of the output file")

    args = parser.parse_args()
    paths = [Path(p) for p in args.paths]
    output_format = args.format.lower()
    if output_format == "jpg":
        output_format = "jpeg"

    quality = args.quality if args.quality else DEFAULT_QUALITIES[output_format]

    if not validate_paths(paths):
        sys.exit()

    for path in paths:
        if path.is_dir():
            convert_folder_content(
                folder_path=path, output_format=output_format, quality=quality
            )
        elif path.is_file():
            status = convert_file(
                file_path=path, output_format=output_format, quality=quality
            )
            print(f"STATUS: {status['status']}, FILE: {status['file']}")


if __name__ == "__main__":
    main()
