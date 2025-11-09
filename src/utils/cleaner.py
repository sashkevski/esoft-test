import shutil


def clear_folder(path: str) -> None:
    shutil.rmtree(path)
