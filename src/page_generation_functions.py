import re
import os
from markdown_to_html_node import *

def extract_title(markdown):
    title = re.search(r"# .*\n", markdown)
    if title == None:
        raise Exception("no h1 header found")
    title_text = title.group(0)
    stripped_title = title_text.strip("# \n")
    return stripped_title

def generate_page(from_path, template_path, basepath):
    dest_file_path = from_path.replace("content", "docs").replace(".md", ".html")
    print(f"Generating page from {from_path} to {dest_file_path} using {template_path}")
    markdown_file = open(from_path)
    markdown_text = markdown_file.read()
    template_file = open(template_path)
    template_text = template_file.read()
    content_html_node = markdown_to_html_node(markdown_text)
    content_html_text = content_html_node.to_html()
    title = extract_title(markdown_text)
    title_template = template_text.replace("{{ Title }}", title)
    # basepath_links_html = title_template.replace("href=\"/", f"href=\"{basepath}").replace("src=\"/", f"src=\"{basepath}")
    replace_content_html = title_template.replace("{{ Content }}", content_html_text)
    final_html = replace_content_html.replace("href=/", f"href={basepath}").replace("src=/", f"src={basepath}")
    output_file = open(dest_file_path, "w")
    output_file.write(final_html)

def generate_page_recursive(from_path, template_path, basepath):
    dest_dir_path = from_path.replace("content", "docs")
    ls = os.listdir(from_path)
    for item in ls:
        item_path = os.path.join(from_path, item)
        if os.path.isfile(item_path):
            generate_page(item_path, template_path, basepath)
        else:
            os.mkdir(os.path.join(dest_dir_path, item)) #if item is a directory, creates the directory in the public folder
            generate_page_recursive(item_path, template_path, basepath)
    

# generate_page_recursive("/home/iangoller/bootdev/static_site_gen/content/", "der", "der")