# PDF Chunking Guide

This guide explains how to use the `chunk_pdf.py` script to process PDF files in chunks.

## Prerequisites

- Python 3.x
- Poetry for dependency management
- The required dependencies installed via Poetry

## Usage

The script allows you to process PDF files in chunks with customizable start pages and chunk sizes.

### Basic Command Structure

```bash
poetry run python chunk_pdf.py <input_pdf> <output_dir> [--start-page PAGE] [--chunk-size SIZE]
```

### Parameters

- `input_pdf`: Path to your input PDF file
- `output_dir`: Directory where the output markdown files will be saved
- `--start-page`: (Optional) Page number to start processing from (default: 0)
- `--chunk-size`: (Optional) Number of pages per chunk (default: 30)

### Examples

1. Process a PDF from the beginning with default chunk size (30 pages):
```bash
poetry run python chunk_pdf.py "Crawl4AI_Code_Docs.pdf" "data/output"
```

2. Continue processing from page 60:
```bash
poetry run python chunk_pdf.py "Crawl4AI_Code_Docs.pdf" "data/output" --start-page 60
```

3. Process with a custom chunk size of 20 pages:
```bash
poetry run python chunk_pdf.py "Crawl4AI_Code_Docs.pdf" "data/output" --chunk-size 20
```

### Output Format

The script will create markdown files in the output directory with names following this pattern:
```
<pdf_name>_P_<start>-<end>.md
```
For example: `Crawl4AI_Code_Docs_P_60-90.md`

## Interactive Mode

After processing each chunk, the script will ask if you want to continue with the next chunk. 
- Type 'y' to process the next chunk
- Type 'n' to stop processing

This allows you to control the processing and check the output between chunks.
