# Marker Setup Guide for Windows with RTX 2060

This guide provides instructions for setting up Marker on Windows with RTX 2060, using Poetry for package management.

## System Configuration

- **OS**: Windows 10/11
- **GPU**: NVIDIA RTX 2060 (6GB VRAM)
- **RAM**: 16GB
- **Python**: 3.10
- **CUDA**: 11.8

## Installation Steps

1. **Prerequisites**
   ```powershell
   # Install Python 3.10
   winget install Python.Python.3.10

   # Install Git
   winget install Git.Git

   # Install Visual Studio Build Tools 2019 (for C++ compilation)
   winget install Microsoft.VisualStudio.2019.BuildTools
   ```

2. **Install Poetry**
   ```powershell
   # Install Poetry using PowerShell
   (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
   ```

3. **Install CUDA**
   - Download [CUDA Toolkit 11.8](https://developer.nvidia.com/cuda-11-8-0-download-archive)
   - Install with default options
   - Verify installation:
     ```powershell
     nvidia-smi
     ```

4. **Setup Marker**
   ```powershell
   # Clone repository
   git clone https://github.com/VikParuchuri/marker.git
   cd marker

   # Configure Poetry to create venv in project directory
   poetry config virtualenvs.in-project true

   # Install dependencies
   poetry install

   # Install PyTorch with CUDA support
   poetry run pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
   ```

5. **Configure for RTX 2060**
   Create `local.env` with these optimized settings:
   ```shell
   # Device Settings
   TORCH_DEVICE=cuda

   # RTX 2060 Optimized Batch Sizes
   DETECTOR_BATCH_SIZE=8
   RECOGNITION_BATCH_SIZE=32
   TEXIFY_BATCH_SIZE=6
   LAYOUT_BATCH_SIZE=8
   ORDER_BATCH_SIZE=8
   TABLE_REC_BATCH_SIZE=4

   # Windows Parallel Processing
   PDFTEXT_CPU_WORKERS=6
   DETECTOR_POSTPROCESSING_CPU_WORKERS=6
   OCR_PARALLEL_WORKERS=3

   # RTX 2060 Memory-Optimized Quality Settings
   OCR_ENGINE=surya
   SURYA_DETECTOR_DPI=144
   SURYA_OCR_DPI=300
   SURYA_LAYOUT_DPI=144
   SURYA_TABLE_DPI=300

   # RTX 2060 VRAM Optimizations
   ORDER_MAX_BBOXES=512
   TEXIFY_MODEL_MAX=768
   TEXIFY_TOKEN_BUFFER=512

   # Quality Settings
   EXTRACT_IMAGES=true
   FLATTEN_PDF=true
   OCR_ALL_PAGES=true
   BBOX_INTERSECTION_THRESH=0.85
   TABLE_INTERSECTION_THRESH=0.85
   IMAGE_DPI=300
   HEADING_MERGE_THRESHOLD=0.15
   DEBUG=true
   ```

## Usage

1. **Directory Structure**
   ```
   data/
   ├── input/     # Place your PDF files here
   └── output/    # Converted markdown files will appear here
   ```

2. **Activate Environment**
   ```powershell
   # Navigate to marker directory
   cd path/to/marker

   # Activate Poetry shell
   poetry shell
   ```

3. **Convert PDFs**
   ```powershell
   # Single PDF using data directories
   poetry run python convert_single.py "data/input/your-file.pdf" "data/output/your-file.md"

   # Multiple PDFs
   poetry run python convert_dir.py "data/input" "data/output"

   # Convert specific pages (e.g., first 5 pages)
   poetry run python convert_single.py "data/input/your-file.pdf" "data/output/your-file.md" --max_pages 5
   ```

## Troubleshooting

1. **GPU Memory Issues**
   - Close other GPU applications
   - Monitor GPU usage in Task Manager
   - For large documents, try:
     ```shell
     SURYA_DETECTOR_DPI=96
     SURYA_OCR_DPI=192
     ```

2. **Poetry Issues**
   ```powershell
   # List environments
   poetry env list

   # Rebuild environment
   poetry env remove --all
   poetry install --sync
   ```

3. **Common Errors**
   - **PATH issues**: Restart terminal after Poetry installation
   - **CUDA errors**: Update NVIDIA drivers
   - **DLL errors**: Install/repair Visual C++ Redistributable

## Performance Notes

- Processing time: ~15 seconds per page
- VRAM usage: 4-5GB
- Optimal for documents up to 50 pages
- Best quality/speed ratio with current settings

# Setup and Usage Guide

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/marker.git
cd marker
```

2. Install Poetry (if not already installed):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

3. Install dependencies:
```bash
poetry install
```

## PDF Processing Tools

### PDF Chunking Tool

This tool allows you to process PDF files in chunks with customizable start pages and chunk sizes.

#### Basic Command Structure

```bash
poetry run python chunk_pdf.py <input_pdf> <output_dir> [--start-page PAGE] [--chunk-size SIZE]
```

#### Parameters

- `input_pdf`: Path to your input PDF file
- `output_dir`: Directory where the output markdown files will be saved
- `--start-page`: (Optional) Page number to start processing from (default: 0)
- `--chunk-size`: (Optional) Number of pages per chunk (default: 30)

#### Examples

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

#### Output Format

The script will create markdown files in the output directory with names following this pattern:
```
<pdf_name>_P_<start>-<end>.md
```
For example: `Crawl4AI_Code_Docs_P_60-90.md`

#### Interactive Mode

After processing each chunk, the script will ask if you want to continue with the next chunk. 
- Type 'y' to process the next chunk
- Type 'n' to stop processing

This allows you to control the processing and check the output between chunks.

## Project Structure

```
marker/
├── chunk_pdf.py          # PDF chunking script
├── convert_single.py     # Single PDF conversion script
├── data/                 # Data directory
│   ├── input/           # Input PDFs
│   └── output/          # Output markdown files
└── poetry.lock          # Poetry dependency lock file
```

## Troubleshooting

If you encounter any issues:

1. Ensure all dependencies are installed:
```bash
poetry install
```

2. Check if the input PDF file exists and is readable
3. Verify that the output directory is writable
4. Make sure you have sufficient disk space for the output files

## Contributing

1. Create a new branch for your feature:
```bash
git checkout -b feature-name
```

2. Make your changes and commit them:
```bash
git add .
git commit -m "Description of changes"
```

3. Push to your branch:
```bash
git push origin feature-name
```

4. Create a Pull Request on GitHub
