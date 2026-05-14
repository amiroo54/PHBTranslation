import re, os, sys

if len(sys.argv) == 1:
    print("Usage: python chapter_assembler.py [INDEX FILE] [VAULT ROOT] [OUTPUT FILE]")
    exit()

index_path = sys.argv[1]
vault_root = sys.argv[2] if len(sys.argv) > 2 else ""
output_path = sys.argv[3] if len(sys.argv) > 3 else ""


def realize_backling(index_path, vault_root):
    def process_match(match: re.Match):
        content = match.group(1)
        if not content.endswith(".md"):
            content += ".md"
        text = realize_backling(content, vault_root)
        return text

    with open(os.path.join(vault_root, index_path), "r") as file:
        text = file.read()
        return re.sub("\[\[(.*?)\]\]", process_match, text)

with open(output_path, "w+") as file:
    file.write(realize_backling(index_path, vault_root))