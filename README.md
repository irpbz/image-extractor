# image-extractor
A powerful Python tool to extract images from PDF, Word (.docx), and PowerPoint (.pptx) files with a user-friendly GUI.

# Image Extractor

A powerful Python tool to extract images from PDF, Word (.docx), and PowerPoint (.pptx) files with a user-friendly GUI.

## Features

- 📄 Extract images from PDF files
- 📝 Extract images from Word documents (.docx)
- 🎨 Extract images from PowerPoint presentations (.pptx)
- 🖼️ Support for multiple image formats (JPG, PNG, JP2)
- 🎯 Unique filenames using UUID
- 💻 Graphical User Interface (GUI)
- ⌨️ Command Line Interface (CLI)

## Installation

Clone the repository:
git clone https://github.com/irpbz/image-extractor.git
cd image-extractor


Install dependencies:
pip install -r requirements.txt

Usage:
GUI Version

python src/gui_extractor.py

CLI Version:
python src/cli_extractor.py "path/to/your/file.pdf"

Requirements
    Python 3.8+
    Pillow
    pypdf
    tkinter (usually included with Python)

Supported Formats
    PDF (.pdf)
    Microsoft Word (.docx)
    Microsoft PowerPoint (.pptx)

Output
Images are saved in an extracted_images folder next to the original file with unique UUID filenames.
Contributing

Feel free to fork this project and submit pull requests!
