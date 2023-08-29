import os
import re
import sys
import shutil
from pathlib import Path

dir_suff_dict = {"Images": ['.jpg', '.jpeg', '.png', '.gif', '.tiff', '.ico', '.bmp', '.webp', '.svg'],
                 "Documents": [".md", ".epub", ".txt", ".docx", ".doc", ".ods", ".odt", ".dotx", ".docm", ".dox",
                               ".rvg", ".rtf", ".rtfd", ".wpd", ".xls", ".xlsx", ".ppt", ".pptx", ".csv", ".xml"],
                 "Archives": [".iso", ".tar", ".gz", ".7z", ".dmg", ".rar", ".zip"],
                 "Audio": [".aac", ".m4a", ".mp3", "ogg", ".raw", ".wav", ".wma"],
                 "Video": [".avi", ".flv", ".wmv", ".mov", ".mp4", ".webm", ".vob", ".mpg", ".mpeg", ".3gp"],
                 "PDF": [".pdf"],
                 "HTML": [".html", ".htm", ".xhtml"],
                 "EXE_MSI": [".exe", ".msi"],
                 "PYTHON": [".py", ".pyw"]}


def normalize(name: str) -> str:
    CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    TRANSLATION = (
    "a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
    "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja")

    TRANS = {}
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()
    t_name = name.translate(TRANS)
    t_name = re.sub(r'\W', '_', t_name)
    return t_name


images = list()
documents = list()
video = list()
archives = list()
music = list()
others = list()
folders = list()
unknown = set()
extensions = set()

registered_extensions = {"JPEG": images, "PNG": images,"JPG": images, "SVG": images,
    "TXT": documents, "DOCX": documents,"DOC": documents,"PDF": documents,"XLSX": documents,"PPTX": documents,
    "AVI": video, "MP4":video, "MOV":video, "MKV":video,
    "ZIP": archives,"TAR": archives, "GZ": archives,
    "MP3":music, "OGG":music, "WAV":music, "AMR": music
}


def get_extensions(file_name):
    return Path(file_name).suffix[1:].upper()

def scan(folder):
    for file in folder.iterdir():
        if file.is_dir():
            if file.name not in ("Images", "Documents", "Video", "Archives", "Music", "Others"):
                folders.append(file)
                if not any(file.iterdir()):
                    file.rmdir()
                scan(file)
            continue

        extension = get_extensions(file_name=file.name)
        new_name = folder/file.name
        if not extension:
            others.append(new_name)
        else:
            try:
                container = registered_extensions[extension]
                extensions.add(extension)
                container.append(new_name)
            except KeyError:
                unknown.add(extension)
                others.append(new_name)
    

def del_empty_dirs(path_dir): 
    for d in os.listdir(path_dir):
        a = os.path.join(path_dir, d)
        if os.path.isdir(a):
            if not os.listdir(a):
                os.rmdir(a)
            else:
                del_empty_dirs(a)

def main(path_dir):
    path_dir = arg
    if not Path(path_dir).exists():
        print('[-] Папки не існує')
    else:
        sort(path_dir)

def sort(path_dir):
    cur_dir = Path(path_dir)
    dir_path = []
    scan(cur_dir)
    for root, dirs, files in os.walk(path_dir):
        for d in dirs:
            if d not in ("Images", "Documents", "Video", "Archives", "Music", "Others"):
                dir_path.append(os.path.join(root, d))
        for file in files:
            p_file = Path(root) / file
            for suff in dir_suff_dict:
                if p_file.suffix.lower() in dir_suff_dict[suff]:
                    if suff == 'Archives':
                        archive_dir = cur_dir.joinpath(suff)             
                        base_archive_dir = archive_dir.joinpath(f"{(normalize(p_file.name[0:-len(p_file.suffix)]))}")
                        archive_dir.mkdir(exist_ok=True)
                        base_archive_dir.mkdir(exist_ok=True)
                        shutil.unpack_archive(p_file, base_archive_dir)
                        os.remove(p_file)
                    else:
                        dir_img = cur_dir.joinpath(suff)
                        dir_img.mkdir(exist_ok=True)
                        try:
                            p_file.rename(dir_img.joinpath(p_file.name))
                        except FileExistsError:
                            p_file.rename(dir_img.joinpath(f'{p_file.name.split(".")[0]}_c{p_file.suffix}'))
                            print(f"Можливо дублікат: {p_file.name}")
        del_empty_dirs(path_dir) 
    for root, dirs, files in os.walk(path_dir):
        for file in files:
            p_file = Path(root) / file
            name_normalize = f"{normalize(p_file.name[0:-len(p_file.suffix)])}{p_file.suffix}"
            p_file.rename(Path(root) / name_normalize)
            

if __name__ == "__main__":
    path_dir = sys.argv[1]
    print(f"Start in {path_dir}")
    arg = Path(path_dir)
    main(arg.resolve())
    print("Finished!!!")
    exit()