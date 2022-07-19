import re
from sys import argv
import os
import shutil
from pathlib import Path

CYRILLIC_SYMBOLS = (
    "а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м", "н", "о", "п", "р", "с", "т", "у",
    "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я", "є", "і", "ї", "ґ")
LATIN_ALTERNATIVE = (
    "a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
    "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANSLITERATION = {}

for cyrillic, latin in zip(CYRILLIC_SYMBOLS, LATIN_ALTERNATIVE):
    """
    Populates the transliteration mapping with "cyrillic": "latin" pairs for uppercase and lowercase letters.
    """
    TRANSLITERATION[ord(cyrillic)] = latin
    TRANSLITERATION[ord(cyrillic.upper())] = latin.capitalize()

IMAGES = (".jpeg", ".png", ".jpg", ".svg", ".bmp", ".heic")
VIDEOS = (".avi", ".mp4", ".mov", ".mkv")
DOCS = (".doc", ".docx", ".txt", ".pdf", ".xls", ".pptx", ".xlsx")
AUDIO = (".mp3", ".ogg", ".wav", ".amr")
ARCHIVES = (".zip", ".gz", ".tar", ".tar.gz")

IMAGE_DIR = "images"
AUDIO_DIR = "audio"
VIDEO_DIR = "video"
DOCUMENTS_DIR = "documents"
ARCHIVES_DIR = "archives"


def normalized_name(filename: str) -> str:
    """
    Normalizes the filename by replacing cyrillic symbols with latin alternatives, and unrecognized symbols with
    underscores.

    :return: normalized filename with extension
    """
    path = Path(filename)
    new_name = path.stem
    new_name = new_name.translate(TRANSLITERATION)

    new_name = re.sub(r"\W", "_", new_name)
    return new_name + path.suffix


def organize(f: str, path: str, folder_name: str) -> None:
    """
    Organizes the given file into corresponding folder depending on the file extension.

    :param f: path to the file
    :param path: path to the directory where the file is
    :param folder_name: name of a folder to move the file to
    """
    new_path = os.path.join(path, folder_name)
    if os.path.exists(new_path):
        shutil.move(f, os.path.join(new_path, os.path.basename(f)))
    else:
        os.mkdir(os.path.join(path, folder_name))
        shutil.move(f, os.path.join(new_path, os.path.basename(f)))


def organize_archive(f: str, path: str) -> None:
    """
    Moves the archive to the "archives" directory, unpacks it into the folder and deletes the original archive.

    :param f: path to the archive
    :param path: path to the directory where the file is
    """
    new_path = os.path.join(path, ARCHIVES_DIR)
    if os.path.exists(new_path):
        new_addr = os.path.join(new_path, os.path.basename(f))
        shutil.move(f, new_addr)
        shutil.unpack_archive(new_addr, os.path.join(new_addr, os.path.splitext(new_addr)[0]))
        os.remove(new_addr)
    else:
        os.mkdir(os.path.join(path, ARCHIVES_DIR))
        new_addr = os.path.join(new_path, os.path.basename(f))
        shutil.move(f, new_addr)
        shutil.unpack_archive(new_addr, os.path.join(new_addr, os.path.splitext(new_addr)[0]))
        os.remove(new_addr)


def is_empty_dir(directory):
    """
    Checks if the directory is empty.

    :param directory: path to the directory
    :return: True if the directory is empty, False otherwise
    """
    return len(os.listdir(directory)) == 0


def sort_folder(path: str, met_extensions: set[str], unknown_extensions: set[str]) -> None:
    """
    Iterates recursively over folders in the given path and organizes the files found in the folders according to their
    extensions.

    :param path: path to the root directory
    :param met_extensions: set of extensions already found in the root
    :param unknown_extensions: set of extensions that cannot be processed by the script
    """
    ignored_folders = [IMAGE_DIR, VIDEO_DIR, DOCUMENTS_DIR, AUDIO_DIR, ARCHIVES_DIR]
    for filename in os.listdir(path):
        f = os.path.join(path, filename)
        if os.path.isdir(f):
            if filename in ignored_folders:
                continue
            if is_empty_dir(f):
                os.rmdir(f)
            else:
                sort_folder(f, met_extensions, unknown_extensions)
                if is_empty_dir(f):
                    os.rmdir(f)
        else:
            new_path = os.path.join(path, normalized_name(f))
            if not os.path.exists(new_path):
                os.rename(f, new_path)
            extension = Path(new_path).suffix

            if extension in IMAGES:
                met_extensions.add(extension)
                organize(new_path, path, IMAGE_DIR)
            elif extension in VIDEOS:
                met_extensions.add(extension)
                organize(new_path, path, VIDEO_DIR)
            elif extension in DOCS:
                met_extensions.add(extension)
                organize(new_path, path, DOCUMENTS_DIR)
            elif extension in AUDIO:
                met_extensions.add(extension)
                organize(new_path, path, AUDIO_DIR)
            elif extension in ARCHIVES:
                met_extensions.add(extension)
                organize_archive(new_path, path)
            else:
                unknown_extensions.add(extension)


def clean_folder():
    if len(argv) != 2:
        print("You have to specify the path to the directory to organize.")
        quit()

    path = argv[1]
    met_extensions = set()
    unknown_extensions = set()
    try:
        sort_folder(path, met_extensions, unknown_extensions)
        print(f"The list of all met extensions: {list(met_extensions)}")
        print(f"The list of all unknown extensions: {list(unknown_extensions)}")
        for path, directories, files in os.walk(path):
            print('Path:{}, folders: {}, files: {}'.format(repr(path), repr(directories), repr(files)))
    except OSError as err:
        print(f"Error: {err}")


if __name__ == "__main__":
    clean_folder()
