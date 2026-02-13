from pathlib import Path
import os
import shutil
import datetime
import argparse

file_records = []
files = []
folders = []
unk_items = []
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

def source_cur_dir():
    p = Path(".")
    return p
    
def source_other_dir(src):
    if Path(src).exists():
        p = Path(src)
        return p
    else:
        raise Exception("Path does not exist")

def dest_cur_dir():
    d = Path(".")
    return d
    
def dest_other_dir(des):
    if Path(des).exists():
        d = Path(des)
        return d
    else:
        raise Exception("Path does not exist")

parser = argparse.ArgumentParser(description="Automate everyday file management tasks")
parser.add_argument('--src',metavar='src',type=str,help='Input Source')
parser.add_argument('--des',metavar='des',type=str,help='Input Destination')
parser.add_argument('-dr', '--dry_run', action='store_true',help='Dry Run Preview')
args = parser.parse_args()
src = args.src
des = args.des

if src == None:
    p = source_cur_dir()
elif src != None:
    p = source_other_dir(src)

if des == None:
    d = dest_cur_dir()
elif des != None:
    d = dest_other_dir(des)

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

#Copy Files Function
def copy_files_cur_dir():
    for x in files:
        file = x['file']
        loc = "__" + x['cat']
        try:
            temp_src = str(file)
            temp_path = str(os.path.join(des, loc))
            try:
                os.mkdir(temp_path)
            except FileExistsError:
                pass
            try:
                if x['sub_cat']:
                    temp_subcat_path = str(os.path.join(temp_path, x['sub_cat']))
                    temp_dest = str(os.path.join(temp_subcat_path, file.name))
                    os.mkdir(temp_subcat_path)
                else:
                    temp_dest = str(os.path.join(temp_path, file.name))
            except Exception as e:
                raise(e)
            shutil.copy(temp_src, temp_dest)
        except Exception as e:
            raise(e)

#Move Files Function
def move_files_cur_dir():
    for x in files:
        file = x['file']
        loc = "__" + x['cat']
        try:
            temp_src = str(file)
            temp_path = str(os.path.join(des, loc))
            try:
                os.mkdir(temp_path)
            except FileExistsError:
                pass
            try:
                if x['sub_cat']:
                    temp_subcat_path = str(os.path.join(temp_path, x['sub_cat']))
                    temp_dest = str(os.path.join(temp_subcat_path, file.name))
                    os.mkdir(temp_subcat_path)
                else:
                    temp_dest = str(os.path.join(temp_path, file.name))
            except Exception as e:
                raise(e)
            shutil.move(temp_src, temp_dest)
        except Exception as e:
            raise(e)

#Dry Run Preview
def dry_run_preview(des, file_record):
    for x in file_record:
        file = x['file']
        if x['cat']:
            loc = "__" + x['cat']
        else :
            loc = ""
        try:
            temp_src = str(file)
            temp_path = str(os.path.join(des, loc))
            try:
                if x['sub_cat']:
                    temp_subcat_path = str(os.path.join(temp_path, x['sub_cat']))
                    temp_dest = str(os.path.join(temp_subcat_path, file.name))
                else:
                    temp_dest = str(os.path.join(temp_path, file.name))
            except Exception as e:
                raise(e)
            print(temp_src + " --> " + temp_dest)
        except Exception as e:
            raise(e)
        
if args.dry_run:
    dry_run_preview(d, file_records)
else:
    pass