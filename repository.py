import os
import shutil
import filecmp
from datetime import datetime
from utils import is_ignored, create_directory


WIT_DIR = ".wit"


def init_repository():
    """
    Initialize a new wit repository by creating the .wit directory
    and its internal structure.
    """
    if os.path.exists(WIT_DIR):
        print("Repository already initialized.")
        return

    create_directory(WIT_DIR)
    create_directory(os.path.join(WIT_DIR, "commits"))
    create_directory(os.path.join(WIT_DIR, "staging"))


    head_path = os.path.join(WIT_DIR, "HEAD")
    with open(head_path, "w") as f:
        f.write("")   # HEAD מתחיל ריק

    print("Initialized empty wit repository.")

STAGING_DIR = os.path.join(".wit", "staging")


def add_to_staging(path):
    """
    Add a file or directory to the staging area.
    """
    if not os.path.exists(path):
        print(f"Error: path '{path}' does not exist")
        return

    # אם זו תיקייה, נוסיף את כל הקבצים שבתוכה
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):

            dirs[:] = [d for d in dirs if not is_ignored(os.path.join(root, d))]

            for file in files:
                full_path = os.path.join(root, file)

                if is_ignored(full_path):
                    continue

                copy_to_staging(full_path)
    else:
        if is_ignored(path):
            print(f"Ignored: {path}")
            return
        copy_to_staging(path)


def copy_to_staging(src_path):
    """
    Copy a file to the staging directory while preserving folder structure.
    """
    relative_path = os.path.relpath(src_path, os.getcwd())
    dest_path = os.path.join(STAGING_DIR, relative_path)
    dest_dir = os.path.dirname(dest_path)
    create_directory(dest_dir)
    shutil.copy2(src_path, dest_path)
    print(f"Added to staging: {relative_path}")



COMMITS_DIR = os.path.join(".wit", "commits")

def commit_repository(message):
        """
        Create a new commit from the staging area.
        """

        # בדיקה שהרפוזיטורי קיים
        if not os.path.exists(WIT_DIR):
            print("Repository not initialized.")
            return

        # בדיקה אם staging ריק
        if not os.path.exists(STAGING_DIR) or not os.listdir(STAGING_DIR):
            print("Nothing to commit.")
            return

        # יצירת מזהה ייחודי לקומיט (timestamp)
        commit_id = datetime.now().strftime("%Y%m%d%H%M%S")
        new_commit_path = os.path.join(COMMITS_DIR, commit_id)

        create_directory(new_commit_path)

        # העתקת כל התוכן מה-staging ל-commit החדש
        for root, dirs, files in os.walk(STAGING_DIR):
            for file in files:
                src_path = os.path.join(root, file)

                # שומרים על מבנה תיקיות
                relative_path = os.path.relpath(src_path, STAGING_DIR)
                dest_path = os.path.join(new_commit_path, relative_path)

                dest_dir = os.path.dirname(dest_path)
                create_directory(dest_dir)

                shutil.copy2(src_path, dest_path)

        # שמירת הודעת commit
        message_file = os.path.join(new_commit_path, "message.txt")
        with open(message_file, "w") as f:
            f.write(message)

        # ניקוי staging אחרי commit
        clear_staging()

        print(f"Commit created: {commit_id}")

def clear_staging():
    """
    Remove all files from the staging directory.
    """
    for root, dirs, files in os.walk(STAGING_DIR, topdown=False):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            os.rmdir(os.path.join(root, dir))


import os
import filecmp

def status_repository():
    """
    Show the status of the repository (staged / modified / untracked),
    ignoring files and directories listed in .witignore.

    Returns:
        dict: {
            "staged": list of files in the staging area,
            "modified": list of files changed since last commit,
            "untracked": list of new files not staged or committed
        }
    """

    # קריאת הקובץ .witignore
    def get_ignored_files():
        ignored = set()
        ignore_path = os.path.join(os.getcwd(), ".witignore")
        if os.path.exists(ignore_path):
            with open(ignore_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):  # דילוג על הערות ושורות ריקות
                        ignored.add(line)
        return ignored

    ignored = get_ignored_files()

    # יצירת מילון לתוצאות
    status_dict = {
        "staged": [],
        "modified": [],
        "untracked": []
    }

    # פונקציית עזר למציאת הקומיט האחרון
    def get_latest_commit():
        if not os.path.exists(COMMITS_DIR):
            return None
        commits = [d for d in os.listdir(COMMITS_DIR) if os.path.isdir(os.path.join(COMMITS_DIR, d))]
        if not commits:
            return None
        latest = sorted(commits)[-1]
        return os.path.join(COMMITS_DIR, latest)

    latest_commit = get_latest_commit()

    # איסוף כל הקבצים ב-staging
    staged_files = []
    for root, dirs, files in os.walk(STAGING_DIR):
        for file in files:
            rel_path = os.path.relpath(os.path.join(root, file), STAGING_DIR)
            if rel_path in ignored:
                continue
            staged_files.append(rel_path)
            status_dict["staged"].append(rel_path)

    # איסוף כל הקבצים מהקומיט האחרון
    committed_files = {}
    if latest_commit:
        for root, dirs, files in os.walk(latest_commit):
            for file in files:
                rel_path = os.path.relpath(os.path.join(root, file), latest_commit)
                if rel_path in ignored:
                    continue
                committed_files[rel_path] = os.path.join(root, file)

    # מעבר על כל קבצי תיקיית העבודה
    for root, dirs, files in os.walk(os.getcwd()):
        # הסרת תיקיות לא רצויות מהרשימה ש-os.walk יכנס בהן
        dirs[:] = [d for d in dirs if d not in ignored]

        for file in files:
            rel_path = os.path.relpath(os.path.join(root, file), os.getcwd())
            if rel_path in ignored:
                continue  # דילוג על קבצים שמופיעים ב-.witignore

            if rel_path in staged_files:
                continue  # כבר ב-staging
            elif rel_path in committed_files:
                # בדיקה אם הקובץ השתנה מאז הקומיט האחרון
                if not filecmp.cmp(os.path.join(root, file), committed_files[rel_path], shallow=False):
                    status_dict["modified"].append(rel_path)
            else:
                # קובץ חדש שלא נמצא ב-staging ולא בקומיט
                status_dict["untracked"].append(rel_path)

    return status_dict
