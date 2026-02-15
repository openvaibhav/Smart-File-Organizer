# Smart File Organizer

A command-line utility designed to automate everyday file management tasks directly from the terminal.

Smart File Organizer focuses on practical filesystem automation : organizing, categorizing, and restructuring files without relying on graphical interfaces.

Built for developers, power users, and terminal-first workflows.

---

## 🚀 Features (Current)

### 📂 Automatic File Classification

Sorts files into structured categories based on extensions.

**Primary categories:**

* Documents
* Images
* Videos
* Audios
* Archives
* Uncategorized

Classification is driven via an external JSON taxonomy system.

---

### 🧠 Subtype Taxonomy System

Files are further classified into granular subtypes for deeper organization.

**Examples**

```
Documents → text / office / ebooks / code / data
Images    → common / vector / raw_camera
Audios    → lossy / lossless / studio
```

This enables multi-layer sorting without manual folder creation.

---

### 🗂️ Hierarchical Folder Generation

Automatically builds structured directories:

```
__Documents/
__Images/
__Videos/
__Audios/
__Archives/
```

Subtype folders are generated dynamically during execution.

---

### 🔁 Copy / Move Execution Modes

Choose how files are handled:

* **Copy Mode** → Leaves originals untouched
* **Move Mode** → Fully reorganizes source

Execution is performed with permission validation and collision handling.

---

### 💥 Collision Handling Engine

Handles duplicate filename conflicts at destination.

Supported policies:

* **Skip (default)** → Ignore duplicates
* **Rename** → Generates unique collision filename
* **Overwrite** → Replaces existing file

Example:

```
report.pdf
→ report__collision_x82kf91.pdf
```

---

### 🔍 Dry-Run Preview Mode

Preview execution before performing operations.

Displays:

* Source → Destination mapping
* Collision outcomes
* Skipped files

Prevents accidental filesystem changes.

---

### 🔁 Recursive Sorting

Process files inside nested subfolders:

```
python organizer.py -r
```

Useful for deep directory cleanup.

---

### 🚫 Exclusion Filters

Exclude files or folders from processing:

```
python organizer.py -e node_modules,.git,env
```

Organizer system folders are auto-excluded.

---

### 🧾 Metadata Collection Layer

Each processed file records:

* File size
* Creation timestamp
* Modification timestamp

This metadata layer prepares the engine for:

* Execution logging
* Audit manifests
* Undo systems

---

### 🔐 Permission Awareness

Validates required permissions before execution:

* Read → Copy / Dry-Run
* Write + Execute → Move
* Destination write validation

Files lacking permissions are skipped safely.

---

## 🛠️ CLI Usage

### Basic Execution

```
python organizer.py -m copy
```

---

### Source + Destination

```
python organizer.py -s ~/Downloads -d ~/Organized -m move
```

---

### Dry Run

```
python organizer.py -dr -m copy
```

---

### Recursive Sorting

```
python organizer.py -r -m move
```

---

### Exclusions

```
python organizer.py -e node_modules,.git -m copy
```

---

### Collision Policies

```
python organizer.py -oc skip
python organizer.py -oc rename
python organizer.py -oc overwrite
```

---

## ⚙️ Flags Reference

| Flag                  | Description                                            |
| --------------------- | ------------------------------------------------------ |
| `-s, --src`           | Source directory                                       |
| `-d, --des`           | Destination directory                                  |
| `-m, --mode`          | Execution mode: `copy` / `move`                        |
| `-oc, --on_collision` | Collision policy mode: `skip` / `rename` / `overwrite` |
| `-r, --recursive`     | Include subfolders                                     |
| `-e, --exclude`       | Exclude files/folders                                  |
| `-dr, --dry_run`      | Preview execution                                      |

---

## 🧩 Core Module

### File Organizer Execution Engine

Responsibilities:

* Directory scanning
* Permission validation
* File classification
* Taxonomy mapping
* Collision resolution
* Folder generation
* Safe execution handling

Acts as the foundational automation layer.

---

## 🧭 Architecture Vision

Smart File Organizer is evolving into a broader **CLI Personal Toolbox** : a suite of terminal utilities focused on filesystem automation.

Planned systems:

* Structured execution logging
* Undo / rollback engine
* Duplicate detection
* Large file sorters
* Temp & cache cleaners
* Configurable taxonomies
* Plugin modules

---

## 📌 Status

**Work in Progress 🚧**

| Layer                 | Status      |
| --------------------- | ----------- |
| Classification Engine | Stable      |
| Execution Engine      | Stable      |
| Collision System      | Implemented |
| Permission Layer      | Implemented |
| Logging System        | Planned     |
| Undo Engine           | Planned     |

Actively iterating toward a stable **v1.0 CLI automation toolkit**.
