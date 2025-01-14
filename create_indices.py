from modalities.api import create_local_index, create_global_index, create_shuffled_global_index
from pathlib import Path

# Split the files first using your split_script.py
# Then create indices:

base_dir = Path("data/processed")
for folder in base_dir.glob("split_*"):
    for jsonl_file in folder.glob("*.jsonl"):
        # Create index file path in same directory as jsonl file
        #index_path = jsonl_file.with_suffix('.idx')
        #create_local_index(src_path=jsonl_file, index_path=index_path)  # Now providing both required arguments
        pass
# Similarly for global index:

# Create a file list of all JSONL files
file_list_output = base_dir / "file_list.txt"
with open(file_list_output, "w") as f:
    for folder in base_dir.glob("split_*"):
        for jsonl_file in folder.glob("*.jsonl"):
            # Write relative path from base_dir
            relative_path = jsonl_file.relative_to(base_dir)
            f.write(f"{relative_path}\n")

# Create directory for global index
global_index_path = Path("data/global_index")
global_index_path.mkdir(parents=True, exist_ok=True)  # Create directory if it doesn't exist

# Create global index
create_global_index(
    file_list_path=file_list_output,
    root_index_path=base_dir,
    global_index_root_path=global_index_path
)

# Create shuffled index
create_shuffled_global_index(
    global_index_file_path=global_index_path / "global_index_inorder.idx"
)