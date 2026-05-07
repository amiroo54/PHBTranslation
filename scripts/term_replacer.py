
import re, os, sys
import openpyxl

def replace(terms: dict, text: str, replace_braces: bool):
    def process_match(match: re.Match):
        content = match.group(1) # For example "Cone:5"
        
        parts = content.split(":") # ["Cone", "5"]

        base = parts[0] # "Cone"
        args = parts[1:] # ["5"]
        
        key = base + ":%" * len(args) # "Cone:%:%", This is how the extractor extracts these.

        if key in terms: # If there's no args it means it's a simple term and we just return the translation
            replacement = terms[key] # Something like "مخروط ٪ فیتی"
            for arg in args:
                replacement = replacement.replace("%", arg, 1) # This won't allow changing the order but should suffice.
            if replace_braces: replacement = f"{{{{{replacement}}}}}"
            return replacement

        return match.group(0)
    
    return re.sub("\{\{(.*?)\}\}", process_match, text)




def extract_terms(workbook_path):
    workbook = openpyxl.load_workbook(workbook_path)
    sheet = workbook.active

    terms = {}

    for row in sheet.rows:
        if len(row) > 2: continue
        if not row[1].value: continue

        terms[row[0].value] = row[1].value
    return terms


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
            with open(curr, "r", encoding="utf-8") as file:
                text = replace(terms, file.read(), replace_braces)
            
            if output_path:
                relative_path = os.path.relpath(curr, input_path)

                save_path = os.path.join(output_path, relative_path) 

                os.makedirs(os.path.dirname(save_path), exist_ok=True)
            else:
                save_path = curr

            with open(save_path, "w", encoding="uft-8") as file:
                file.write(text)

                
if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage: python term_replacer.py [INPUT WORKBOOK] [DIRECTORY/FILE TO REPLACE] [DIRECTORY/FILE TO OUTPUT TO] [REPLACE BRACES]")
        
        exit()

    workbook_path = sys.argv[1] if len(sys.argv) > 1 else ""
    input_path = sys.argv[2] if len(sys.argv) > 2 else ""
    output_path = sys.argv[3] if len(sys.argv) > 3 else ""
    replace_braces = len(sys.argv) > 4
    terms = extract_terms(workbook_path)
    if os.path.isfile(input_path):
        replace_file(terms, input_path, replace_braces, output_path)
    else:
        replace_directory(terms, input_path, replace_braces, output_path)