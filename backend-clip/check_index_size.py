from app import index
from jina import DocumentArrayMemmap
import os
from glob import glob
import sys

if len(sys.argv) < 2:
    print("Workspace directory not specified so assuming default name 'workspace'")
    root_folder = "workspace"
else:
    root_folder = sys.argv[1]

all_files = glob(root_folder + "/**/header.bin", recursive=True)
index_subfolder = '/'.join(all_files[0].split('/')[:-1])

dam = DocumentArrayMemmap(index_subfolder)
print(f"Your index at {index_subfolder} has {len(dam)} Documents")
