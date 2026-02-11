from pathlib import Path
import datetime

p = Path('.')
file_records = []

Docexts = {
    "text": (
        ".txt", ".md", ".rtf"
        ),
    "office": (
        ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx"
        ),
    "open_formats": (
        ".odt", ".ods", ".odp"
        ),
    "academic": (
        ".tex",
        ),
    "data": (
        ".csv",
        ),
    "ebooks": (
        ".pdf", ".epub", ".mobi", ".azw"
        ),
    "publishing": (
        ".pages", ".wpd"
        )
}

sub_cat = ""

for key, value in Docexts.items():
    for x in value:
        print(key,str(x))

# for x in p.iterdir():
#     stat = x.stat()
#     a = dict(
#         file=x,
#         size=stat.st_size,
#         cr_time=datetime.datetime.fromtimestamp(stat.st_ctime),
#         mod_time=datetime.datetime.fromtimestamp(stat.st_mtime),
#         sub_cat=""
#     )
#     file_records.append(a)