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
ucatdocs = []
images = []
videos = []
audios = []
archives = []
docexts = {
    "text": (".txt", ".md", ".rtf"),
    "office": (".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx"),
    "open_formats": (".odt", ".ods", ".odp"),
    "academic": (".tex"),
    "data": (".csv"),
    "ebooks": (".pdf", ".epub", ".mobi", ".azw"),
    "publishing": (".pages", ".wpd"),
}
doc_set = {
    ext
    for val in docexts.values()
    for ext in (val if isinstance(val, tuple) else [val])
}
imgexts = {
    "common": (
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"
    ),

    "print": (
        ".tiff", ".tif"
    ),

    "vector": (
        ".svg"
    ),

    "icons": (
        ".ico"
    ),

    "mobile": (
        ".heic", ".heif", ".avif"
    ),
    "raw_camera": (
    ".raw", ".cr2", ".nef", ".arw", ".dng", ".orf", ".rw2"
    )
}

img_set = {
    ext
    for val in imgexts.values()
    for ext in (val if isinstance(val, tuple) else [val])
}
vdsexts = {
    "standard": (
        ".mp4", ".mkv", ".avi", ".mov"
    ),
    "web": (
        ".webm", ".flv"
    ),
    "platform_specific": (
        ".wmv", ".m4v", ".3gp"
    ),
    "broadcast_legacy": (
        ".mpeg", ".mpg", ".ts"
    ),
}
vds_set = {
    ext
    for val in vdsexts.values()
    for ext in (val if isinstance(val, tuple) else [val])
}
audexts = {
    "lossy": (
        ".mp3", ".aac", ".ogg", ".wma", ".m4a", ".amr"
    ),
    "lossless": (
        ".flac", ".alac"
    ),
    "uncompressed_studio": (
        ".wav", ".aiff"
    ),
}
aud_set = {
    ext
    for val in audexts.values()
    for ext in (val if isinstance(val, tuple) else [val])
}
archexts = {
    "compressed": (
        ".zip", ".rar", ".7z"
    ),
    "tar_archives": (
        ".tar", ".tgz"
    ),
    "single_compressed": (
        ".gz", ".bz2", ".xz"
    ),
    "disk_images": (
        ".iso"
    ),
    "windows_packages": (
        ".cab"
    ),
}
arch_set = {
    ext
    for val in archexts.values()
    for ext in (val if isinstance(val, tuple) else [val])
}

p = Path(".")

for x in p.iterdir():
    stat = x.stat()
    a = dict(
        file=x,
        size=stat.st_size,
        cr_time=datetime.datetime.fromtimestamp(stat.st_ctime),
        mod_time=datetime.datetime.fromtimestamp(stat.st_mtime),
    )
    file_records.append(a)

for x in file_records:
    if x["file"].is_file():
        files.append(x)
    elif x["file"].is_dir():
        folders.append(x)
    else:
        unk_items.append(x)

for x in files:
    ext = str(x['file'].suffix).lower()
    if ext in doc_set:
        docs.append(x)
    elif ext in img_set:
        images.append(x)
    elif ext in vds_set:
        videos.append(x)
    elif ext in aud_set:
        audios.append(x)
    elif ext in arch_set:
        archives.append(x)
    else:
        ucatdocs.append(x)


print(files)
print(folders)
print(docs)
