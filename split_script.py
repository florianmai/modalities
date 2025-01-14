import json
from pathlib import Path
import random

def split_jsonl_file(input_file: Path, output_base_dir: Path, max_folders: int, files_per_folder: int = 2, lines_per_file: int = 1000):
    """
    Splits a large JSONL file into multiple smaller files across different folders, up to max_folders.
    
    Args:
        input_file: Path to input JSONL file
        output_base_dir: Base directory for output folders
        max_folders: Maximum number of folders to create
        files_per_folder: Number of files to create per folder
        lines_per_file: Number of lines per output file
    """
    # Create base output directory
    output_base_dir.mkdir(exist_ok=True, parents=True)
    
    # Read all lines from input file
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    # Shuffle lines
    random.shuffle(lines)
    
    # Calculate number of folders needed, but cap at max_folders
    total_files = len(lines) // lines_per_file + (1 if len(lines) % lines_per_file else 0)
    num_folders = min(max_folders, (total_files + files_per_folder - 1) // files_per_folder)
    
    current_line = 0
    
    for folder_idx in range(num_folders):
        # Create folder
        folder_path = output_base_dir / f"split_{folder_idx:03d}"
        folder_path.mkdir(exist_ok=True)
        
        # Create files in this folder
        for file_idx in range(files_per_folder):
            if current_line >= len(lines):
                break
                
            file_path = folder_path / f"data_{file_idx:03d}.jsonl"
            
            # Get chunk of lines for this file
            end_line = min(current_line + lines_per_file, len(lines))
            chunk = lines[current_line:end_line]
            
            # Write chunk to file
            with open(file_path, 'w') as f:
                f.writelines(chunk)
            
            current_line = end_line
            if current_line >= len(lines):
                break

# Usage example
if __name__ == "__main__":
    input_file = Path("data/raw/fineweb_edu_num_docs_483606.jsonl")
    output_dir = Path("data/processed")
    
    split_jsonl_file(
        input_file=input_file,
        output_base_dir=output_dir,
        max_folders=5,         # Maximum 5 folders
        files_per_folder=2,    # 2 files per folder
        lines_per_file=1000    # 1000 lines per file
    )