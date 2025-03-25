from textnode import *
import os
import shutil
from page_generation_functions import *
import sys

def copy_directory_contents(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    shutil.copytree(source, destination)


def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    print (basepath)

    copy_directory_contents("/home/iangoller/bootdev/static_site_gen/static","/home/iangoller/bootdev/static_site_gen/docs")
    generate_page_recursive("/home/iangoller/bootdev/static_site_gen/content", "/home/iangoller/bootdev/static_site_gen/template.html", basepath)
    
main()