import os
import subprocess
import re
import glob
import datetime

path = "D:\\Download"
rar = '"C:\\Program Files\\WinRAR\\Rar.exe" x -r -y -ri10 '
archive = 'D:\\Download\\Riverdale.S03E02.Chapter.Thirty-Seven.Fortune.And.Mens.Eyes.1080p.AC3.ITA.ENG.part1.rar'
#dest = 'D:\\Download\\Riverdale'
def search_folder():
    for folder in os.listdir(path):
        if os.path.isdir(os.path.join(os.path.abspath(path), folder)):
            dotname = re.sub("\s+", ".", folder.strip())
            print (dotname)
            if re.search("(.+)S[0-9]+E[0-9]+",dotname):
                removefld = extract_file(os.path.join(path,folder))
                if removefld == 0:
                    os.remove(os.path.join(path,folder))
            elif re.search("(.+)[0-9]{4}\.FU22\.HD",dotname):
                removefld = extract_file(os.path.join(path,folder))
                if removefld == 0:
                    os.remove(os.path.join(path,folder))
            elif re.search("(.+)[0-9]{4}\.FULL\.HD",dotname):
                removefld = extract_file(os.path.join(path,folder))
                time.sleep(7)
                if removefld == 0:
                    os.rmdir(os.path.join(path,folder))
    return
def extract_file(abpath):
    exitcode = 1
    for file in os.listdir(abpath):
        if file.endswith(".rar"):
            if re.search("part0?0?1(?!\d)",file):
                #print (file)
                if re.search("(.+)S[0-9]+E[0-9]+",file):
                    print ("serie tv")
                    name = re.search("(.+)S[0-9]+E[0-9]+",file).group(1)
                    name = re.sub("\.", " ", name).rstrip()
                    dest = path + "\\2-Serie Tv\\" + name
                    if not os.path.exists(dest):
                        os.makedirs(dest)
                    multipart = re.sub("part[0-9]+","part*", file)
                    source = abpath + "\\" + multipart
                    cmd = rar + '"' + source + '"' + " " + '"' + dest +'"'
                    exitcode = subprocess.call(cmd, shell=True)
                    if exitcode > 0:
                        print (exitcode)
                    else :
                        for fl in glob.glob(source):
                            os.remove(fl)
                elif re.search("(.+)S[0-9]+\.[0-9]{4}p?",file):
                    print ("serie tv completa")
                    name = re.search("(.+)S([0-9]+)\.[0-9]{4}p?",file).group(1)
                    name = re.sub("\.", " ", name).rstrip()
                    season = re.search("(.+)S([0-9]+)\.[0-9]{4}p?",file).group(2)
                    dest = path + "\\2-Serie Tv\\" + name
                    if not os.path.exists(dest):
                        os.makedirs(dest)
                    dest = path + "\\2-Serie Tv\\" + name + "\\Season " + season
                    if not os.path.exists(dest):
                        os.makedirs(dest)
                    multipart = re.sub("part[0-9]+","part*", file)
                    source = abpath + "\\" + multipart
                    cmd = rar + '"' + source + '"' + " " + '"' + dest +'"'
                    exitcode = subprocess.call(cmd, shell=True)
                    if exitcode > 0:
                        print (exitcode)
                    else :
                        for fl in glob.glob(source):
                            os.remove(fl)
                elif re.search("(.+)[0-9]{4}\.FULL\.HD",file):
                    dest = path + "\\1-Film\\"
                    multipart = re.sub("part[0-9]+","part*", file)
                    source = abpath + "\\" + multipart
                    cmd = rar + source + " " + '"' + dest +'"'
                    exitcode = subprocess.call(cmd, shell=True)
                    if exitcode > 0:
                        print (exitcode)
                    else :
                        for fl in glob.glob(source):
                            os.remove(fl)
                elif re.search("(.+)[0-9]{4}\.FU22\.HD",file):
                    dest = path + "\\1-Film\\"
                    multipart = re.sub("part[0-9]+","part*", file)
                    source = abpath + "\\" + multipart
                    cmd = rar + '"' + source + '"' + " " + '"' + dest + '"'
                    print (cmd)
                    exitcode = subprocess.call(cmd, shell=True)
                    if exitcode > 0:
                        print (exitcode)
                    else :
                        for fl in glob.glob(source):
                            os.remove(fl)
                else:
                    dest = path + "\\"
                    multipart = re.sub("part[0-9]+","part*", file)
                    source = abpath + "\\" + multipart
                    cmd = rar + source + " " + '"' + dest +'"'
                    exitcode = subprocess.call(cmd, shell=True)
                    if exitcode > 0:
                        print (exitcode)
                    else :
                        for fl in glob.glob(source):
                            os.remove(fl)
    return exitcode
print ("Searching folders")
search_folder()
print ("Searching files")
extract_file(path)
ora = datetime.datetime.now().hour
if 0 <= ora <= 9 :
    os.system('shutdown -s -f -t 0')
