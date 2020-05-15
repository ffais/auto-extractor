import os
import subprocess
import re
import glob
import datetime
from pathlib import Path

path = Path("/mnt/int_hd/Download/")
rar_command = "unrar x -r -y"
films_folder = Path("/mnt/int_hd/Download/1-Film/")
series_folder = Path("/mnt/int_hd/Download/2-Serie Tv/")
remote_films_folder = Path("/mnt/ext_hd/1-Film/")
remote_series_folder = Path("/mnt/ext_hd/2-Serie Tv")
regex_file = Path("regex-list.txt")
regex_list = []
shutdown = False
move_file = True
rm_file = True

def load_regex(regex_file_path):
    regex_file = open(regex_file_path, 'r')
    pattern = "([a-zA-Z-]+)\s+\|\s+(.*)"
    loadregex = re.compile(pattern)
    for line in regex_file:
        m = loadregex.search(line)
        regex_list.append((m.group(1), m.group(2)))
    regex_file.close()

def search_multipart(search_dir):
    pattern = "part0?0?1(?!\d)"
    multiregex = re.compile(pattern)
    for file in os.scandir(search_dir):
        if file.is_file() and file.name.endswith(".rar") and multiregex.search(file.name) != None:
            search_category(file)
        elif file.is_dir():
            search_multipart(file.path)

def search_category(file):
    for category, pattern in regex_list:
        searchregex = re.compile(pattern)
        if searchregex.match(file.name):
            if category == "film":
                destination_path = Path(films_folder)
                check_folder_exist(destination_path)
                ext_code = extract_file(file, destination_path)
                remove_multipart(ext_code, file)
            elif category == "serie-tv":
                name, season = extract_name_season(file)
                name = re.sub("\.", " ", name).rstrip()
                destination_path = Path(f"{series_folder}/{name}/Season {season}")
                check_folder_exist(destination_path)
                ext_code = extract_file(file, destination_path)
                remove_multipart(ext_code, file)

def extract_file(file, destination_path):
    archive_path = file.path
    archive_path = archive_path.translate(str.maketrans({"'": r"\'"}))
    dest_path = str(destination_path)
    dest_path = dest_path.translate(str.maketrans({"'": r"\'"," ": r"\ "}))
    print (archive_path)
    cmd = f"{rar_command} {archive_path} {dest_path}"
    print (cmd)
    exitcode = os.system(cmd)
    return exitcode

def check_folder_exist(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def extract_name_season(file):
    pattern = "(.+)S([0-9]+)"
    ext_re = re.compile(pattern)
    name = ext_re.search(file.name).group(1)
    season = ext_re.search(file.name).group(2)
    return [name, season]

def remove_multipart(ext_code, file):
    if ext_code > 0 and not rm_file:
        print (f"filename: {file.name} error: {ext_code}")
    elif ext_code == 0 and rm_file:
        print (f"filename: {file.name} error: {ext_code}")
        to_del = re.sub("part[0-9]+","part*", file.path)
        for fl in glob.glob(to_del):
            os.remove(fl)

if __name__ == "__main__":
    load_regex(regex_file)
    search_multipart(path)
    if shutdown:
        ora = datetime.datetime.now().hour
        if 0 <= ora <= 9 :
            os.system('shutdown -s -f -t 0')
    if move_file:
        os.system(f"rsync -av --remove-source-files --progress '{films_folder}/' '{remote_films_folder}/'")
        os.system(f"rsync -av --remove-source-files --progress '{series_folder}/' '{remote_series_folder}/'")
