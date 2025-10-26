from setuptools import setup, find_packages
import os

# خواندن محتوای فایل README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# خواندن ورژن از فایل جداگانه
def get_version():
    with open("VERSION", "r", encoding="utf-8") as f:
        return f.read().strip()

setup(
    name="image-extractor",
    version=get_version(),
    author="Amin",
    author_email="amin.pbz@gmail.com",
    description="A powerful Python tool to extract images from PDF, Word, and PowerPoint files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/irpbz/image-extractor",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pillow>=10.0.0",
        "pypdf>=4.0.0",
    ],
    entry_points={
        "console_scripts": [
            "image-extractor-cli=src.cli_extractor:main",
            "image-extractor-gui=src.gui_extractor:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt"],
    },
    keywords="image extractor pdf word powerpoint docx pptx",
    project_urls={
        "Bug Reports": "https://github.com/irpbz/image-extractor/issues",
        "Source": "https://github.com/irpbz/image-extractor",
        "Documentation": "https://github.com/irpbz/image-extractor/wiki",
    },
)