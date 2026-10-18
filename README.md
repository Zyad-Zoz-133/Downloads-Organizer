📂 Downloads Organizer

A simple Python script that tidies up your Downloads folder by sorting files into folders based on their type (images, documents, videos, archives, and more).

⚡ Vibe coded: this project was built through vibe coding with Claude (by Anthropic). It works for my setup, but it hasn't been battle-tested, so run it with --dry-run first and review the code before pointing it at anything important.

Features
Sorts files into category folders: Images, Documents, Spreadsheets, Videos, Audio, Archives, Programs, Code, Fonts, Torrents, and Others
Dry-run mode to preview changes without moving anything
Optional sub-folders by date (YYYY-MM) within each category
Never overwrites files: name clashes become file (1).ext, file (2).ext, and so on
Skips unfinished downloads (.crdownload, .part, .tmp, ...), hidden files, existing folders, and the script itself
Safe to run repeatedly: only loose files are moved, and existing category folders are reused
No dependencies, standard library only
Requirements
Python 3.8+
Usage
Download organize_downloads.py (or clone this repo).
Open a terminal in the folder containing the script.
Preview what would happen:
bash
   python organize_downloads.py --dry-run
If it looks right, run it for real:
bash
   python organize_downloads.py
Options
Option	Description
--path "<folder>"	Folder to organize. Defaults to your user's Downloads folder.
--dry-run	Show what would be moved without moving any files.
--by-date	Add YYYY-MM sub-folders inside each category, based on the file's modified date.
Examples
bash
# Organize a custom folder
python organize_downloads.py --path "C:\Users\you\Downloads"

# Preview with date sub-folders
python organize_downloads.py --by-date --dry-run

# Organize and group by month
python organize_downloads.py --by-date

Result:

Downloads/
├── Images/
│   └── 2026-10/
├── Documents/
├── Videos/
├── Archives/
└── Others/
Changing the default folder

By default the script organizes the Downloads folder inside your user's home directory (e.g. C:\Users\you\Downloads on Windows, ~/Downloads on Linux/macOS). If your Downloads folder lives somewhere else, either pass --path each time, or edit the default near the bottom of the script:

python
default=Path.home() / "Downloads",
# for example, to always use another drive:
default=Path(r"D:\Downloads"),
Customizing categories

Open the script and edit the CATEGORIES dictionary at the top to add or change file extensions and folders:

python
CATEGORIES = {
    "Images": {".jpg", ".png", ".webp"},
    "Ebooks": {".epub", ".mobi"},   # add your own
}
Automating it (optional)
Windows: create a task in Task Scheduler that runs python C:\path\to\organize_downloads.py
Linux/macOS: add a cron job, for example 0 * * * * python3 /path/to/organize_downloads.py
Disclaimer

This script moves files on your computer. It never deletes or overwrites anything, but always try --dry-run first. Use at your own risk.

License

MIT, feel free to use, modify, and share.
