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
