import os
from utils import *
from callbacks import *
import openpyxl
import typst
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

CALLBAKCS = {
    "GP:%": gp_callback,
    "SP:%": sp_callback,
    "CP:%": cp_callback,
    "LB:%": lb_callback,
}

def render():
    realized_text = realize_backlink("Book.md", "PHBFA")

    typst_file = open("data/format.typ").read()
    compiler = typst.Compiler()
    dictionaries = os.listdir("dictionaries")
    
    for dictionary in dictionaries:
        if dictionary.startswith(".") or not dictionary.endswith(".xlsx"): continue
        workbook = openpyxl.open(os.path.join("dictionaries", dictionary))

        terms = extract_from_dict(workbook)
        
        compiled_text = replace(terms, realized_text, False, CALLBAKCS)

        compiled_text = sort_blocks(compiled_text)

        pdf_bytes = compiler.compile(bytes(typst_file, "utf-8"), sys_inputs={"text": compiled_text, "column-count": "2"})

        os.makedirs("tmp/out", exist_ok=True)
        open(f"tmp/out/{dictionary.split(".")[0]}.pdf", "wb+").write(pdf_bytes)

render()

class MySnoopingHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # Make sure we only react to the specific file, not everything in the directory
        path = event.src_path
        if not os.path.isdir(path) and not path.endswith(".pdf"):
            print("File changed")
            try:
                render()
            except Exception as e:
                print(e)
                print("An error occured.")
observer = Observer()
event_handler = MySnoopingHandler()
# Watch the directory containing your file
observer.schedule(event_handler, path='../', recursive=True)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()