from pathlib import Path
import datetime

p = Path(".")
unk_items = []
file_records = []
files = []
folders = []
docs = []
ucatdocs = []
images = []
videos = []
audios = []
archives = []
docexts = {
    "text": (
        ".txt", ".rtf", ".md", ".rst"
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
        ),
    "languages": (
        ".py", ".js", ".ts", ".java", ".c", ".cpp", ".cs",
        ".go", ".rs", ".swift", ".kt", ".rb", ".php"
    ),
    "web": (
        ".html", ".css", ".scss", ".sass", ".less"
    ),
    "frontend_frameworks": (
        ".jsx", ".tsx"
    ),
    "data_config": (
        ".json", ".xml", ".yaml", ".yml", ".toml"
    ),
    "database": (
        ".sql",
    ),
    "scripting": (
        ".sh", ".bash", ".zsh", ".ps1", ".bat", ".cmd"
    ),
    "build_tools": (
        ".gradle", ".maven", ".lock"
    ),
    "devops": (
        ".dockerfile", ".tf"
    ),
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
        ".svg",
    ),
    "icons": (
        ".ico",
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
        ".iso",
    ),
    "windows_packages": (
        ".cab",
    ),
}
arch_set = {
    ext
    for val in archexts.values()
    for ext in (val if isinstance(val, tuple) else [val])
}

for x in p.iterdir():
    stat = x.stat()
    a = dict(
        file=x,
        size=stat.st_size,
        cr_time=datetime.datetime.fromtimestamp(stat.st_ctime),
        mod_time=datetime.datetime.fromtimestamp(stat.st_mtime),
        sub_cat=""
    )
    file_records.append(a)

for x in file_records:
    if x["file"].is_file():
        files.append(x)
    elif x["file"].is_dir():
        x.update(sub_cat='folder')
        folders.append(x)
    else:
        unk_items.append(x)

for x in files:
    ext = str(x['file'].suffix).lower()
    if ext in doc_set:
        for key, value in docexts.items():
            for y in value:
                if ext == str(y):
                    x.update(sub_cat=key)
        docs.append(x)
    elif ext in img_set:
        for key, value in imgexts.items():
            for y in value:
                if ext == str(y):
                    x.update(sub_cat=key)
        images.append(x)
    elif ext in vds_set:
        for key, value in vdsexts.items():
            for y in value:
                if ext == str(y):
                    x.update(sub_cat=key)
        videos.append(x)
    elif ext in aud_set:
        for key, value in audexts.items():
            for y in value:
                if ext == str(y):
                    x.update(sub_cat=key)
        audios.append(x)
    elif ext in arch_set:
        for key, value in archexts.items():
            for y in value:
                if ext == str(y):
                    x.update(sub_cat=key)
        archives.append(x)
    else:
        x.update(sub_cat="uncategorized")
        ucatdocs.append(x)

