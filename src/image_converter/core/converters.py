from PIL import Image
from pathlib import Path

from .globals import SUPPORTED_FORMATS, ENCODERS
from .validators import validate_file
from .status import Status, StatusType


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
        return Status(StatusType.INVALID, file_path, "File invalid")

    try:
        with Image.open(file_path) as img:
            output = ENCODERS[output_format](img, quality, output_dir)
        return Status(StatusType.OK, output, "SUCCESS")
    except Exception as e:
        return Status(StatusType.FAILED, file_path, str(e))


