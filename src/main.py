from markdown import (extract_title, generate_page)

import os
import sys

def copyDir(src, dest):         #str, str
    if os.path.exists(src):
        if not os.path.exists(dest):
            if os.path.isdir(src):
                if not os.path.exists(dest):
                    print("Creating directory: "+dest)
                    os.makedirs(dest)
                files = os.listdir(src)
                for file in files:
                    copyDir(src + '/' + file, dest + '/' + file)
            elif os.path.isfile(src):
                print(f"Copying file: {dest}")
                with open(src, 'rb') as fsrc:
                    with open(dest, 'wb') as fdest:
                        fdest.write(fsrc.read())
        else:
            os.system(f"rm -r {dest}")
            copyDir(src, dest)
    else:
        print('Source path does not exist: '+src)

def main(src, temp, dest):
    # copyDir(src, dest)
    copyDir("static", "public")
    generate_page(src, temp, dest)

if __name__ == "__main__":
    if len(sys.argv) == 4:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        # main("static", "public")        #hard coded
        # print("This program copies all the contents of a directory. It requires two arguments: \n\t1) Source directory\n\t2) Destination directory")
        main("content/index.md", "template.html", "public/index.html")        #hard coded
