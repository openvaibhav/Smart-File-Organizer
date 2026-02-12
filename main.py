from pathlib import Path
import os
import shutil
import datetime

p = Path(".")
dest = ''
cwd=os.getcwd()
unk_items = []
file_records = []
files = []
folders = []
doc_ext_map = {
    # text
    ".txt": "text",
    ".rtf": "text",
    ".md": "text",
    ".rst": "text",

    # office
    ".doc": "office",
    ".docx": "office",
    ".xls": "office",
    ".xlsx": "office",
    ".ppt": "office",
    ".pptx": "office",

    # open formats
    ".odt": "open_formats",
    ".ods": "open_formats",
    ".odp": "open_formats",

    # academic
    ".tex": "academic",

    # data
    ".csv": "data",

    # ebooks
    ".pdf": "ebooks",
    ".epub": "ebooks",
    ".mobi": "ebooks",
    ".azw": "ebooks",

    # publishing
    ".pages": "publishing",
    ".wpd": "publishing",

    # languages
    ".py": "languages",
    ".js": "languages",
    ".ts": "languages",
    ".java": "languages",
    ".c": "languages",
    ".cpp": "languages",
    ".cs": "languages",
    ".go": "languages",
    ".rs": "languages",
    ".swift": "languages",
    ".kt": "languages",
    ".rb": "languages",
    ".php": "languages",

    # web
    ".html": "web",
    ".css": "web",
    ".scss": "web",
    ".sass": "web",
    ".less": "web",

    # frontend frameworks
    ".jsx": "frontend_frameworks",
    ".tsx": "frontend_frameworks",

    # data/config
    ".json": "data_config",
    ".xml": "data_config",
    ".yaml": "data_config",
    ".yml": "data_config",
    ".toml": "data_config",

    # database
    ".sql": "database",

    # scripting
    ".sh": "scripting",
    ".bash": "scripting",
    ".zsh": "scripting",
    ".ps1": "scripting",
    ".bat": "scripting",
    ".cmd": "scripting",

    # build tools
    ".gradle": "build_tools",
    ".maven": "build_tools",
    ".lock": "build_tools",

    # devops
    ".dockerfile": "devops",
    ".tf": "devops",
}
img_ext_map = {
    # common
    ".jpg": "common",
    ".jpeg": "common",
    ".png": "common",
    ".gif": "common",
    ".bmp": "common",
    ".webp": "common",

    # print
    ".tiff": "print",
    ".tif": "print",

    # vector
    ".svg": "vector",

    # icons
    ".ico": "icons",

    # mobile
    ".heic": "mobile",
    ".heif": "mobile",
    ".avif": "mobile",

    # raw camera
    ".raw": "raw_camera",
    ".cr2": "raw_camera",
    ".nef": "raw_camera",
    ".arw": "raw_camera",
    ".dng": "raw_camera",
    ".orf": "raw_camera",
    ".rw2": "raw_camera",
}
video_ext_map = {
    # standard
    ".mp4": "standard",
    ".mkv": "standard",
    ".avi": "standard",
    ".mov": "standard",

    # web
    ".webm": "web",
    ".flv": "web",

    # platform specific
    ".wmv": "platform_specific",
    ".m4v": "platform_specific",
    ".3gp": "platform_specific",

    # broadcast / legacy
    ".mpeg": "broadcast_legacy",
    ".mpg": "broadcast_legacy",
    ".ts": "broadcast_legacy",
}
audio_ext_map = {
    # lossy
    ".mp3": "lossy",
    ".aac": "lossy",
    ".ogg": "lossy",
    ".wma": "lossy",
    ".m4a": "lossy",
    ".amr": "lossy",

    # lossless
    ".flac": "lossless",
    ".alac": "lossless",

    # uncompressed studio
    ".wav": "uncompressed_studio",
    ".aiff": "uncompressed_studio",
}
archive_ext_map = {
    # compressed
    ".zip": "compressed",
    ".rar": "compressed",
    ".7z": "compressed",

    # tar archives
    ".tar": "tar_archives",
    ".tgz": "tar_archives",

    # single compressed
    ".gz": "single_compressed",
    ".bz2": "single_compressed",
    ".xz": "single_compressed",

    # disk images
    ".iso": "disk_images",

    # windows packages
    ".cab": "windows_packages",
}

for x in p.iterdir():
    stat = x.stat()
    a = dict(
        file=x,
        size=stat.st_size,
        cr_time=datetime.datetime.fromtimestamp(stat.st_ctime),
        mod_time=datetime.datetime.fromtimestamp(stat.st_mtime),
        type="",
        cat="",
        sub_cat=""
    )
    file_records.append(a)

for x in file_records:
    if x["file"].is_file():
        x.update(type='file')
        files.append(x)
    elif x["file"].is_dir():
        x.update(type='folder')
        folders.append(x)
    else:
        x.update(type='unknown')
        unk_items.append(x)

for x in files:
    ext = str(x['file'].suffix).lower()
    if ext in doc_ext_map:
        x.update(sub_cat=doc_ext_map[ext],cat="Document")
    elif ext in img_ext_map:
        x.update(sub_cat=img_ext_map[ext],cat="Image")
    elif ext in audio_ext_map:
        x.update(sub_cat=audio_ext_map[ext],cat="Audio")
    elif ext in video_ext_map:
        x.update(sub_cat=video_ext_map[ext],cat="Video")
    elif ext in archive_ext_map:
        x.update(sub_cat=archive_ext_map[ext],cat="Archive")
    else:
        x.update(cat="Uncategorized")
        
print(file_records)


#Copy Files Function
def copy_files_cur_dir():
    for x in files:
        file = str(x['file'])
        if x['cat'] == 'Document':
            temp_src = str(os.path.join(cwd, file))
            temp_path = str(os.path.join(cwd, "__Documents"))
            temp_subcat_path = str(os.path.join(temp_path, x['sub_cat']))
            temp_dest = str(os.path.join(temp_subcat_path, file))
            try:
                os.mkdir(temp_path)
                os.mkdir(temp_subcat_path)
            except FileExistsError:
                pass
            shutil.copy(temp_src, temp_dest)
        elif x['cat'] == 'Image':
            temp_src = str(os.path.join(cwd, file))
            temp_path = str(os.path.join(cwd, "__Images"))
            temp_subcat_path = str(os.path.join(temp_path, x['sub_cat']))
            temp_dest = str(os.path.join(temp_subcat_path, file))
            try:
                os.mkdir(temp_path)
                os.mkdir(temp_subcat_path)
            except FileExistsError:
                pass
            shutil.copy(temp_src, temp_dest)
        elif x['cat'] == 'Audio':
            temp_src = str(os.path.join(cwd, file))
            temp_path = str(os.path.join(cwd, "__Audios"))
            temp_subcat_path = str(os.path.join(temp_path, x['sub_cat']))
            temp_dest = str(os.path.join(temp_subcat_path, file))
            try:
                os.mkdir(temp_path)
                os.mkdir(temp_subcat_path)
            except FileExistsError:
                pass
            shutil.copy(temp_src, temp_dest)
        elif x['cat'] == 'Video':
            temp_src = str(os.path.join(cwd, file))
            temp_path = str(os.path.join(cwd, "__Videos"))
            temp_subcat_path = str(os.path.join(temp_path, x['sub_cat']))
            temp_dest = str(os.path.join(temp_subcat_path, file))
            try:
                os.mkdir(temp_path)
                os.mkdir(temp_subcat_path)
            except FileExistsError:
                pass
            shutil.copy(temp_src, temp_dest)
        elif x['cat'] == 'Archive':
            temp_src = str(os.path.join(cwd, file))
            temp_path = str(os.path.join(cwd, "__Archives"))
            temp_subcat_path = str(os.path.join(temp_path, x['sub_cat']))
            temp_dest = str(os.path.join(temp_subcat_path, file))
            try:
                os.mkdir(temp_path)
                os.mkdir(temp_subcat_path)
            except FileExistsError:
                pass
            shutil.copy(temp_src, temp_dest)
        else:
            temp_src = str(os.path.join(cwd, file))
            temp_path = str(os.path.join(cwd, "__Unknown"))
            temp_dest = str(os.path.join(temp_path, file))
            try:
                os.mkdir(temp_path)
            except FileExistsError:
                pass
            shutil.copy(temp_src, temp_dest)
    