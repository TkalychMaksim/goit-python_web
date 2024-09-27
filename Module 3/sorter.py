import os
import shutil
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import sys

def process_directory(source_dir): # Recursive search for files in source directory
    founded_files = []
    for root, _, files in os.walk(source_dir):
        for file_name in files:
            file_path = Path(root) / file_name
            founded_files.append(file_path)
    return founded_files
        
        
        
def creating_extenisons_folders(files,target_dir): # Creating folders with all founded files extensions
    extensions = set()
    for file_path in files:
        ext = file_path.suffix
        extensions.add(ext[1:])
    for ext in extensions:
        target_path = target_dir / ext
        target_path.mkdir(parents=True,exist_ok=True)
    


def copy_files(files,target_dir): # Copying files from source directory to created extensions folders
    for file_path in files:
        ext = file_path.suffix
        target_path = target_dir / ext[1:]
        shutil.copy(file_path,target_path / file_path.name)
        
        

def main(source_dir, target_dir):
    target_dir = Path(target_dir)
    source_dir = Path(source_dir)
    
    if not source_dir.exists(): # Return error if source directory dos not exist
        print(f"Source directory {source_dir} does not exist.")
        return
    
    all_files = process_directory(source_dir) # Getting all files from the source directory using the function

    
    
    with ThreadPoolExecutor() as executor: # Creating a thread pool for parallel creation and filling of directories
        executor.submit(creating_extenisons_folders,all_files,target_dir)
        executor.submit(copy_files, all_files, target_dir)


if __name__ == "__main__":
    source_dir = sys.argv[1]
    target_dir = sys.argv[2] if len(sys.argv) > 2 else 'dist'
    main(source_dir, target_dir)