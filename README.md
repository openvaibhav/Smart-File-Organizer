# Smart File Organizer

A command-line utility designed to automate everyday file management tasks directly from the terminal.

Smart File Organizer focuses on practical filesystem automation - organizing, categorizing, and restructuring files without relying on graphical interfaces.

---

## 🚀 Features (Current)

* 📂 **Automatic File Classification**
  Sorts files into categories based on extensions.

* 🧠 **Subtype Taxonomy System**
  Files are organized not just by category, but also by subcategories
  *(e.g., Documents → text / office / ebooks).*

* 🗂️ **Hierarchical Folder Creation**
  Creates structured parent folders like:

  ```
  __Documents/
  __Images/
  __Videos/
  ```

  With subtype subfolders inside them.

* 🔍 **Dry-Run Preview Mode**
  Preview file movements before executing operations.

* 📥 **Custom Source Support**
  Organize files from any specified directory.

* 📤 **Custom Destination Support**
  Output sorted files into a separate folder.

* 🧾 **Metadata Collection**
  Tracks file size and timestamps for future logging and analysis features.

---

## 🛠️ CLI Usage (Current)

```
python organizer.py --src <source_path> --des <destination_path>
python organizer.py --dry_run
```

| Flag        | Description                       |
| ----------- | --------------------------------- |
| `--src`     | Source directory to organize      |
| `--des`     | Destination directory             |
| `--dry_run` | Preview changes without executing |

---

## 🧩 Current Module

**File Organizer Engine**

Automatically:

* Scans directories
* Classifies files
* Builds folder hierarchies
* Copies or moves files into sorted structures

---

## 🧭 Vision

Smart File Organizer aims to evolve into a broader **CLI Personal Toolbox** - a suite of lightweight terminal utilities that improve productivity and automate repetitive filesystem tasks for developers and power users.

Planned expansion areas include:

* Logging & audit trails
* Duplicate conflict handling
* Recursive sorting
* Configurable taxonomies
* Plugin-style utility modules

---

## 📌 Status

Work in progress 🚧

Core classification and execution engine implemented.
Actively expanding CLI capabilities and automation features.
