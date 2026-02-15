import os
import shutil
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
