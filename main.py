from pathlib import Path
import datetime

unk_items = []
all_files_folders = []
size = []
cr_time = []
mod_time = []
files = []
folders = []

p = Path('.')

for x in p.iterdir():
    all_files_folders.append(x)
    stat = x.stat()
    cr_time.append(datetime.datetime.fromtimestamp(stat.st_ctime))
    mod_time.append(datetime.datetime.fromtimestamp(stat.st_mtime))
    size.append(stat.st_size)

for y in all_files_folders:
    if y.is_file():
        files.append(y)
    elif y.is_dir():
        folders.append(y)
    else:
        unk_items.append(y)


print(files)
print(folders)
print(size)
print(cr_time)
print(mod_time)