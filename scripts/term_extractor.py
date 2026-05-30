import re, os, sys
import openpyxl

if len(sys.argv) == 1:
    print("Usage: python term_extractor.py [DIRECTORY/FILE TO SCAN] [INPUT WORKBOOK]")
    exit()

scan_path = sys.argv[1]
workbooK_path = sys.argv[2] if len(sys.argv) > 2 else ""

terms = []
directories = [scan_path]

while directories:
    curr = directories.pop()
    if os.path.isdir(curr):
        for subdir in os.listdir(curr): directories.append(os.path.join(curr, subdir))
    if os.path.isfile(curr):
        if not curr.endswith(".md"): continue
        with open(curr, "r", encoding="utf-8") as file:
            matches = re.findall("\{\{(.*?)\}\}", file.read())
        for match in matches:
            parts = match.split(":")
            res = parts[0] + ":%" * (len(parts) - 1) 
            terms.append(res)

terms = dict.fromkeys(sorted(terms), "")
workbook = openpyxl.Workbook()
if workbooK_path and os.path.exists(workbooK_path): workbook = openpyxl.load_workbook(workbooK_path)
sheet = workbook.active
for row in sheet.rows:
    if len(row) <= 1: continue
    print(row[0].value)
    if row[1].value:
        terms[row[0].value] = row[1].value


name = sheet.title
workbook.remove(sheet)
sheet = workbook.create_sheet(name)

for i, term in enumerate(terms):
    sheet[f"A{i+1}"] = term
    sheet[f"B{i+1}"] = terms[term]

print(terms.keys())
workbook.save(workbooK_path or "Translations.xlsx" )
