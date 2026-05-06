from ..core.status import Status, StatusType
from ..core.cache import Cache, CacheEntry, compute_hash_key
from ..core.task import Task, TaskResult
from .worker import worker

from pathlib import Path


def run(tasks, parallel, cache):
    if parallel:
        return run_parallel(tasks, cache)
    return run_sequential(tasks, cache)


def run_sequential(tasks, cache: Cache):
    results = []

    for task in tasks:
        result = worker(task)
        results.append(result)

        if result.status == StatusType.OK:
            cache_entry = build_cache_entry(result=result, task=task)
            cache.add(cache_entry)

    cache.save()
    return results


def run_parallel(tasks, cache: Cache):
    from multiprocessing import Pool, cpu_count

    with Pool(min(cpu_count(), 4)) as pool:
        results = pool.map(worker, tasks)

    for task, result in zip(tasks, results):
        if result.status.status == StatusType.OK:
            cache_entry = build_cache_entry(result=result, task=task) 
            cache.add(cache_entry)
    
    cache.save()
    return results


def run_pipeline(
    *,
    paths: list[str],
    output_format: str,
    quality: int,
    cache: Cache,
    parallel: bool = False,
    recursive: bool = False,
    output_dir: Path | None = None,
):

    all_results = []
    for path in paths:
        if path.is_dir():
            tasks = build_tasks(
                folder_path=path,
                output_format=output_format,
                quality=quality,
                output_dir=output_dir or (path / "converted"),
                cache=cache,
                recursive=recursive,
            )
        else:
            tasks = build_tasks(
                folder_path=path.parent,
                output_format=output_format,
                quality=quality,
                output_dir=output_dir or (path.parent / "converted"),
                cache=cache,
                recursive=recursive,
            )
            tasks = [t for t in tasks if t.file_path == path]

        results = run(tasks, cache=cache, parallel=parallel)

        all_results.extend(results)

    return all_results


def build_cache_entry(result: TaskResult, task: Task):
    return CacheEntry(
        key=task.cache_key,
        input_file=task.file_path,
        output_file=result.output_file,
        output_format=task.output_format,
        quality=task.quality,
    )


def build_tasks(
    folder_path: Path,
    output_format: str,
    quality: int,
    output_dir: Path,
    cache: Cache,
    recursive: bool = False,
) -> list[Task]:

    tasks = []

    files = folder_path.rglob("*") if recursive else folder_path.iterdir()
    for file in files:
        if not file.is_file():
            continue

        try:
            file.relative_to(folder_path)
        except ValueError:
            continue

        key = compute_hash_key(file, output_format, quality)
        if cache.lookup(key):
            print(Status(status=StatusType.SKIPPED, file=file, reason="ALREADY IN CACHE"))
            continue

        relative_path = file.relative_to(folder_path)
        target_dir = output_dir / relative_path.parent
        target_dir.mkdir(parents=True, exist_ok=True)

        tasks.append(
            Task(
                file_path=file,
                output_format=output_format,
                quality=quality,
                output_dir=output_dir,
                cache_key=key,
            )
        )

    return tasks
