from textnode import *
import os
import shutil
from page_generation_functions import *

def copy_directory_contents(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    shutil.copytree(source, destination)


def main():
    copy_directory_contents("/home/iangoller/bootdev/static_site_gen/static","/home/iangoller/bootdev/static_site_gen/public")
    generate_page_recursive("/home/iangoller/bootdev/static_site_gen/content", "/home/iangoller/bootdev/static_site_gen/template.html")
    
main()