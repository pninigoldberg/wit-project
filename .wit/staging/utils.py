import os


def create_directory(path):
    """
    Create a directory if it does not already exist.
    """
    os.makedirs(path, exist_ok=True)

def is_ignored(path):
    """
    Check if a file or directory should be ignored.
    """

    relative_path = os.path.relpath(path, os.getcwd())
    DEFAULT_IGNORES = [".wit", "__pycache__"]

    # 🔥 התעלמות קבועה
    for ignored in DEFAULT_IGNORES:
        if relative_path.startswith(ignored):
            return True

    # בדיקה מול .witignore
    if os.path.exists(".witignore"):
        with open(".witignore", "r") as f:
            ignored_files = [line.strip() for line in f if line.strip()]

        if relative_path in ignored_files:
            return True

    return False

