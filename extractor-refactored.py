#!/usr/bin/env python
import os, sys, subprocess, re, glob, datetime, configparser
from pathlib import Path
from distutils.util import strtobool

path = ""
rar_command = ""
films_folder = ""
series_folder = ""
remote_films_folder = ""
remote_series_folder = ""
regex_file = ""
regex_list = []
shutdown = False
move_file = True
rm_file = True

def parse_config(configs):
    global path, rar_command, films_folder, remote_films_folder, remote_series_folder, regex_file
    global shutdown, move_file, rm_file

    config = configparser.ConfigParser()
    config.read(configs)
    print(config.sections())
    path = Path(config['folder_settings']['ScanDir'])
    print(path)
    rar_command = config['DEFAULT']['RarCommand']
    films_folder = Path(config['folder_settings']['FilmsFolder'])
    series_folder = Path(config['folder_settings']['SeriesFolder'])
    remote_films_folder = Path(config['folder_settings']['RemoteFilmsFolder'])
    remote_series_folder = Path(config['folder_settings']['RemoteSeriesFolder'])
    regex_file = Path(config['DEFAULT']['RegexFile'])
    shutdown = strtobool(config['DEFAULT']['ShutdownAfterFinish'])
    move_file = strtobool(config['DEFAULT']['MoveFileToRemote'])
    rm_file = strtobool(config['DEFAULT']['RemoveLocalFile'])


def load_regex(regex_file_path):
    regex_file = open(regex_file_path, 'r')
    pattern = r"([a-zA-Z-]+)\s+\|\s+(.*)"
    loadregex = re.compile(pattern)
    for line in regex_file:
        m = loadregex.search(line)
        regex_list.append((m.group(1), m.group(2)))
    regex_file.close()

def search_multipart(search_dir):
    pattern = r"part0?0?1(?!\d)"
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
                name = re.sub(r"\.", " ", name).rstrip()
                destination_path = Path(f"{series_folder}/{name}/Season {season}")
                check_folder_exist(destination_path)
                ext_code = extract_file(file, destination_path)
                remove_multipart(ext_code, file)

def extract_file(file, destination_path):
    cmd = f"{rar_command} {escape_char(file.path)} {escape_char(destination_path)}"
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

def escape_char(str):
    translation = str.maketrans({"'":  r"\'",
                                 "]":  r"\]",
                                 " ": r"\ ",
                                 "^":  r"\^",
                                 "$":  r"\$",
                                 "&":  r"\&"})
    return str.translate(translation)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
    else:
        config_file = "extractor.conf"
    parse_config(config_file)
    load_regex(regex_file)
    search_multipart(path)
    if shutdown:
        ora = datetime.datetime.now().hour
        if 0 <= ora <= 9 :
            os.system('shutdown -s -f -t 0')
    if move_file:
        os.system(f"rsync -av --remove-source-files --progress '{films_folder}/' '{remote_films_folder}/'")
        os.system(f"rsync -av --remove-source-files --progress '{series_folder}/' '{remote_series_folder}/'")
