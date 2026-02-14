# Imports
from pathlib import Path
import os
import shutil
import datetime
import argparse
import sys
import json

# Argparse setup
parser = argparse.ArgumentParser(description="Automate everyday file management tasks")
parser.add_argument('-s','--src',metavar='src',type=str,help='Input Source of where you want the automation to be done')
parser.add_argument('-d','--des',metavar='des',type=str,help='Input Destination of where you want the final output')
parser.add_argument('-m','--mode',metavar='mode',type=str,help='Mode of Script - Copy | Move')
parser.add_argument('-r', '--recursive', action='store_true',help='This will sort all files and even files inside subfolders')
parser.add_argument('-e', '--exclude', metavar='exclude',help='This will exclude files and folders (Separate inputs with commas)')
parser.add_argument('-dr', '--dry_run', action='store_true',help='Dry Run Preview (No Execution)')

args = parser.parse_args()

# Variables and lists
files = []
src = args.src
des = args.des
mode = args.mode.lower() if args.mode else None
if args.exclude:
    exclude_list = set(args.exclude.split(","))
else:
    exclude_list = set()

# Extensions load from json
with open("extensions.json", "r") as f:
    data = json.load(f)

doc_ext_map = data["doc_ext_map"]
img_ext_map = data["img_ext_map"]
audio_ext_map = data["audio_ext_map"]
video_ext_map = data["video_ext_map"]
archive_ext_map = data["archive_ext_map"]
categories = data["categories"]

# Source initialisation
def source_cur_dir():
    p = Path(".")
    return p
    
def source_other_dir(src):
    if Path(src).exists():
        p = Path(src)
        return p
    else:
        raise Exception("Path does not exist")

# Destination initialisation
def dest_cur_dir():
    d = Path(".")
    return d
    
def dest_other_dir(des):
    if Path(des).exists():
        d = Path(des)
        return d
    else:
        raise Exception("Path does not exist")
    
# Files Iteration
def collect_files(P,exclude_list):
    forbidden = set(exclude_list)
    for x in P:
        if forbidden and any(part in forbidden for part in x.parts):
            continue
        
        if x.is_file():
            stat = x.stat()
            a = dict(
                file=x,
                size=stat.st_size,
                cr_time=datetime.datetime.fromtimestamp(stat.st_ctime),
                mod_time=datetime.datetime.fromtimestamp(stat.st_mtime),
                cat="",
                sub_cat=""
            )
            files.append(a)
    
# Copy or Move Files Function
def copy_move_files(mode, des, files):
    t = 0
    c = set()
    for x in files:
        file = x['file']
        loc = f"__{x['cat']}" if x['cat'] else ""
        if loc not in c:
            c.add(loc)
        try:
            src_path = str(file)
            dest_dir = os.path.join(des, loc, x.get('sub_cat', ''))
            dest_path = os.path.join(dest_dir, file.name)
            try:
                Path(dest_dir).mkdir(parents=True, exist_ok=True)
            except Exception as e:
                print(f"Error Creating Folder : {e}")
            if mode == "copy":
                shutil.copy(src_path, dest_path)
                strng = "Copied"
            else:
                shutil.move(src_path, dest_path)
                strng = "Moved"
            t += 1
        except Exception as e:
            raise(e)
    cc = len(c)
    print(f"Sorted({strng}) {t} files into {cc} Categories to {des}")

# Dry Run Preview
def dry_run_preview(des, files):
    prepped_paths = []
    for x in files:
        file = x['file']
        loc = f"__{x['cat']}" if x['cat'] else ""
        
        dest_dir = os.path.join(des, loc, x.get('sub_cat', ''))
        dest_path = os.path.join(dest_dir, file.name)
        
        prepped_paths.append((str(file), str(dest_path)))

    if not prepped_paths:
        return
    
    prepped_paths.sort(key=lambda path_pair: path_pair[1].lower())
    
    max_src_len = max(len(srcc) for srcc, destt in prepped_paths) + 2

    for srcc, destt in prepped_paths:
        print(f"{srcc:<{max_src_len}} --> {destt}")

# Variable locations setup
if src == None:
    p = source_cur_dir()
elif src != None:
    p = source_other_dir(src)

if des == None:
    d = dest_cur_dir()
elif des != None:
    d = dest_other_dir(des)

# Collecting Metadata
P = p.rglob("*") if args.recursive else p.iterdir()
collect_files(P, exclude_list)

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
        dry_run_preview(d, files)
    else:
        if mode == "copy" or mode == "move":
            copy_move_files(mode, d, files)
        else:
            print(f"{parser.prog}: try 'python {parser.prog} --help' for more information")