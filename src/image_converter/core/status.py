from dataclasses import dataclass
from enum import Enum

from pathlib import Path
from typing import Optional

class StatusType(str, Enum):
    OK = "ok"
    INVALID = "invalid"
    SKIPPED = "skipped"
    FAILED = "failed"

    def __str__(self):
        return self.value

@dataclass
class Status:
    status: StatusType 
    file: str | Path
    reason: Optional[str] = None

    def __str__(self):
        parts = [
                f"STATUS: {self.status}",
                f"FILE: {self.file}"
                ]

        if self.reason:
            parts.append(f"REASON: {self.reason}")
        
        return ", ".join(parts)

