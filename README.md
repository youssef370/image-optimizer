# Image Converter

A fast, extensible CLI tool for converting and optimizing images across multiple formats.

Designed for developers and build pipelines, **image-converter** supports batch processing, caching, and automation-friendly workflows.

---

## Features

* Convert images between formats (JPEG, PNG, WebP, AVIF, etc.)
* Batch processing for entire directories
* Built-in caching to avoid redundant conversions
* Configurable compression/quality settings
* CLI-first design (scriptable & automation-friendly)
* Modular architecture for easy extension
* (Planned) Parallel processing for improved performance
* (Planned) JSON config override support

---

## Installation

### Option 1: Install globally with pipx (recommended)

```bash
pipx install image-converter
```

### Option 2: Install from source

```bash
git clone https://github.com/yourusername/image-converter.git
cd image-converter
pip install .
```

---

## Usage

### Basic usage

```bash
image-converter input.jpg output.webp
```

### Convert with quality setting

```bash
image-converter input.png output.jpg --quality 80
```

### Batch conversion

```bash
image-converter ./images ./output --format webp
```

---

## CLI Options

| Option        | Description                               |
| ------------- | ------------------------------------------|
| `--format`    | Output format (jpeg, png, webp, avif)     |
| `--quality`   | Compression quality (format-dependent)    |
| `--output`    | Output file or directory                  |
| `--recursive` | Process directories recursively           |
| `--parallel`  | Enable parallel processing (max 4 cores)  |

---

## Caching

The tool includes a caching mechanism to prevent re-processing unchanged images.

### Current behavior

* Stores processed file metadata
* Skips conversion if input hasn't changed

### Known limitation

* If an output file is manually deleted, the cache may still consider it valid

### Planned fix

* Cache invalidation based on output file existence

---

## Configuration (Planned)

Support for JSON-based configuration:

```bash
image-converter --config config.json
```

Example config:

```json
{
  "format": "webp",
  "quality": 75,
  "recursive": true
}
```

---

## Project Structure

```
src
├── image_converter
│   ├── cli.py
│   ├── core
│   │   ├── cache.py
│   │   ├── converters.py
│   │   ├── encoders.py
│   │   ├── globals.py
│   │   ├── __init__.py
│   │   ├── parser.py
│   │   ├── __pycache__
│   │   │   ├── cache.cpython-312.pyc
│   │   │   ├── converters.cpython-312.pyc
│   │   │   ├── encoders.cpython-312.pyc
│   │   │   ├── globals.cpython-312.pyc
│   │   │   ├── __init__.cpython-312.pyc
│   │   │   ├── parser.cpython-312.pyc
│   │   │   ├── status.cpython-312.pyc
│   │   │   ├── task.cpython-312.pyc
│   │   │   ├── utils.cpython-312.pyc
│   │   │   └── validators.cpython-312.pyc
│   │   ├── status.py
│   │   ├── task.py
│   │   ├── utils.py
│   │   └── validators.py
│   ├── execution
│   │   ├── __pycache__
│   │   │   ├── runner.cpython-312.pyc
│   │   │   └── worker.cpython-312.pyc
│   │   ├── runner.py
│   │   └── worker.py
│   ├── __init__.py
│   └── __pycache__
│       ├── cache.cpython-312.pyc
│       ├── cli.cpython-312.pyc
│       ├── converters.cpython-312.pyc
│       ├── encoders.cpython-312.pyc
│       ├── globals.cpython-312.pyc
│       ├── __init__.cpython-312.pyc
│       ├── parser.cpython-312.pyc
│       ├── status.cpython-312.pyc
│       ├── utils.cpython-312.pyc
│

---

## Development

### Run locally

```bash
python -m image_converter.cli
```

### Install in editable mode

```bash
pip install -e .
```

---

## Testing (Planned)

* Unit tests for core modules
* Integration tests for CLI workflows
* End-to-end tests for real file conversions

---

## Roadmap

* Fix cache invalidation edge cases
* JSON and YAML configuration support
* Improve error handling and logging
* Plugin system for custom formats or pipelines

---

## Contributing

Contributions are welcome.

1. Fork the repo
2. Create a feature branch
3. Submit a pull request

---

## License

MIT License

---

## Why this project?

Most image tools are either:

* Too heavy (GUI-based)
* Too limited (single conversion only)
* Not developer-friendly

**image-converter** aims to be:

* Fast
* Scriptable
* Reliable in production pipelines
