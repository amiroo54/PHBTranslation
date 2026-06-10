
import re, os, sys
import openpyxl
from utils import replace, extract_from_dict


def replace_file(terms, input_path, replace_braces, output_path=None):
    ready_text = replace(terms, open(input_path).read(), replace_braces)
    print(ready_text)
    confirmation = input("Do you want to write this N/y? ")
    if confirmation.strip().lower() == "y": 
        with open(output_path or input_path, "w") as file:
            file.write(ready_text)
    exit()


def replace_directory(terms, input_path, replace_braces, output_path=None):
    directories = [input_path]

    while directories:
        curr = directories.pop()
        if os.path.isdir(curr):
            for subdir in os.listdir(curr): directories.append(os.path.join(curr, subdir))
        if os.path.isfile(curr):
            if not curr.endswith(".md"): continue
            
            with open(curr, "r", encoding="utf-8") as file:
                text = replace(terms, file.read(), replace_braces)
            
            if output_path:
                relative_path = os.path.relpath(curr, input_path)

                save_path = os.path.join(output_path, relative_path) 

                os.makedirs(os.path.dirname(save_path), exist_ok=True)
            else:
                save_path = curr


            with open(save_path, "w", encoding="utf-8") as file:
                file.write(text)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage: python term_replacer.py [INPUT WORKBOOK] [DIRECTORY/FILE TO REPLACE] [DIRECTORY/FILE TO OUTPUT TO] [REPLACE BRACES]")
        
        exit()

    workbook_path = sys.argv[1] if len(sys.argv) > 1 else ""
    input_path = sys.argv[2] if len(sys.argv) > 2 else ""
    output_path = sys.argv[3] if len(sys.argv) > 3 else ""
    replace_braces = len(sys.argv) > 4

    workbook = openpyxl.load_workbook(workbook_path)
    sheet = workbook.active

    terms = extract_from_dict(sheet)

    if os.path.isfile(input_path):
        replace_file(terms, input_path, replace_braces, output_path)
    else:
        replace_directory(terms, input_path, replace_braces, output_path)
