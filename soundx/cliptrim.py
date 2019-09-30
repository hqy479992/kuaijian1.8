import os


def trim(resultfile):


    file = open(resultfile, 'r')
    for line in file.readline():
        temp = line.split("_")
        source_video = temp[0].split(".")[0] + ".MP4"
        offset = temp[2]

        command_get_duration = "ffmpeg -i v1.MP4 2>&1|grep 'Duration'|cut -d ' ' -f 4|sed s/,//"
        p = os.popen(command_get_duration, 'r')
        duration_temp = p.read()


