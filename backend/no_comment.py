import os
import zipfile
import argparse
from io import BytesIO
import sys
import argparse
def remove_comments(file_path, language, output_file_path):

    single_line_comment = None
    multi_line_comment_starts, multi_line_comment_ends = None, None

    if language in ['python', 'c', 'cpp', 'java', 'javascript']:
        if language == 'python':
            single_line_comment = '#'
            multi_line_comment_starts, multi_line_comment_ends = ("'''", '"""'), ("'''", '"""')
        elif language in ['c', 'cpp', 'java', 'javascript']:
            single_line_comment = '//'
            multi_line_comment_starts, multi_line_comment_ends = '/*', '*/'
        if language == 'javascript': 
            multi_line_comment_starts, multi_line_comment_ends = ('/*', '<!--'), ('*/', '-->')

    elif language == 'html':
        multi_line_comment_starts, multi_line_comment_ends = '<!--', '-->'
    elif language == 'css':
        multi_line_comment_starts, multi_line_comment_ends = '/*', '*/'

    inside_multi_line_comment = False
    new_lines = []

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        cleaned_line = ''
        line_has_content = False  # Flag to track if the line has non-comment content

        if not inside_multi_line_comment and single_line_comment:
            parts = line.split(single_line_comment, 1)
            line = parts[0]
            line_has_content = bool(line.strip())  # Check if there's content left
            if len(parts) > 1 and not parts[0].strip():
                continue  # Skip processing rest of the line if it's just a comment

        i = 0
        while i < len(line):
            if not inside_multi_line_comment and multi_line_comment_starts:
                for start in (multi_line_comment_starts if isinstance(multi_line_comment_starts, tuple) else [multi_line_comment_starts]):
                    if line[i:].startswith(start):
                        inside_multi_line_comment = True
                        break  # Assume the rest of the line is a comment
            elif inside_multi_line_comment and multi_line_comment_ends:
                for end in (multi_line_comment_ends if isinstance(multi_line_comment_ends, tuple) else [multi_line_comment_ends]):
                    if line[i:].startswith(end):
                        inside_multi_line_comment = False
                        i += len(end)  # Skip past the end of the comment
                        continue
            if not inside_multi_line_comment:
                cleaned_line += line[i]
                line_has_content = True
            i += 1

        # Append the line if it contains non-comment content
        if line_has_content:
            new_lines.append(cleaned_line)

    with open(output_file_path, 'w', encoding='utf-8') as file:
        # Join lines with '\n' to avoid adding extra new lines
        file.write('\n'.join(new_lines))

def detect_language(file_path):
    _, ext = os.path.splitext(file_path)
    extensions = {
        '.py': 'python',
        '.js': 'javascript',
        '.c': 'c',
        '.cpp': 'cpp',
        '.hpp': 'cpp',
        '.h': 'c',
        '.java': 'java',
        '.html': 'html',  
        '.css': 'css',   
    }
    return extensions.get(ext, None)

def process_file(file_path, original_base_dir, output_dir):
    language = detect_language(file_path)
    if language:
        # Calculate relative path
        relative_path = os.path.relpath(file_path, start=original_base_dir)
        output_file_path = os.path.join(output_dir, relative_path)
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

        print(f"Removing comments from {file_path} ({language})...")
        remove_comments(file_path, language, output_file_path)
    else:
        print(f"Unsupported file type: {file_path}")

def process_directory(directory_path, output_dir=None):
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            process_file(file_path, directory_path, output_dir)

help_message = r"""
                                                       _   
                                                      | |  
  _ __   ___   ___ ___  _ __ ___  _ __ ___   ___ _ __ | |_ 
 | '_ \ / _ \ / __/ _ \| '_ ` _ \| '_ ` _ \ / _ \ '_ \| __|
 | | | | (_) | (_| (_) | | | | | | | | | | |  __/ | | | |_ 
 |_| |_|\___/ \___\___/|_| |_| |_|_| |_| |_|\___|_| |_|\__|
                                                           
                                                           
                                                       
Welcome to no_comment, your go-to tool for tidying up your code by removing comments from various programming languages with ease.

USAGE:
    python no_comment.py [OPTIONS] PATH

OPTIONS:
    -o, --output     Specify an output directory for processed files. If not provided, 
                     no_comment will overwrite the original files.

    -h, --help       Display this help message and exit.

ARGS:
    PATH             The path to the file or directory you wish to process. no_comment 
                     recursively processes all files in the specified directory, 
                     applying comment removal based on the file extension.

SUPPORTED LANGUAGES:
    - Python (.py)
    - JavaScript (.js)
    - C (.c)
    - C++ (.cpp, .hpp)
    - Java (.java)
    - HTML (.html)
    - CSS (.css)

EXAMPLES:
    Remove comments from a single file and overwrite:
        python no_comment.py /path/to/file.py

    Remove comments from all files in a directory and output to a new location:
        python no_comment.py -o /path/to/output /path/to/directory

For more information and updates, visit [GitHub repository link].

Thank you for using no_comment. Happy coding!

Varol Cagdas TOK - 2024
C.Tok@campus.lmu.de
"""
if '--help' in sys.argv:
    print(help_message)
    sys.exit()

def main():
    parser = argparse.ArgumentParser(description='Remove comments from code files.', add_help=False) # Disable automatic help
    parser.add_argument('path', help='Path to the file or directory.')
    parser.add_argument('-o', '--output', help='Output directory for processed files.', default=None)
    args = parser.parse_args()

    if args.output and not os.path.exists(args.output):
        os.makedirs(args.output, exist_ok=True)

    output_dir = args.output if args.output else os.path.dirname(args.path)

    if os.path.isdir(args.path):
        process_directory(args.path, output_dir)
    elif os.path.isfile(args.path):
        process_file(args.path, output_dir)
    else:
        print("The path does not exist.")

if __name__ == "__main__":
    main()