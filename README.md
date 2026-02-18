# Smart File Organizer

A command-line utility designed to automate everyday file management tasks directly from the terminal.

Smart File Organizer focuses on practical filesystem automation: organizing, classifying, and restructuring files without relying on graphical interfaces.

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

Classification is driven via an external **JSON taxonomy system**, allowing extensibility without modifying core code.

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

Execution includes permission validation and collision handling safeguards.

---

### 💥 Collision Handling Engine

Handles duplicate filename conflicts at destination.

Supported policies:

* **Skip (default)** → Ignore duplicates
* **Rename** → Generates unique collision filename
* **Overwrite** → Replaces existing file

**Example**

```
report.pdf
→ report__collision_x82kf91.pdf
```

Collision outcomes are logged for auditability.

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

This metadata layer powers logging and audit trails.

---

### 🔐 Permission Awareness

Validates required permissions before execution:

* **Read** → Copy / Dry-Run
* **Write + Execute** → Move
* Destination write validation

Files lacking permissions are skipped safely.

---

## 📜 Structured Execution Logging

Smart File Organizer maintains an append-only execution log:

```
log.jsonl
```

Each processed file is written as a structured JSONL entry.

### Logged Fields

* Run ID (batch identifier)
* Original filename
* File creation timestamp
* Execution timestamp
* Log timestamp
* Source path
* Destination path
* Action performed (copy / move)
* Collision outcome
* Rename mapping (if applicable)

### Example Entry

```json
{
  "id": "2026-02-17 09:15:02",
  "original_file": "report.pdf",
  "file_created_at": "2026-02-16 16:18:34",
  "executed_at": "2026-02-17 09:15:02",
  "logged_at": "2026-02-17 09:15:02",
  "src_path": "/Downloads/report.pdf",
  "dest_path": "/Organized/__Documents/report.pdf",
  "action": "copy",
  "on_collision": "rename",
  "renamed_to": "report__collision_x82kf91.pdf"
}
```

Logs are stored in **JSONL format** for streaming safety and incremental history tracking.

---

## 🧭 Run Grouping System

Every execution is assigned a unique **Run ID**.

This enables:

* Batch identification
* Execution lineage tracking
* Collision analytics
* Audit grouping

All files processed in a single command share the same Run ID.

---

## 📊 Log Inspection CLI

Execution history can be inspected directly from the terminal.

### Show All Runs

```
python organizer.py -l
```

Displays:

* Run index (serial number)
* Run ID
* Files processed
* Files skipped
* Action type

---

### Inspect Specific Run

```
python organizer.py -l <serial_number>
```

Shows detailed logs for a specific execution batch.

---

## ↩️ Undo System

Smart File Organizer includes a **batch undo engine** powered by execution logs.

Undo operates at the **run level**, reversing file operations from a specific execution instance.

---

### Undo Last Run

```
python organizer.py -u
```

Reverses the most recent execution batch.

---

### Undo Specific Run

```
python organizer.py -u <serial_number>
```

Targets a specific logged run.

---

### Undo Behavior

| Original Action | Undo Result                        |
| --------------- | ---------------------------------- |
| Move            | File moved back to source          |
| Copy            | Copied instance removed / archived |
| Rename          | Original filename restored         |
| Skip            | Ignored                            |
| Overwrite       | Cannot restore overwritten data    |

---

### Undo Safety Notes

* Skipped files are ignored
* Existing conflicts are avoided
* Overwritten originals cannot be recovered
* Requires original paths to still exist

Undo is a **best-effort rollback**, not snapshot recovery.

---

## 🛠️ CLI Usage

### Basic Execution

```
python organizer.py -m copy
```

### Source + Destination

```
python organizer.py -s ~/Downloads -d ~/Organized -m move
```

### Dry Run

```
python organizer.py -dr -m copy
```

### Recursive Sorting

```
python organizer.py -r -m move
```

### Exclusions

```
python organizer.py -e node_modules,.git -m copy
```

### Collision Policies

```
python organizer.py -oc skip
python organizer.py -oc rename
python organizer.py -oc overwrite
```

### Logs & Undo

```
python organizer.py -l
python organizer.py -l 0

python organizer.py -u
python organizer.py -u 0
```

---

## ⚙️ Flags Reference

| Flag                  | Description                                       |
| --------------------- | ------------------------------------------------- |
| `-s, --src`           | Source directory                                  |
| `-d, --des`           | Destination directory                             |
| `-m, --mode`          | Execution mode: `copy` / `move`                   |
| `-oc, --on_collision` | Collision policy: `skip` / `rename` / `overwrite` |
| `-r, --recursive`     | Include subfolders                                |
| `-e, --exclude`       | Exclude files/folders                             |
| `-l, --logs`          | View execution history                            |
| `-u, --undo`          | Undo execution batch                              |
| `-dr, --dry_run`      | Preview execution                                 |

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
* Metadata extraction
* Structured logging
* Batch undo processing

Acts as the foundational automation layer.

---

## 📌 Status

**Learning Project : Active Development 🚧**

| Layer                 | Status      |
| --------------------- | ----------- |
| Classification Engine | Stable      |
| Execution Engine      | Stable      |
| Collision System      | Implemented |
| Permission Layer      | Implemented |
| Logging System        | Implemented |
| Run Grouping          | Implemented |
| Log Viewer CLI        | Implemented |
| Undo Engine           | Implemented |

Built as a practical filesystem automation project for learning CLI systems, logging design, and rollback mechanics.
