from pathlib import Path
import datetime

unk_items = []
file_records = []
size = []
cr_time = []
mod_time = []
files = []
folders = []
docs = []
images = []
videos = []
audios = []
archives = []
docexts = [
  ".doc", ".docx", ".pdf", ".txt", ".rtf", ".odt",
  ".pages", ".tex", ".wpd", ".md", ".csv",
  ".xls", ".xlsx", ".ods", ".ppt", ".pptx", ".odp"
]
imgexts = (
    ".jpg", ".jpeg", ".png", ".gif", ".bmp",
    ".webp", ".tiff", ".tif", ".svg", ".ico",
    ".heic", ".heif", ".avif"
)
vdsexts = (
    ".mp4", ".mkv", ".avi", ".mov", ".wmv",
    ".flv", ".webm", ".m4v", ".3gp", ".mpeg",
    ".mpg", ".ts"
)
audexts = (
    ".mp3", ".wav", ".flac", ".aac", ".ogg",
    ".wma", ".m4a", ".alac", ".aiff", ".amr"
)
archexts = (
    ".zip", ".rar", ".7z", ".tar", ".gz",
    ".bz2", ".xz", ".iso", ".cab", ".tgz"
)


p = Path('.')

for x in p.iterdir():
    stat = x.stat()
    a = dict(file = x, size = stat.st_size, cr_time = datetime.datetime.fromtimestamp(stat.st_ctime), mod_time = datetime.datetime.fromtimestamp(stat.st_mtime))
    file_records.append(a)

for x in file_records:
    if x['file'].is_file():
        files.append(x)
    elif x['file'].is_dir():
        folders.append(x)
    else:
        unk_items.append(x)

for x in files:
    if str(x['file'].suffix).lower() in docexts:
        docs.append(x)
    elif str(x['file'].suffix).lower() in imgexts:
        images.append(x)
    elif str(x['file'].suffix).lower() in vdsexts:
        videos.append(x)
    elif str(x['file'].suffix).lower() in audexts:
        audios.append(x)
    elif str(x['file'].suffix).lower() in archexts:
        archives.append(x)
    else:
        unk_items.append(x)




print(file_records)
print(files)
print(folders)
print(docs)