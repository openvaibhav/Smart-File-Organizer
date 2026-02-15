# Imports
from pathlib import Path
import os
import shutil
import datetime
import argparse
import sys
import json
import string
import random

# Argparse setup
parser = argparse.ArgumentParser(description="Automate everyday file management tasks")
parser.add_argument('-s','--src',metavar='src',type=str,help='Input Source of where you want the automation to be done')
parser.add_argument('-d','--des',metavar='des',type=str,help='Input Destination of where you want the final output')
parser.add_argument('-m','--mode',metavar='mode',type=str,help='Mode of Script - Copy | Move')
parser.add_argument('-oc','--on_collision',metavar='collision',type=str,help='Mode of Collision (What you want to do if the file/files exists at the destination) - (Default) Skip | Rename | Overwrite')
parser.add_argument('-r', '--recursive', action='store_true',help='This will sort all files and even files inside subfolders')
parser.add_argument('-e', '--exclude', metavar='exclude',help='This will exclude files and folders (Separate inputs with commas)')
parser.add_argument('-dr', '--dry_run', action='store_true',help='Dry Run Preview (No Execution)')

args = parser.parse_args()

# Extensions load from json
try:
    with open("extensions.json", "r") as f:
        data = json.load(f)
except FileNotFoundError:
    print("Extensions json file not found")
    sys.exit(1)
    
# Variables and lists
files = []

src = args.src if args.src else "."
des = args.des if args.des else "."
mode = args.mode.lower() if args.mode else None

doc_ext_map = data["doc_ext_map"]
img_ext_map = data["img_ext_map"]
audio_ext_map = data["audio_ext_map"]
video_ext_map = data["video_ext_map"]
archive_ext_map = data["archive_ext_map"]

categories = data["categories"]
set_cat_dict = categories.copy()
for key,value in set_cat_dict.items():
    set_cat_dict[key] = f"__{value}"
set_cat = set(set_cat_dict.values())

if args.exclude:
    exclude_list = set_cat.union(set(args.exclude.split(",")))
else:
    exclude_list = set_cat
    
if args.on_collision:
    if str(args.on_collision).lower() == "overwrite":
        on_collision = "overwrite"
    elif str(args.on_collision).lower() == "rename":
        on_collision = "rename"
    elif str(args.on_collision).lower() == "skip":
        on_collision = "skip"
    else:
        print("Collision arguement not correct, if needed default (skip) action will be done")
        on_collision = "skip"
elif not args.on_collision:
    print("Collision arguement not provided, if needed default (skip) action will be done")
    on_collision = "skip"
    
# Permission Checks
dest_ok = os.access(des, os.W_OK | os.X_OK)
if dest_ok:
    pass
elif not dest_ok:
    print(f"Please check the permissions of destination dir (To move you need write and exec permissions.)")
    sys.exit(1)    
    
# Files Iteration
def collect_files(mode, P ,exclude_list):
    forbidden = set(exclude_list)
    for x in P:
        if forbidden and any(part in forbidden for part in x.parts):
            continue
        
        if x.is_file():
            stat = x.stat()
            
            if args.dry_run or mode == "copy":
                src_ok = os.access(x, os.R_OK)
            elif mode == "move":
                src_ok = os.access(x, os.W_OK | os.X_OK)
            else:
                src_ok = True
                
            if not src_ok:
                print(f"Please check the permissions of {x}. For now its being removed from the sorting system.")
                continue
            
            a = dict(
                file=x,
                size=stat.st_size,
                cr_time=datetime.datetime.fromtimestamp(stat.st_ctime),
                mod_time=datetime.datetime.fromtimestamp(stat.st_mtime),
                cat="",
                sub_cat=""
            )
            files.append(a)
            
# Collision Handling
def coll_handling(file, dest, file_h):
    ext = file.suffix
    if file_h == "overwrite":
        return "overwrite"
    elif file_h == "rename":
        chars = string.ascii_lowercase + string.digits
        random_str = file.stem + "__collision_" + ''.join(random.choices(chars, k=10)) + ext
        destn = os.path.join(dest, random_str)
        while os.path.exists(destn):
            random_str = file.stem + "__collision_" + ''.join(random.choices(chars, k=10)) + ext
            destn = os.path.join(dest, random_str)

        return destn
    else:
        return "skip"
    
    
# Copy or Move Files Function
def copy_move_files(des, mode, files, on_collision):
    t = 0
    c = set()
    subc = set()
    strng = "Processed"
    strng = "Copied" if mode == "copy" else "Moved"
    for x in files:
        file = x['file']
        loc = f"__{x['cat']}" if x['cat'] else ""
        try:
            src_path = str(file)
            dest_dir = os.path.join(des, loc, x.get('sub_cat', ''))
            if dest_dir not in subc:
                subc.add(dest_dir)
            dest_path = os.path.join(dest_dir, file.name)
            try:
                Path(dest_dir).mkdir(parents=True, exist_ok=True)
            except Exception as e:
                print(f"Error Creating Folder : {e}")
            if mode == "copy":
                if os.path.exists(dest_path):
                    handler = coll_handling(file, dest_dir, on_collision)
                    if handler == "skip":
                        continue
                    elif handler == "overwrite":
                        os.remove(dest_path)
                        shutil.copy(src_path, dest_path)
                        t += 1
                        if loc not in c:
                            c.add(loc)
                    else:
                        shutil.copy(src_path, handler)
                        print(f"File copied to {handler} successfully")
                        t += 1
                        if loc not in c:
                            c.add(loc)
                else:
                    shutil.copy(src_path, dest_path)
                    t += 1
                    if loc not in c:
                        c.add(loc)
                    
            else:
                if os.path.exists(dest_path):
                    handler = coll_handling(file, dest_dir, on_collision)
                    if handler == "skip":
                        continue
                    elif handler == "overwrite":
                        os.remove(dest_path)
                        shutil.move(src_path, dest_path)
                        t += 1
                        if loc not in c:
                            c.add(loc)
                    else:
                        shutil.move(src_path, handler)
                        print(f"File moved to {handler} successfully")
                        t += 1
                        if loc not in c:
                            c.add(loc)
                else:
                    shutil.move(src_path, dest_path)
                    t += 1
                    if loc not in c:
                        c.add(loc)
        except Exception as e:
            raise(e)
    cc = len(c)
    subcc = len(subc)
    print(f"Sorted({strng}) {t} files into {cc} Categories and {subcc} Subcategories to {des}")

# Dry Run Preview
def dry_run_preview(on_collision, des, files):
    prepped_paths = []
    for x in files:
        file = x['file']
        loc = f"__{x['cat']}" if x['cat'] else ""
        
        dest_dir = os.path.join(des, loc, x.get('sub_cat', ''))
        dest_path = os.path.join(dest_dir, file.name)
        
        if os.path.exists(dest_path):
            handler = coll_handling(file, dest_dir, on_collision)
            if handler == "skip":
                prepped_paths.append((str(file), "Skipped"))
            elif handler == "overwrite":
                prepped_paths.append((str(file), str(dest_path)))
            else:
                prepped_paths.append((str(file), str(handler)))
        else:
            prepped_paths.append((str(file), str(dest_path)))

    if not prepped_paths:
        return
    
    prepped_paths.sort(key=lambda path_pair: path_pair[1].lower())
    
    max_src_len = max(len(srcc) for srcc, destt in prepped_paths) + 2

    for srcc, destt in prepped_paths:
        print(f"{srcc:<{max_src_len}} --> {destt}")

# Variable locations setup
if args.src:
    if Path(src).exists():
        p = Path(src)
    else:
        print("Path does not exist")
        sys.exit(1)
        
elif not args.src:
    p = Path(src)

if args.des:
    if Path(des).exists():
        if Path(des).resolve().is_relative_to(Path(src).resolve()):
            print("Destination cannot be inside Source")
            sys.exit(1)
        d = Path(des)
    else:
        print("Path does not exist")
        sys.exit(1)
    
elif not args.des:
    d = Path(des)

# Collecting Metadata
P = p.rglob("*") if args.recursive else p.iterdir()
collect_files(mode, P, exclude_list)

# Updating Category and Sub-Category of Files
for x in files:
    ext = str(x['file'].suffix).lower()
    if ext in doc_ext_map:
        x.update(sub_cat=doc_ext_map[ext],cat=categories["doc_ext_map"])
    elif ext in img_ext_map:
        x.update(sub_cat=img_ext_map[ext],cat=categories["img_ext_map"])
    elif ext in audio_ext_map:
        x.update(sub_cat=audio_ext_map[ext],cat=categories["audio_ext_map"])
    elif ext in video_ext_map:
        x.update(sub_cat=video_ext_map[ext],cat=categories["video_ext_map"])
    elif ext in archive_ext_map:
        x.update(sub_cat=archive_ext_map[ext],cat=categories["archive_ext_map"])
    else:
        x.update(cat="Uncategorized")
        
# Main CLI
if len(sys.argv) == 1:
    print(f"{parser.prog}: try 'python {parser.prog} --help' for more information")
    sys.exit(1)
else:
    if args.dry_run:
        dry_run_preview(on_collision, d, files)
    else:
        if mode == "copy" or mode == "move":
            copy_move_files(d, mode, files, on_collision)
        else:
            print(f"{parser.prog}: try 'python {parser.prog} --help' for more information")