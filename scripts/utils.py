import os, re, icu

def replace(terms: dict, text: str, replace_braces: bool, callbacks = {}):
    def process_match(match: re.Match):
        content = match.group(1) # For example "Cone:5"
        
        parts = content.split(":") # ["Cone", "5"]

        base = parts[0] # "Cone"
        args = parts[1:] # ["5"]
        
        key = base + ":%" * len(args) # "Cone:%:%", This is how the extractor extracts these.

        if key in terms: # If there's no args it means it's a simple term and we just return the translation

            replacement = terms[key][0] # Something like "مخروط ٪ فیتی"
            for arg in args:
                replacement = replacement.replace("%", arg, 1) # This won't allow changing the order but should suffice.
            
            if key in callbacks.keys():
                callback_result = callbacks[key](*args, term=terms[key][0])
                if callback_result: replacement = callback_result 
            
            if replace_braces: replacement = f"{{{{{replacement}}}}}"

            if terms[key][1]:
                replacement += f" ({pascal_to_natural(key)})"
                terms[key][1] = False
            return replacement

        return match.group(0)
    
    return re.sub(r"\{\{(.*?)\}\}", process_match, text)

def realize_backlink(index_path, vault_root):
    def process_match(match: re.Match):
        content = match.group(1)
        if not content.endswith(".md"):
            content += ".md"
        
        text = realize_backlink(content, vault_root)
        return text
    path = os.path.join(vault_root, index_path)
    with open(path, "r") as file:
        text = file.read()
        return re.sub(r"\[\[(.*?)\]\]", process_match, text)

def extract_from_dict(sheet):
    terms = {}

    for row in sheet.rows:
        if len(row) == 1: continue
        if not row[1].value: continue

        terms[row[0].value] = [row[1].value, row[2].value if len(row) >= 3 else False]
    return terms

def natural_to_pascal(text):
    return text.capitalize().replace(" ", "")

def pascal_to_natural(text):
    return re.sub(r'(?<!^)(?=[A-Z])', ' ', text)

def extract_blocks(start_pattern, end_pattern, text):

    starts = [(m.start(0), m.end(0), m.group(1))  for m in re.finditer(start_pattern, text)]
    ends = [(m.start(0), m.end(0)) for m in re.finditer(end_pattern, text)]

    blocks = map(lambda x: ((x[0][0], x[0][1]), (x[1][0], x[1][1]), x[0][2]), zip(starts, ends))
    return blocks

def sort_blocks(text):
    START_PATTERN = r"<!-- Sort\(\"(.*?)\"\) -->"
    END_PATTERN = r"<!-- SortEnd -->"

    blocks = extract_blocks(START_PATTERN, END_PATTERN, text)
    chunks = [(text[block[0][0]:block[1][1]], block[2]) for block in blocks]
    output = text
    for chunk in chunks:
        raw = chunk[0]
        raw_no_comment = raw[:raw.rfind("\n")] # Removing the end comment
        separator = chunk[1]
        separator = separator.replace("\\n", "\n")

        separated = list(raw_no_comment.split(separator))
        collator = icu.Collator.createInstance(icu.Locale('fa_IR.UTF-8'))
        separated = sorted(separated, key=collator.getSortKey)
        separated = list(filter(lambda x: not x.startswith("<!--"), separated))
        replacement = separator + separator.join(separated)
        replacement = replacement.strip()

        output = output.replace(raw, replacement).strip()
    return output