# MPEG to GIF Converter

A simple tool to convert MP4 videos to GIFs. Supports batch processing via configuration or single file conversion via command-line arguments.

## Installation

1. Clone the repository.
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## Usage

The program operates in two modes:

### Mode 1: Batch Processing (via .env)
To process all `.mp4` files in a source folder:
1. Copy `.env.example` to `.env`: `cp .env.example .env`
2. Configure your folders in `.env`:
   - `SOURCE_FOLDER`: Path to the directory containing MP4 files.
   - `OUTPUT_FOLDER`: Path to the directory where GIFs will be saved.
   - `FREQ`: Speed multiplier (e.g., 2.0 to double speed).
   - `WIDTH`: Target width in pixels (e.g., 480).
3. Run without arguments:
   ```bash
   python main.py
   ```

### Mode 2: Single File (via Arguments)
To convert a specific file with custom settings:
```bash
python main.py input.mp4 [output.gif] [--freq 2.0] [--width 640]
```
If `output.gif` is not specified, it will use the input filename with a `.gif` extension.

## Build

To build a standalone executable binary:
```bash
./build.sh
```
The resulting binary will be in `dist/mpeg2gif`.

## Help
Run with `--help` to see all available options:
```bash
python main.py --help
```
