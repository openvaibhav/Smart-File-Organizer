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
parser.add_argument('-s','--src',metavar='Source',type=str,help='Input Source of where you want the automation to be done')
parser.add_argument('-d','--des',metavar='Destination',type=str,help='Input Destination of where you want the final output')
parser.add_argument('-m','--mode',metavar='Copy | Move',type=str,help='Mode of Script')
parser.add_argument('-oc','--on_collision',metavar='(Default) Skip | Rename | Overwrite',type=str,help='Mode of Collision (What you want to do if the file/files exists at the destination)')
parser.add_argument('-r', '--recursive', action='store_true',help='This will sort all files and even files inside subfolders')
parser.add_argument('-e', '--exclude', metavar='Files/Folders',help='This will exclude files and folders (Separate inputs with commas)')
parser.add_argument('-l', '--logs',nargs='?',const=True,default=None,type=int,metavar='Time',help='-l show all the logs logged with dates and data | -l [sr. no.(int)] shows the specific log of that sr. no.')
parser.add_argument('-u', '--undo',nargs='?',const=True,default=None,type=int,metavar='Undo',help='-u undo the last instance | -u [sr. no.(int)] undo the specific instance of that sr. no.')
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
log_sr = args.logs
RUN_ID = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
    
# On Collision
def on_collision():
    if args.on_collision:
        if str(args.on_collision).lower() == "overwrite":
            return "overwrite"
        elif str(args.on_collision).lower() == "rename":
            return "rename"
        elif str(args.on_collision).lower() == "skip":
            return "skip"
        else:
            print("Collision arguement not correct, if needed default (skip) action will be done")
            return "skip"
    elif not args.on_collision and not args.logs:
        print("Collision arguement not provided, if needed default (skip) action will be done")
        return "skip"

# Load Logs
def load_logs(i):
    data = []
    with open('log.jsonl', 'r') as f:
            for line in f:
                data.append(json.loads(line))
    if i == "l":    
        data.sort(key=lambda x: x["id"])
    else:
        data.sort(key=lambda x: x["id"], reverse=True)
        
    return data

# Main log Menu    
def show_log_menu():
    try:
        data = load_logs("l")
        ids = []
        files = []
        action = []
        sk = []
        tmp = ""
        file = 0
        skip_c = 0
        if not data:
            print("No logs")
            sys.exit(1)
        for item in data:
            is_skip = str(item.get('on_collision')) == "skip"
            run_id = item.get('id')
            act = item.get('action')
            if str(run_id) != tmp:
                ids.append(run_id)
                if tmp != "":
                    files.append(file)
                    sk.append(skip_c)
                action.append(act)
                tmp = str(run_id)
                skip_c = 1 if is_skip else 0
                file = 0 if is_skip else 1
            else:
                if is_skip:
                    skip_c += 1
                elif not is_skip:
                    file += 1
        files.append(file)
        sk.append(skip_c)
        return ids, files, action, sk
    except Exception as e:
        print(e)
        
# Log with ID
def field(label, value):
    v = value if value else "-"
    return f"{label:<14}: {v}"

def trunc_path(p, max_len=60):
    p = str(p)
    if len(p) <= max_len:
        return p
    return "..." + p[-55:]

def log_sr_check(sr_no, run_ids, fcnt, mode, skpcnt):
    try:
        data = load_logs("l")
        if not data:
            print("No logs")
            sys.exit(1)
        print("_"*40)
        print(field("Run ID", run_ids[sr_no]))
        print(field("Mode", mode))
        print(field("Files", fcnt))
        print(field("Skipped", skpcnt))
        print("_"*40)
        a = 1
        for item in data:
            if run_ids[sr_no] == item.get('id'):
                run_id = item.get('id')
                org_file = item.get('original_file')
                fca = item.get('file_created_at')
                ea = item.get('executed_at')
                la =item.get('logged_at')
                src = item.get('src_path')
                des = item.get('dest_path')
                action = item.get('action').capitalize()
                on_coll = item.get('on_collision')
                renamed_to = item.get('renamed_to')
                print("_"*40)
                print(a,".",org_file)
                print(field("Created", fca))
                print(field("Executed", ea))
                print(field("Logged", la))
                print(field("Source", trunc_path(src)))
                print(field("Destination", trunc_path(des)))
                print(field("Action", action))
                print(field("On Collision", on_coll))
                print(field("Renamed to", renamed_to))
                print("_"*40)
                a += 1
    except Exception as e:
        print(e)
    
# Permission Checks
dest_ok = os.access(des, os.W_OK | os.X_OK)
if dest_ok:
    pass
elif not dest_ok:
    print(f"Please check the permissions of destination dir (To move you need write and exec permissions.)")
    sys.exit(1)    
    
# Logs
def logs(org_file_name,created_at,c_time,src_path_log,dest_path_log,mode,handler,name):
    log_entry = {
        "id": RUN_ID,
        "original_file": str(org_file_name),
        "file_created_at": str(created_at),
        "executed_at": str(c_time),
        "logged_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "src_path": str(src_path_log),
        "dest_path": str(dest_path_log),
        "action": mode,
        "on_collision": handler,
        "renamed_to": name
    }
    
    with open("log.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")

# Files Iteration
def collect_files(mode, P ,exclude_list):
    forbidden = set(exclude_list)
    for x in P:
        if forbidden and any(part in forbidden for part in x.parts):
            continue
        
        if x.is_file():
            stat = x.stat()
            
            a = dict(
                file=x,
                size=stat.st_size,
                cr_time=datetime.datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S"),
                mod_time=datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
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
        created_at = x['cr_time']
        org_file_name = file.name
        src_path_log = Path.resolve(file)
        loc = f"__{x['cat']}" if x['cat'] else ""
        try:
            src_path = str(file)
            dest_dir = os.path.join(des, loc, x.get('sub_cat', ''))
            if dest_dir not in subc:
                subc.add(dest_dir)
            dest_path = os.path.join(dest_dir, file.name)
            t_dest = Path(dest_path)
            dest_path_log = Path.resolve(t_dest)
            try:
                Path(dest_dir).mkdir(parents=True, exist_ok=True)
            except Exception as e:
                print(f"Error Creating Folder : {e}")
            if mode == "copy":
                if os.path.exists(dest_path):
                    handler = coll_handling(file, dest_dir, on_collision)
                    if handler == "skip":
                        c_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        name = None
                        logs(org_file_name,created_at,c_time,src_path_log,dest_path_log,mode,handler,name)
                        continue
                    elif handler == "overwrite":
                        c_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        name = None
                        os.remove(dest_path)
                        shutil.copy(src_path, dest_path)
                        t += 1
                        if loc not in c:
                            c.add(loc)
                        logs(org_file_name,created_at,c_time,src_path_log,dest_path_log,mode,handler,name)
                    else:
                        c_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        name = Path(handler).name
                        dest_path_log = Path.resolve(handler)
                        shutil.copy(src_path, handler)
                        print(f"File copied to {handler} successfully")
                        t += 1
                        if loc not in c:
                            c.add(loc)
                        handler = "rename"
                        logs(org_file_name,created_at,c_time,src_path_log,dest_path_log,mode,handler,name)
                else:
                    c_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    handler = None
                    name = None
                    shutil.copy(src_path, dest_path)
                    t += 1
                    if loc not in c:
                        c.add(loc)
                    logs(org_file_name,created_at,c_time,src_path_log,dest_path_log,mode,handler,name)
                    
            else:
                if os.path.exists(dest_path):
                    handler = coll_handling(file, dest_dir, on_collision)
                    if handler == "skip":
                        c_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        name = None
                        logs(org_file_name,created_at,c_time,src_path_log,dest_path_log,mode,handler,name)
                        continue
                    elif handler == "overwrite":
                        c_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        name = None
                        os.remove(dest_path)
                        shutil.move(src_path, dest_path)
                        t += 1
                        if loc not in c:
                            c.add(loc)
                        logs(org_file_name,created_at,c_time,src_path_log,dest_path_log,mode,handler,name)
                    else:
                        c_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        name = Path(handler).name
                        dest_path_log = Path.resolve(handler)
                        shutil.move(src_path, handler)
                        print(f"File moved to {handler} successfully")
                        t += 1
                        if loc not in c:
                            c.add(loc)
                        handler = "rename"
                        logs(org_file_name,created_at,c_time,src_path_log,dest_path_log,mode,handler,name)
                else:
                    c_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    handler = None
                    name = None
                    shutil.move(src_path, dest_path)
                    t += 1
                    if loc not in c:
                        c.add(loc)
                    logs(org_file_name,created_at,c_time,src_path_log,dest_path_log,mode,handler,name)
                        
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
        
# Undo Last Instance
def undo_last_instance(run_ids, files_count, act, s):
    try:
        data = load_logs("u")
        id = run_ids.pop()
        for item in data:
            if id == item.get('id'):
                org_file = item.get('original_file')
                src_path = Path(item.get('dest_path'))
                dest_path = Path(item.get('src_path'))
                src_dir = src_path.parent
                dest_dir = dest_path.parent
                action = item.get('action')
                handler = item.get('on_collision')
                renamed_to = item.get('renamed_to')
                try:
                    os.path.exists(src_dir)
                    os.path.exists(dest_dir)
                except Exception as e:
                    print(f"Cannot find location...\nError:{e}\nPlease check logs and check both locations exist...\nExiting...")
                    sys.exit(1)
                if action == "move":
                    if os.path.exists(dest_path):
                        pass
                    else:
                        if handler == "skip":
                            continue
                        elif handler == "overwrite":
                            shutil.move(src_path, dest_path)
                        elif handler == "rename":
                            dest_path = dest_path.with_name(renamed_to)
                            shutil.move(src_path, dest_path)
                            dest_path.rename(org_file)
                elif action == "copy":
                    if handler == "skip":
                        continue
                    else:
                        ext = src_path.suffix
                        chars = string.ascii_lowercase + string.digits
                        random_str = src_path.stem + "__undo_" + ''.join(random.choices(chars, k=10)) + ext
                        dest_path = os.path.join(dest_dir, random_str)
                        while os.path.exists(dest_path):
                            random_str = src_path.stem + "__undo_" + ''.join(random.choices(chars, k=10)) + ext
                            dest_path = os.path.join(dest_dir, random_str)
                        shutil.move(src_path, dest_path)

                
        if not data:
            print("No logs")
            sys.exit(1)
    except Exception as e:
        print(e)

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
        d = Path(des)
    else:
        print("Path does not exist")
        sys.exit(1)

if args.recursive:
    if Path(des).resolve().is_relative_to(Path(src).resolve()):
        print("Destination cannot be inside Source")
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
        on_coll = on_collision()
        dry_run_preview(on_coll, d, files)
    elif args.undo is True:
        try:
            input("\nUndo Feature will skip 'Skipped' logs and file if a file with same name (in case of move action) is present at the destination, also it wont be able to return any files which were overwritten. Its just an undo feature for the last instance. Press Enter to start organizing, or Ctrl+C to cancel...")
            log_id_list, files_count, act, s = show_log_menu()
            undo_last_instance(log_id_list, files_count, act, s)
        except KeyboardInterrupt:
            sys.exit(1)
    elif args.undo is not None:
        try:
            input("\nUndo Feature(For Later) will skip 'Skipped' logs and file if a file with same name (in case of move action) is present at the destination, also it wont be able to return any files which were overwritten. Its just an undo feature for the specific instance. Press Enter to start organizing, or Ctrl+C to cancel...")
            pass 
        except KeyboardInterrupt:
            sys.exit(1)
        # For Later 
    elif args.undo is None:
        if args.logs is True:
            a = 0
            log_id_list, files_count, act, s = show_log_menu()
            print("_"*40)
            print("Available Runs")
            print("_"*40)

            for id in log_id_list:
                ac = "Copied" if str(act[a]) == "copy" else "Moved"
                print(f"{a}. {id} - {files_count[a]} {ac} , {s[a]} Skipped")
                a +=1
        elif args.logs is not None:
            if isinstance(log_sr, int):
                log_id_list, files_count, act, s = show_log_menu()
                if log_sr > len(act)-1:
                    print("Please check the log list again by -l")
                else:
                    ac = "Copied" if str(act[log_sr]) == "copy" else "Moved"
                    log_sr_check(log_sr,log_id_list,files_count[log_sr],ac,s[log_sr])
            else:
                print(f"{parser.prog}: try 'python {parser.prog} --help' for more information")
        elif args.logs is None:
            if mode == "copy" or mode == "move":
                on_coll = on_collision()
                copy_move_files(d, mode, files, on_coll)
            else:
                print(f"{parser.prog}: try 'python {parser.prog} --help' for more information")
                sys.exit(1)