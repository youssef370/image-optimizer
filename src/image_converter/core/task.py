from dataclasses import dataclass
from pathlib import Path
from .status import Status

@dataclass(frozen=True)
class Task:
    file_path: Path
    output_format: str 
    quality: int 
    output_dir: str
    cache_key: str

@dataclass
class TaskResult:
    status: Status
    task: Task
    output_file: Path | None = None


