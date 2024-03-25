
# no_comment

`no_comment` is a versatile tool designed to clean up your code by removing comments from files across multiple programming languages. With support for languages including Python, JavaScript, C, C++, Java, HTML, and CSS, `no_comment` streamlines the process of preparing code for production or review by stripping out unnecessary comments, while preserving the integrity and functionality of the original code.

## Features

- Supports a wide range of programming languages.
- Can process individual files or entire directories.
- Offers the option to specify an output directory for the cleaned files.
- Simple and intuitive command-line interface.
- Cross-platform compatibility.

## Supported Languages

- Python (.py)
- JavaScript (.js)
- C (.c)
- C++ (.cpp, .hpp)
- Java (.java)
- HTML (.html)
- CSS (.css)

## Requirements

- Python 3.6 or higher

## Installation

Clone the repository to your local machine:

```
git clone https://github.com/yourusername/no_comment.git
```

Navigate to the cloned directory:

```
cd no_comment
```

No additional installation steps are required, as the script uses standard Python libraries.

## Usage

To use `no_comment`, you can specify the path to a single file or a directory. If processing a directory, the tool will recursively process all supported files within that directory.

### Basic Command

```
python no_comment.py [OPTIONS] PATH
```

### Options

- `-o, --output`: Specify the output directory for processed files. If not provided, `no_comment` will overwrite the original files.
- `-h, --help`: Display the help message and exit.

### Examples

Remove comments from a single file and overwrite:

```
python no_comment.py /path/to/file.py
```

Remove comments from all files in a directory and output to a new location:

```
python no_comment.py -o /path/to/output /path/to/directory
```

## Contributing

Contributions to `no_comment` are welcome. Please follow the standard GitHub pull request workflow to propose improvements or fixes.


## Contact

Varol Cagdas TOK - C.Tok@campus.lmu.de

Thank you for using `no_comment`. Happy coding!
