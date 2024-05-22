from markdown import (extract_title, generate_page, generate_pages_recursive)

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
    copyDir("static", "public")
    generate_pages_recursive(src, temp, dest)

if __name__ == "__main__":
    if len(sys.argv) == 4:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("""This program replaces all the contents of a relative 'public' directory with 
    those of a 'static' directory. Then it recursively generates .html files to 
    'public' with relative paths for every .md file found in a 'content' directory. 
              \nIt can optionally take three arguments specifying alternate\n    1) Content directory\n    2) Template file\n    3) Public directory\n""")
        main("content", "template.html", "public")        #hard coded
