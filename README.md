# Smart File Organizer

A command-line utility designed to automate everyday file management tasks directly from the terminal.

Smart File Organizer focuses on practical filesystem automation — organizing, categorizing, and restructuring files without relying on graphical interfaces.

Built for developers, power users, and anyone who prefers terminal-first workflows.

---

## 🚀 Features (Current)

### 📂 Automatic File Classification

Sorts files into structured categories based on extensions.

Supported primary categories include:

* Documents
* Images
* Videos
* Audios
* Archives
* Uncategorized

---

### 🧠 Subtype Taxonomy System

Files are classified beyond top-level categories into granular subtypes.

**Examples:**

```
Documents → text / office / ebooks / code / data
Images    → common / vector / raw_camera
Audios    → lossy / lossless / studio
```

This enables deeper organization without manual folder creation.

---

### 🗂️ Hierarchical Folder Generation

Automatically builds structured directories such as:

```
__Documents/
__Images/
__Videos/
__Audios/
__Archives/
```

Each containing subtype subfolders when applicable.

---

### 🔁 Copy / Move Execution Modes

Choose how files are handled:

* **Copy Mode** → Leaves originals untouched
* **Move Mode** → Fully reorganizes source

---

### 🔍 Dry-Run Preview Mode

Preview sorting operations before execution:

* Displays source → destination mapping
* Helps validate taxonomy + exclusions
* Prevents accidental file movement

---

### 📥 Custom Source Support

Organize files from any directory:

```
python organizer.py --src ~/Downloads
```

---

### 📤 Custom Destination Support

Output sorted files to a separate location:

```
python organizer.py --des ~/Organized
```

---

### 🔁 Recursive Sorting

Process files inside subfolders:

```
python organizer.py -r
```

Useful for deep cleanup of messy directories.

---

### 🚫 Exclusion Filters

Exclude specific files or folders from sorting:

```
python organizer.py -e node_modules,.git,env
```

Prevents interference with development environments.

---

### 🧾 Metadata Collection Layer

Each processed file records:

* Size
* Creation timestamp
* Modification timestamp

This lays groundwork for:

* Logging
* Audit trails
* Analytics modules

---

## 🛠️ CLI Usage

### Basic

```
python organizer.py -m copy
```

### With Source & Destination

```
python organizer.py -s <source_path> -d <destination_path> -m move
```

### Dry Run

```
python organizer.py -dr -m copy
```

### Recursive + Exclusions

```
python organizer.py -r -e node_modules,.git -m move
```

---

## ⚙️ Flags Reference

| Flag              | Description                     |
| ----------------- | ------------------------------- |
| `-s, --src`       | Source directory                |
| `-d, --des`       | Destination directory           |
| `-m, --mode`      | Execution mode: `copy` / `move` |
| `-r, --recursive` | Include subfolders              |
| `-e, --exclude`   | Exclude files/folders           |
| `-dr, --dry_run`  | Preview execution               |

---

## 🧩 Current Module

### File Organizer Engine

Core responsibilities:

* Directory scanning
* File classification
* Taxonomy mapping
* Folder generation
* Safe execution handling

Designed as the foundation for future automation modules.

---

## 🧭 Vision

Smart File Organizer is evolving into a broader **CLI Personal Toolbox** — a suite of lightweight terminal utilities focused on filesystem automation.

Planned expansion areas:

* Execution logging & audit trails
* Conflict / duplicate handling
* Undo manifests
* Large file sorters
* Temp & cache cleaners
* Configurable taxonomies
* Plugin-style modules

---

## 📌 Status

**Work in Progress 🚧**

Engine: Functional
CLI Layer: Expanding
Safety Systems: In Development

Actively iterating toward a stable **v1.0 CLI automation toolkit**.
