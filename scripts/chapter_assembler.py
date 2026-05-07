import re, os, sys

if len(sys.argv) == 1:
    print("Usage: python chapter_assembler.py [INDEX FILE] [OUTPUT FILE]")
    exit()

index_path = sys.argv[1]
output_path = sys.argv[2] if len(sys.argv) > 2 else ""

if not os.path.isfile(index_path):
    print(f"Error: {index_path} is not a file")
    exit()

with open(index_path, "r", encoding="utf-8") as file:
    lines = file.readlines()

vault_root = os.path.dirname(index_path)
chapter_name = os.path.splitext(os.path.basename(index_path))[0]
sections_dir = os.path.join(vault_root, chapter_name)

if not os.path.isdir(sections_dir):
    print(f"Error: {sections_dir} directory not found")
    exit()

def to_pascal_case(text):
    words = re.split(r'[\s_-]+', text)
    return ''.join(word.capitalize() for word in words if word)

assembled = []

for line in lines:
    line = line.strip()
    if not line: continue
    
    match = re.search(r"\[\[(.*?)\]\]", line)
    if not match: continue
    
    section_path = match.group(1)
    
    if not section_path.endswith(".md"):
        section_path += ".md"
    
    full_path = os.path.join(sections_dir, section_path)
    
    if not os.path.isfile(full_path):
        print(f"Warning: {full_path} not found, skipping")
        continue
    
    section_name = os.path.splitext(os.path.basename(section_path))[0]
    with open(full_path, "r", encoding="utf-8") as section_file:
        content = section_file.read()
    
    pascal_name = to_pascal_case(section_name)
    assembled.append(f"# {{{{{pascal_name}}}}}\n\n{content}\n\n")

final_text = "".join(assembled)

if output_path:
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(final_text)
    print(f"Assembled chapter saved to {output_path}")
else:
    print(final_text)
