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