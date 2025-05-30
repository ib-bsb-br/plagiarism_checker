# Copy Spotter
![PyPI - Version](https://img.shields.io/pypi/v/copy-spotter) ![PyPI - License](https://img.shields.io/pypi/l/copy-spotter)
![Python](https://img.shields.io/badge/python-3.11-blue)


![GIF demo](https://raw.githubusercontent.com/Wazzabeee/copy-spotter/main/data/img/example.gif)

## About
Copy Spotter will process pdf, txt, docx, and odt files that can be found in the given input directory, find similar sentences, calculate similarity percentage, display a similarity table with links to side by side comparison where similar sentences are highlighted.

**Usage**
---

```bash
pip install copy-spotter
copy-spotter [-s] [-o] [-h] input_directory
```
Usage: `copy-spotter input_directory [OPTIONS]`

Performs a similarity analysis of all text files available in given input directory.
Developed by Clément Delteil -> (Github: Wazzabeee)

***Positional Arguments:***
* `input_directory`: One directory that contains all files (pdf, txt, docx, odt) (see `data/pdf/plagiarism` for example). Currently, the script processes files directly within this directory and does not search subdirectories recursively.
  ```
  input_directory/
  │
  ├── file_1.docx
  ├── file_2.pdf
  └── file_3.pdf
  ```

***Optional Arguments:***
* `-s`, `--block-size`: Set minimum number of consecutive and similar words detected. (Default is 2)
* `-o`, `--out_dir`: Set the output directory for html files. (Default is creating a new directory called `results`)
* `-h`, `--help`: Show this message and exit.

**Examples**
---
```bash
# Analyze documents in 'data/pdf/plagiarism', with default settings
copy-spotter data/pdf/plagiarism

# Analyze with custom block size and specify output directory
copy-spotter data/pdf/plagiarism -s 5 -o results/output
```

**Development Setup**
---
```bash
# Clone this repository
git clone https://github.com/Wazzabeee/copy-spotter
# Go into the repository
cd copy-spotter
# Install core requirements
pip install -r requirements.txt
# Install development and linting tools
pip install -r requirements_lint.txt
pip install pytest pre-commit
# Set up pre-commit hooks
pre-commit install
# Run tests
pytest tests/
# Run the app using the module path
python -m scripts.main data/pdf/plagiarism -s 2
# Or, after installing in editable mode (pip install -e .):
copy-spotter data/pdf/plagiarism -s 2
```

**Recommendations**
---
- Please make sure that all text files are closed before running the program.
- In order to get the best results please provide text files of the same languages.
- Ensure you have writing access when using `copy-spotter`.
- If a specific file is not processed correctly feel free to [contact me](mailto:clement45.delteil45@gmail.com) so that I can address the issue.

**TODO**
---
- Add more tests
- Add support for other folder structures
- Add more tests on existing functions
- Implement OCR with tesseract for scanned documents (Initial PDF text extraction improved, OCR is fallback)
- Add custom naming option for pdf files
