
Organize downloads · PY
#!/usr/bin/env python3
"""
سكريبت لتنظيم مجلد الداونلود: بيحرّك الملفات لمجلدات حسب النوع (صور، مستندات، فيديو...).
 
الاستخدام:
    python organize_downloads.py                 # ينظم مجلد Downloads الافتراضي
    python organize_downloads.py --dry-run       # يعرض اللي هيحصل بدون ما يحرّك حاجة
    python organize_downloads.py --path "D:/Downloads"
    python organize_downloads.py --by-date       # يقسم كل نوع لمجلدات سنة-شهر
"""
 
import argparse
import shutil
from datetime import datetime
from pathlib import Path
 
CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".heic", ".ico", ".tiff"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".md", ".epub", ".ppt", ".pptx", ".odp"},
    "Spreadsheets": {".xls", ".xlsx", ".csv", ".ods", ".tsv"},
    "Videos": {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".m4v"},
    "Audio": {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"},
    "Programs": {".exe", ".msi", ".dmg", ".pkg", ".deb", ".rpm", ".apk", ".appimage"},
    "Code": {".py", ".js", ".ts", ".html", ".css", ".java", ".cpp", ".c", ".json", ".xml", ".sh", ".sql", ".ipynb"},
    "Fonts": {".ttf", ".otf", ".woff", ".woff2"},
    "Torrents": {".torrent"},
}
 
# ملفات لسه بتتحمل - مش هنلمسها
INCOMPLETE = {".crdownload", ".part", ".tmp", ".download", ".partial"}
 
OTHERS = "Others"
 
 
def get_category(file: Path) -> str:
    ext = file.suffix.lower()
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return OTHERS
 
 
def unique_destination(dest: Path) -> Path:
    """لو فيه ملف بنفس الاسم، نضيف رقم (1)، (2)... بدل ما نمسح القديم."""
    if not dest.exists():
        return dest
    counter = 1
    while True:
        candidate = dest.with_name(f"{dest.stem} ({counter}){dest.suffix}")
        if not candidate.exists():
            return candidate
        counter += 1
 
 
def organize(folder: Path, dry_run: bool = False, by_date: bool = False) -> None:
    if not folder.is_dir():
        print(f"المجلد مش موجود: {folder}")
        return
 
    moved = 0
    skipped = 0
    script_path = Path(__file__).resolve()
 
    for item in folder.iterdir():
        # نتخطى المجلدات، والملفات المخفية، والسكريبت نفسه، والتحميلات الناقصة
        if (
            not item.is_file()
            or item.name.startswith(".")
            or item.resolve() == script_path
            or item.suffix.lower() in INCOMPLETE
        ):
            skipped += 1
            continue
 
        target_dir = folder / get_category(item)
 
        if by_date:
            modified = datetime.fromtimestamp(item.stat().st_mtime)
            target_dir = target_dir / modified.strftime("%Y-%m")
 
        destination = unique_destination(target_dir / item.name)
 
        if dry_run:
            print(f"[تجربة] {item.name}  ->  {destination.relative_to(folder)}")
        else:
            target_dir.mkdir(parents=True, exist_ok=True)
            try:
                shutil.move(str(item), str(destination))
                print(f"{item.name}  ->  {destination.relative_to(folder)}")
            except (PermissionError, OSError) as e:
                print(f"تعذر نقل {item.name}: {e}")
                skipped += 1
                continue
        moved += 1
 
    action = "هيتنقل" if dry_run else "اتنقل"
    print(f"\nخلص: {moved} ملف {action}، و{skipped} تم تخطيهم.")
 
 
def main() -> None:
    parser = argparse.ArgumentParser(description="تنظيم مجلد الداونلود حسب نوع الملفات")
    parser.add_argument(
        "--path",
        type=Path,
        default=Path.home() / "Downloads",
        help="مسار المجلد (الافتراضي: مجلد Downloads بتاع المستخدم)",
    )
    parser.add_argument("--dry-run", action="store_true", help="عرض النتيجة بدون نقل فعلي")
    parser.add_argument("--by-date", action="store_true", help="تقسيم كل نوع لمجلدات سنة-شهر")
    args = parser.parse_args()
 
    organize(args.path.expanduser(), dry_run=args.dry_run, by_date=args.by_date)
 
 
if __name__ == "__main__":
    main()
 
Claude finished the response
