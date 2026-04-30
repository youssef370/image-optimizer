from pathlib import Path


def validate_file(file_path: Path, supported_formats):
    """Checks if input file is one of the supported types
    Args:
        file_path: Path to the file to check
    Returns:
        bool: true if the file is supported, otherwise false
    """

    ext = file_path.suffix.lstrip(".").lower()
    if ext not in supported_formats:
        print(
            f"File type not supported. Should be in one of the following formats: {', '.join(supported_formats)}"
        )
        return False
    return True


def validate_paths(paths: list[str]):
    """Checks if the paths inputted by the user are valid. If one of them isn't, the program stops.
    Args:
        paths: list of paths to validate
    Returns:
        bool: True if all paths are valid, otherwise False
    """
    for path in paths:
        p = Path(path)
        if not p.exists():
            print(f"{path} is not a valid path.")
            return False
    return True
