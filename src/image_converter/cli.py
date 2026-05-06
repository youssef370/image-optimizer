#!/usr/bin/env python3

import sys
from pathlib import Path

from image_converter.execution.runner import run_pipeline


from .core.validators import validate_paths
from .core.globals import DEFAULT_QUALITIES, CACHE_NAME
from .core.parser import parser
from .core.cache import Cache


def main():
    args = parser.parse_args()
    paths = [Path(p) for p in args.paths]
    output_format = args.format.lower()
    if output_format == "jpg":
        output_format == "jpeg"
 
    quality = args.quality or DEFAULT_QUALITIES[output_format]
    output_dir = Path(args.output) if args.output else None
    recursive = args.recursive
    parallel = args.parallel
    
    if not validate_paths(paths):
        sys.exit()
    
    results = []

    cache = Cache(CACHE_NAME)
    results = run_pipeline(
            paths=paths,
            output_format=output_format,
            quality=quality,
            cache=cache,
            recursive=recursive,
            parallel=parallel,
            output_dir=output_dir
            )
    
if __name__ == "__main__":
    main()
