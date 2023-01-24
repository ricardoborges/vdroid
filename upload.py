import os, json, shutil
from pprint import pprint
import subprocess

def uploadfiles():
    list = []
    for root, dirs, files in os.walk("Finalizados/"):
        for file in files:
            if file.endswith(".json"):
                list.append(os.path.join(root, file))
   
    return list

def dict_to_array(d):
    return [(k, v) for k, v in d.items()]

def buildCmd(item):
    args = ['youtube-upload']
    list = dict_to_array(item)

    for pair in list:
        args.append(pair[0])
        args.append(pair[1])

    #args.append("4/1AWtgzh6NymVvgYTbb6v1fm6evFfWWeVixnIjPf8sxu-F4EbJyNsB9SoQDd8")
    args.pop()
    return args

def openFile(file):
    with open(file, 'r') as json_file:
        content = json_file.read()

    return json.loads(content)

def doUpload(item):
    cmd = buildCmd(item)
    print(f"[uploading {item['--title']}...]")
    print(subprocess.check_output(cmd))
    shutil.copyfile(f"Finalizados/{item['--title']}.json", f"Uploaded/{item['--title']}.json")

def main():
    print("[start]")
    files = uploadfiles()

    for file in files:
        item = openFile(file)
        found = os.path.isfile(f"Uploaded/{item['--title']}.json")

        if (found):
            continue

        doUpload(item)
 

if __name__ == "__main__":
    main()

