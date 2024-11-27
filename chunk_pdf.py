import argparse
import os
import subprocess

def process_pdf_in_chunks(input_pdf, output_dir, chunk_size=30, start_page=None):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Get base filename without extension
    base_name = os.path.splitext(os.path.basename(input_pdf))[0]
    
    # If start_page is not specified, start from the beginning
    current_page = start_page if start_page is not None else 0
    
    while True:
        # Calculate chunk range
        chunk_start = current_page
        chunk_end = current_page + chunk_size
        
        # Create output filename with correct page numbering (including the start page)
        output_file = os.path.join(
            output_dir, 
            f"{base_name}_P_{chunk_start+1}-{chunk_end}.md"
        )
        
        # Construct command
        cmd = [
            "poetry", "run", "python", "convert_single.py",
            input_pdf,
            output_file,
            "--max_pages", str(chunk_size)
        ]
        
        # Add start_page parameter if not starting from beginning
        if chunk_start > 0:
            cmd.extend(["--start_page", str(chunk_start - 1)])  # Subtract 1 to include the start page
        
        # Execute the command
        try:
            subprocess.run(cmd, check=True)
            print(f"Processed pages {chunk_start+1}-{chunk_end} to {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error processing chunk {chunk_start+1}-{chunk_end}: {e}")
            break
            
        # Update for next chunk
        current_page = chunk_end
        
        # Ask user if they want to continue
        response = input(f"\nProcess next chunk (pages {chunk_end+1}-{chunk_end+chunk_size})? [y/n]: ")
        if response.lower() != 'y':
            break

def main():
    parser = argparse.ArgumentParser(description='Process PDF in chunks')
    parser.add_argument('input_pdf', help='Input PDF file')
    parser.add_argument('output_dir', help='Output directory for markdown files')
    parser.add_argument('--chunk-size', type=int, default=30,
                      help='Number of pages per chunk (default: 30)')
    parser.add_argument('--start-page', type=int,
                      help='Starting page number (0-based)')
    
    args = parser.parse_args()
    
    process_pdf_in_chunks(
        args.input_pdf,
        args.output_dir,
        args.chunk_size,
        args.start_page
    )

if __name__ == "__main__":
    main()
