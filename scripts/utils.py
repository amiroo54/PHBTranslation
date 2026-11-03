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

def extract_from_dict(workbook):
    terms = {}
    for sheet in workbook.worksheets:

        for row in sheet.rows:
            if len(row) == 1: continue
            if not row[1].value: continue

            terms[row[0].value] = [row[1].value, row[2].value if len(row) >= 3 else False]
 
    return terms

def handle_term_backlinks(data: dict) -> dict:
    pattern = re.compile(r"\{\{(.*?)\}\}")
    resolved = {}
    visiting = set()

    def resolve_key(key: str):
        if key in resolved:
            return resolved[key]
        if key in visiting:
            raise ValueError(f"Circular dependency detected at key: '{key}'")
        if key not in data:
            raise KeyError(f"Missing key referenced in template: '{key}'")

        visiting.add(key)
        raw_val = data[key][0]
        resolved_val = resolve_value(raw_val)
        visiting.remove(key)

        resolved[key] = resolved_val
        return resolved_val

    def resolve_value(val):
        if isinstance(val, str):
            while pattern.search(val):
                val = pattern.sub(lambda m: str(resolve_key(m.group(1).strip())), val)
            return val
        elif isinstance(val, dict):
            return {k: resolve_value(v) for k, v in val.items()}
        elif isinstance(val, list):
            return [resolve_value(item) for item in val]
        return val

    return {k: [resolve_key(k), flag] for k, (val, flag) in data.items()}


def natural_to_pascal(text):
    return text.replace("'", "").title().replace(" ", "")

def pascal_to_natural(text):
    return re.sub(r'(?<!^)(?=[A-Z])', ' ', text)

def unescape(text):
    return text.replace("\\n", "\n")

def sort_blocks(text):
    PATTERN = r"<!-- Sort\(\"(.*?)\"\) -->|<!-- SortEnd -->"
    finds = re.finditer(PATTERN, text)

    starts = []
    ends = []
    blocks = [[0]] # AST or something I'm not a software engineer

    for find in finds:
        if find[1]: # The match is a start
            starts.append((find.start(0), find.end(0), find[1]))
        else: # The match is an end
            ends.append((find.start(0), find.end(0)))
        
        if len(starts) == len(ends): # If the counts match it means all nested blocks have ended
            blocks[-1].append(starts[0][0])
            blocks.append([starts[0][1], ends[-1][0], starts[0][2]])
            blocks.append([ends[-1][1]])

            starts = []
            ends = []
    
    blocks[-1].append(len(text))

    output = []
    for block in blocks:
        content = text[block[0]:block[1]]

        if len(block) == 2: # No pattern, no sorting :D
            output.append(content)
            continue
        
        content = sort_blocks(content)
        
        pattern = block[2]

        splits = re.split(pattern, content)
        preceding = splits.pop(0)
        collator = icu.Collator.createInstance(icu.Locale('fa_IR.UTF-8'))
        splits = sorted(splits, key=collator.getSortKey)
        splits.insert(0, preceding)
        content = pattern.join(splits)
        content = unescape(content)
        output.append(content)

    print(output)

    return "".join(output)

def to_persian_numerals(text):
    num_dict = {
        "1": "۱",
        "2": "۲",
        "3": "۳",
        "4": "۴",
        "5": "۵",
        "6": "۶",
        "7": "۷",
        "8": "۸",
        "9": "۹",
        "0": "۰",
    }

    for en, fa in num_dict.items():
        text = text.replace(en, fa)

    return text