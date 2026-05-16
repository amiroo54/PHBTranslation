import re, os, sys
from utils import realize_backlink


if len(sys.argv) == 1:
    print("Usage: python chapter_assembler.py [INDEX FILE] [VAULT ROOT] [OUTPUT FILE]")
    exit()

index_path = sys.argv[1]
vault_root = sys.argv[2] if len(sys.argv) > 2 else ""
output_path = sys.argv[3] if len(sys.argv) > 3 else ""

with open(output_path, "w+") as file:
    file.write(realize_backlink(index_path, vault_root))