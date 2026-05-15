import openpyxl, os, sys
from utils import replace
if len(sys.argv) == 1:
    print("Usage: python spell_creator.py [SPELL WORKBOOK] [TRANSLATION WORKBOOK] [DIRECTORY TO OUTPUT] [STARING ROW]")
    
    exit()

workbook_path = sys.argv[1] if len(sys.argv) > 1 else ""
translation_path = sys.argv[2] if len(sys.argv) > 2 else ""
output_path = sys.argv[3] if len(sys.argv) > 3 else ""
starting_row = int(sys.argv[4]) if len(sys.argv) > 4 else 0 

workbook = openpyxl.load_workbook(workbook_path)
translation_workbook = openpyxl.load_workbook(translation_path)
def worksheet_to_strings(workbook, output_path, formatting_text):
    output = []
    for row in workbook.active:
        data = map(lambda x: x.value, row)
        output.append(formatting_text.format(*data))

    return output

terms = {}

for row in translation_workbook.active.rows:
    if len(row) > 2: continue
    if not row[1].value: continue

    terms[row[0].value] = row[1].value

sheet = workbook.active

sheet.delete_rows(0, starting_row)
text = """{0}
{{{{CastingTime}}}} : {1}
{{{{Range}}}}: {2}
{{{{Components}}}}: {3}
{{{{Duration}}}}: {4}

{5}
"""
for row in sheet:
    if not row[2].value:
        continue
    english_name = row[0].value
    persian_name = row[1].value
    school = row[2].value
    level = row[3].value
    time = row[4].value
    spell_range = row[5].value
    components = row[6].value
    duration = row[7].value
    concentration = int(row[8].value)
    ritual = int(row[9].value)
    description = row[11].value
    school += " {{{{Level}}}} " + str(level)
    if concentration: duration = "{{Concentration}}, " + duration
    if ritual: time += " or {{Ritual}}"

    formatted_text = text.format(school, time, spell_range, components, duration, description)
    formatted_text = replace(terms, formatted_text, False)
    formatted_text = formatted_text.replace("\\n", "\n")

    output_file = os.path.join(output_path, english_name + ".md")
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(formatted_text)

