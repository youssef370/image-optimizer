from ..core.converters import convert_file
from ..core.task import Task, TaskResult
from ..core.status import StatusType

def worker(task: Task) -> TaskResult:
    status = convert_file(
            file_path=task.file_path,
            output_format=task.output_format,
            quality=task.quality,
            output_dir=task.output_dir,
            )

    print(status)
    return TaskResult(
            status=status,
            task=task,
            output_file=status.file if status.status == StatusType.OK else None,
            )

